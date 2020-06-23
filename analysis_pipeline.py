import logging
import tempfile
import os
import csv
import argparse

import run_rp2paths
import run_rpreader
import run_rpcofactors
import run_rpfba
import run_rpthermo
import run_rpfindpathway
import run_rpglobalscore
import run_rpreport
import run_rpvisualiser


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def pathwayAnalysis(rp2_pathways.
                    path_to_res=None,
                    retrorules_file=None,
                    sinkfile=None,
                    topx=200,
                    timeout=99999,
                    dont_merge=True,
                    num_workers=1,
                    pubchem_search=False):
    if path_to_res==None:
        path_to_res = os.path.join(os.path.abspath(os.getcwd()), 'pathway_analysis')
        if not os.path.exists(path_to_res):
            os.mkdir(path_to_res)
        else:
            logging.error('Folder '+str(os.path.join(os.path.abspath(os.getcwd()), 'pathway_analysis'))+' already exists, specify different folder or delete the current one')
            return False, 'outfolder'
    rp_pathways = os.path.join(path_to_res, 'rp_pathways.csv')
    if not os.path.exists(rp_pathways):
        logging.error('Could not find the rp2_pathways.csv file')
        return False, 'rp2'
    ##########################################################
    ################# rp2paths ###############################
    ##########################################################
    logging.info('#################### rp2paths  ######################')
    rp2paths_compounds = os.path.join(path_to_res, 'rp2paths_compounds.csv')
    rp2paths_pathways = os.path.join(path_to_res, 'rp2paths_pathways.csv')
    if not os.path.exists(rp2paths_compounds) and not os.path.exists(rp2paths_pathways):
        run_rp2paths.main(rp_pathways, rp2paths_pathways, rp2paths_compounds, timeout)
    if not os.path.exists(rp2paths_compounds) or not os.path.exists(rp2paths_pathways):
        logging.error('rp2paths did not generate files')
        return False, 'rp2paths'
    ##########################################################
    ################### rpReader #############################
    ##########################################################
    logging.info('#################### rpReader ######################')
    path_rpreader = os.path.join(path_to_res, 'rpreader.tar')
    if not os.path.exists(path_rpreader):
        run_rpreader.main(rp_pathways, rp2paths_pathways, rp2paths_compounds, path_rpreader, pubchem_search=pubchem_search)
    if not os.path.exists(path_rpreader):
        logging.error('rpReader did not generate a file')
        return False, 'rpreader'
    ##########################################################
    ################# rpCofactors ############################
    ##########################################################
    logging.info('#################### rpCofactors ######################')
    path_rpcofactors = os.path.join(path_to_res, 'rpcofactors.tar')
    if not os.path.exists(path_rpcofactors):
        run_rpcofactors.main(path_rpreader, 'tar', path_rpcofactors, pubchem_search=pubchem_search)
    if not os.path.exists(path_rpcofactors):
        logging.error('rpCofactors did not generate a file')
        return False, 'rpcofactors'
    ##########################################################
    ######################## rpFBA ###########################
    ##########################################################
    logging.info('#################### rpFBA ######################')
    path_rpfba = os.path.join(path_to_res, 'rpfba.tar')
    logging.info('gem_sbml: '+str(gem_sbml))
    if not os.path.exists(path_rpfba):
        run_rpfba.main(path_rpcofactors, 'tar', gem_sbml, path_rpfba, num_workers, str(dont_merge))
    if not os.path.exists(path_rpfba):
        logging.error('rpFBA did not generate a file')
        return False, 'rpfba'
    ##########################################################
    ##################### rpThermo ###########################
    ##########################################################
    logging.info('#################### rpThermo ######################')
    path_rpthermo = os.path.join(path_to_res, 'rpthermo.tar')
    if not os.path.exists(path_rpthermo):
        run_rpthermo.main(path_rpfba, 'tar', path_rpthermo, num_workers)
    if not os.path.exists(path_rpthermo):
        logging.error('rpThermo did not generate a file')
        return False, 'rpthermo'
    ##########################################################
    ##################### rpGlobalScore ######################
    ##########################################################
    logging.info('#################### rpGlobalScore ######################')
    path_rpglobalscore = os.path.join(path_to_res, 'rpglobalscore.tar')
    if not os.path.exists(path_rpglobalscore):
        run_rpglobalscore.main(path_rpthermo, 'tar', path_rpglobalscore, topX=topx)
    if not os.path.exists(path_rpglobalscore):
        logging.error('rpGlobalScore did not generate a file')
        return False, 'rpglobalscore'
    ##########################################################
    ##################### rpVisualiser #######################
    ##########################################################
    logging.info('#################### rpVisualiser ######################')
    path_rpvisualiser = os.path.join(path_to_res, 'rpvisualiser.html')
    if not os.path.exists(path_rpvisualiser):
        run_rpvisualiser.main(path_rpglobalscore, 'tar', path_rpvisualiser)
    if not os.path.exists(path_rpvisualiser):
        logging.error('rpVisualiser did not generate a file')
        return False, 'rpvisualiser'
    ##########################################################
    ##################### rpReport ###########################
    ##########################################################
    logging.info('#################### rpReport ######################')
    path_rpreport = os.path.join(path_to_res, 'rpreport.csv')
    if not os.path.exists(path_rpreport):
        run_rpvisualiser.main(path_rpglobalscore, 'tar', path_rpreport)
    if not os.path.exists(path_rpreport):
        logging.error('rpReport did not generate a file')
        return False, 'rpreport' 
    return True, ''



if __name__=="__main__":
    parser = argparse.ArgumentParser('Given results by RetroPath2 convert the results to SBML files and perform pathway analysis and ranking')
    parser.add_argument('-rp2_pathways', type=str)
    parser.add_argument('-output_folder', type=str, default='None')
    parser.add_argument('-topX', type=int, default=200)
    parser.add_argument('-timeout', type=float, default=240.0)
    parser.add_argument('-dont_merge', type=str, default='True')
    parser.add_argument('-num_workers', type=int, default=1)
    parser.add_argument('-pubchem_search', type=str, default='False')
    params = parser.parse_args()
    if params.dont_merge=='True' or params.dont_merge=='T' or params.dont_merge=='true' or params.dont_merge=='t':
        dont_merge = True
    elif params.dont_merge=='False' or params.dont_merge=='F' or params.dont_merge=='false' or params.dont_merge=='f':
        dont_merge = False
    else:
        logging.error('Cannot interpret dont_merge input: '+str(params.dont_merge))
        exit(1)
    params = parser.parse_args()
    if params.pubchem_search=='True' or params.pubchem_search=='T' or params.pubchem_search=='true' or params.pubchem_search=='t':
        pubchem_search = True
    elif params.pubchem_search=='False' or params.pubchem_search=='F' or params.pubchem_search=='false' or params.pubchem_search=='f':
        pubchem_search = False
    else:
        logging.error('Cannot interpret pubchem_search input: '+str(params.pubchem_search))
        exit(1)
    outfolder = None
    if params.output_folder=='None':
        if not os.path.exists('rp2_analysis'):
            os.mkdir(os.path.join(os.path.abspath(os.getcwd()), 'rp2_analysis'))
            outfolder = os.path.join(os.path.abspath(os.getcwd()), 'rp2_analysis')
        else:
            logging.error('The rp2_analysis folder already exists, please delete it or point to another folder location')
            exit(1)
    else:
        if not os.path.exists(params.output_folder):
            os.mkdir(params.output_folder)
            outfolder = params.output_folder
        else:
            logging.error('The path: '+str(params.output_folder)+' already exists, please delete or input a different path')
            exit(1)
    #### run the pathway analysis pipeline ####
    status, error_type = pathwayAnalysis(params.rp2_pathways,
                                         outfolder,
                                         params.topx,
                                         params.timeout,
                                         dont_merge,
                                         params.num_workers,
                                         pubchem_search)
    if status:
        logging.info('The pipeline successfully ran')
    else:
        logging.error('The pipeline failed at the following step: '+str(error_type))
