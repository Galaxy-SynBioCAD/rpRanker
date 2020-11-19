import logging
import tempfile
import os
import shutil
import csv
import argparse

import run_retropath2
import run_rpextractsink
import run_retrorules

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


## Perform multiple retropath2.0 runs to find the best possible solution
#
#
def deepRP(target_name,
           target_inchi,
           in_max_steps,
           in_min_steps,
           strain,
           path_to_res,
           in_min_steps=3,
           timeout=240.0,
           range_topx=[1000, 500, 100],
           range_rule_diameters=['2,4,6,8,10,12,14,16', '6,10,16']):
    if strain=='e_coli':
        range_gem_sbml = ['models/e_coli_iML1515.sbml',
                          'models/e_coli_iJO1366.sbml',
                          'models/e_coli_iAF1260.sbml',
                          'models/e_coli_iJR904.sbml',
                          'models/e_coli_core_model.sbml']
    elif strain=='b_subtilis':
        range_gem_sbml = ['models/b_subtilis_iYO844.sbml']
    elif strain=='s_cerevisiae':
        range_gem_sbml = ['models/s_cerevisiae_iMM904.sbml',
                          'models/s_cerevisiae_iND750.sbml']
    elif strain=='y_lipolytica':
        range_gem_sbml = ['models/y_lipolytica_iMK735.sbml'] 
    elif strain=='p_putida':
        range_gem_sbml = ['models/p_putida_iJN746.sbml']
    else:
        logging.error('Cannot detect the string input: '+str(strain))
        return False, 0
    failed_models = []
    for is_partial in [False, True]:
        for gem_sbml in range_gem_sbml:
            for rule_diameters in range_rule_diameters:
                for topx in range_topx:
                    for max_steps in reversed(range(in_min_steps, in_max_steps+1)):
                        logging.info('####################################################')
                        logging.info('Trying to predict heterologous pathways for '+str(target_name)+' in '+str(strain))
                        logging.info('Running the following conditions: ')
                        logging.info('GEM SBML: '+str(gem_sbml))
                        logging.info('TopX: '+str(topx))
                        logging.info('Max Steps: '+(max_steps))
                        logging.info('Rule Diameters: '+str(rule_diameters))
                        with tempfile.TemporaryDirectory() as tmpOutputFolder:
                            if gem_sbml in failed_models:
                                logging.error('Alrready tried this model and it failed, skipping the model: '+str(failed_models))
                                continue
                            ##########################################################
                            ################### Source File ##########################
                            ##########################################################
                            logging.info('#################### Source File  ######################')
                            sourcefile = os.path.join(tmpOutputFolder, 'source.csv')
                            with open(sourcefile, 'w') as csvfile:
                                filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                filewriter.writerow(['Name', 'InChI'])
                                filewriter.writerow([target_name, target_inchi])
                            ##########################################################
                            ################### Sink File ############################
                            ##########################################################
                            logging.info('#################### Sink File  ######################')
                            sinkfile = os.path.join(tmpOutputFolder, 'sinkfile.csv')
                            run_rpextractsink.main(gem_sbml, sinkfile)
                            ##########################################################
                            ################### RetroRules ###########################
                            ##########################################################
                            logging.info('#################### RetroRules ######################')
                            retrorules_file = os.path.join(tmpOutputFolder, 'rules.tar')
                            run_retrorules.main(retrorules_file, diameters=rule_diameters)
                            ##########################################################
                            ################### RetroPath2 ###########################
                            ##########################################################
                            logging.info('#################### RetroPath2 ######################')
                            rp_pathways = os.path.join(tmpOutputFolder, 'rp_pathways.csv')
                            err_str = run_retropath2.main(sinkfile, sourcefile, max_steps, retrorules_file, 'tar', rp_pathways, topx=topx, timeout=int(timeout), partial_retro=is_partial)
                            if err_str:
                                if 'Source has been found in the sink' in err_str:
                                    failed_models.append(gem_sbml)
                                #we assume that if you cannot find a solution with a given model then you pass to the next one
                                if 'RetroPath2.0 has not found any results' in err_str:
                                    failed_models.append(gem_sbml)
                            logging.info(err_str)
                            if os.path.exists(rp_pathways):
                                shutil.copy(sourcefile, os.path.join(path_to_res, 'source.csv'))                    
                                shutil.copy(sinkfile, os.path.join(path_to_res, 'sinkfile.csv'))                    
                                shutil.copy(retrorules_file, os.path.join(path_to_res, 'rules.tar'))                    
                                shutil.copy(rp_pathways, os.path.join(path_to_res, 'rp_pathways.csv'))                    
                                shutil.copy(gem_sbml, os.path.join(path_to_res, 'model.sbml'))                    
                                with open(os.path.join(path_to_res, 'rp2_report.txt'), 'w') as rp2_report:
                                    rp2_report.write('Molecule Name: '+str(target_name)+'\n')
                                    rp2_report.write('Molecule InChI: '+str(target_inchi)+'\n')
                                    rp2_report.write('GEM SBML: '+str(gem_sbml.split('/')[-1])+'\n')
                                    rp2_report.write('TopX: '+str(topx)+'\n')
                                    rp2_report.write('Max Steps: '+str(max_steps)+'\n')
                                    rp2_report.write('Rule Diameters: '+str(rule_diameters)+'\n')
                                    rp2_report.write('Used Partial Results?: '+str(is_partial)+'\n')
                                return True, max_steps   
                            logging.info('####################################################')
    with open(os.path.join(path_to_res, 'rp2_report.txt'), 'w') as rp2_report:
        rp2_report.write('Molecule Name: '+str(target_name)+'\n')
        rp2_report.write('Molecule InChI: '+str(target_inchi)+'\n')
        rp2_report.write('Max Steps: '+str(max_steps)+'\n')
        rp2_report.write('Host Organism: '+str(strain)+'\n')
        rp2_report.write('No Solutions\n')
    return False, 0


if __name__=="__main__":
    parser = argparse.ArgumentParser('Perform deep retrosynthesis given a list of organisms')
    parser.add_argument('-inchi', type=str)
    parser.add_argument('-organism', type=str, choices=['e_coli', 'b_subtilis', 's_cerevisiae', 'y_lipolytica', 'p_putida'])
    parser.add_argument('-max_num_steps', type=int, default=10)
    parser.add_argument('-min_num_steps', type=int, default=3)
    parser.add_argument('-output_folder', type=str, default='None')
    parser.add_argument('-timeout', type=float, default=240.0)
    params = parser.parse_args()
    #TODO: check that the inchi is valid
    if params.max_num_steps<params.min_num_steps:
        logging.error('min_num_steps ('+str(params.min_num_steps)+') cannot be larger than max_num_steps ('+str(params.max_num_steps)+')')
        exit(1)
    outfolder = None
    if params.output_folder=='None':
        if not os.path.exists('rp2_results'):
            os.mkdir(os.path.join(os.path.abspath(os.getcwd()), 'rp2_results'))
            outfolder = os.path.join(os.path.abspath(os.getcwd()), 'rp2_results')
        else:
            logging.error('The rp2_results folder already exists, please delete it or point to another folder location')
            exit(1)
    else:
        if not os.path.exists(params.output_folder):
            os.mkdir(params.output_folder)
            outfolder = params.output_folder
        else:
            logging.error('The path: '+str(params.output_folder)+' already exists, please delete or input a different path')
            exit(1)
    ### run the algorithm ###
    status, max_steps = deepRP('target',
                               params.inchi,
                               params.max_num_steps,
                               params.min_num_steps,
                               params.organism,
                               outfolder,
                               params.timeout)
    if status:
        logging.info('Deep RetroPath2 ran succesfully')
    else:
        logging.info('Deep RetroPath2 could not find a solution')
