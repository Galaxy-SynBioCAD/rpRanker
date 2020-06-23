import logging
import os
import argparse
import deep_rp2
import analysis_pipeline

if __name__=="__main__":
    parser = argparse.ArgumentParser('Run retrosynthesis and pathways analysis pipeline to calculate heterologous pathways to produce a compound of interest in an organism of interest')
    parser.add_argument('-inchi', type=str)
    parser.add_argument('-organism', type=str, choices=['e_coli', 'b_subtilis', 's_cerevisiae', 'y_lipolytica', 'p_putida'])
    parser.add_argument('-num_steps', type=int, default=3)
    parser.add_argument('-output_folder', type=str, default='None')
    parser.add_argument('-topx', type=int, default=200)
    parser.add_argument('-timeout', type=float, default=240.0)
    parser.add_argument('-dont_merge', type=str, default='True')
    parser.add_argument('-num_workers', type=int, default=1)
    parser.add_argument('-pubchem_search', type=str, default='False')
    parser.add_argument('-partial_results', type=str, default='False')
    params = parser.parse_args()
    if params.dont_merge=='True' or params.dont_merge=='T' or params.dont_merge=='true' or params.dont_merge=='t':
        dont_merge = True
    elif params.dont_merge=='False' or params.dont_merge=='F' or params.dont_merge=='false' or params.dont_merge=='f':
        dont_merge = False
    else:
        logging.error('Cannot interpret dont_merge input: '+str(params.dont_merge))
        exit(1)
    if params.pubchem_search=='True' or params.pubchem_search=='T' or params.pubchem_search=='true' or params.pubchem_search=='t':
        pubchem_search = True
    elif params.pubchem_search=='False' or params.pubchem_search=='F' or params.pubchem_search=='false' or params.pubchem_search=='f':
        pubchem_search = False
    else:
        logging.error('Cannot interpret pubchem_search input: '+str(params.pubchem_search))
        exit(1)
    outfolder = None
    if params.partial_results=='True' or params.partial_results=='T' or params.partial_results=='true' or params.partial_results=='t':
        partial_results = True
    elif params.partial_results=='False' or params.partial_results=='F' or params.partial_results=='false' or params.partial_results=='f':
        partial_results = False
    else:
        logging.error('Cannot interpret partial_results input: '+str(params.partial_results))
        exit(1)
    if params.output_folder=='None':
        if not os.path.exists('rp2_full_analysis'):
            os.mkdir(os.path.join(os.path.abspath(os.getcwd()), 'rp2_full_analysis'))
        outfolder = os.path.join(os.path.abspath(os.getcwd()), 'rp2_full_analysis')
    else:
        if not os.path.exists(params.output_folder):
            os.mkdir(params.output_folder)
            outfolder = os.path.abspath(params.output_folder)
        outfolder = os.path.abspath(params.output_folder)
    ### run the algorithm ###
    if not os.path.exists(os.path.join(outfolder, 'rp_pathways.csv')):
        status = deep_rp2.deepRP('target',
                                 params.inchi,
                                 params.num_steps,
                                 params.organism,
                                 outfolder,
                                 params.timeout,
                                 partial_results)
        if status:
            logging.info('Deep RetroPath2 has succesfully found a solution finished')
        else:
            logging.info('Deep RetroPath2 could not find a solution')
            exit(1)
    else:
        logging.info('Already calculated the heterologous pathways using RetroPath2.0')
    #### run the pathway analysis pipeline ####
    status, error_type = analysis_pipeline.pathwayAnalysis(os.path.join(outfolder, 'rp_pathways.csv'),
                                                           os.path.join(outfolder, 'model.sbml'),
                                                           outfolder,
                                                           topx=params.topx,
                                                           timeout=params.timeout,
                                                           dont_merge=dont_merge,
                                                           num_workers=params.num_workers,
                                                           pubchem_search=pubchem_search)
    if status:
        logging.info('The pipeline successfully ran')
    else:
        logging.error('The pipeline failed at the following step: '+str(error_type))
