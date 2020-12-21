import deep_rp2
import run_rp2paths
import os
import json
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

results_path = os.path.join('/mnt/hdd/mdulac/', 'laser_compounds_run')


strains = ['e_coli', 'b_subtilis', 's_cerevisiae', 'y_lipolytica', 'p_putida']
in_max_steps = 6
in_min_steps = 1

laser_compounds = json.load(open('laser_targets_20190726.json', 'r'))

if not os.path.exists(results_path):
    os.mkdir(results_path)

for lc in laser_compounds:
    path = os.path.join(results_path, str(lc.replace('/', ''))+'_'+laser_compounds[lc]['name'].replace('/', '').replace(')', '').replace('(', '').replace(',', '-').replace('+', '_').replace(' ', '_').replace('"', '').replace("'", "")).replace('<', '').replace('>', '')
    if not os.path.exists(path):
        os.mkdir(path)
    for s in strains:
        path_strain = os.path.join(path, s)
        if not os.path.exists(path_strain):
            os.mkdir(path_strain)
        if os.path.exists(os.path.join(path_strain, 'rp2_report.txt')):
            logging.warning('Already have results for '+str(laser_compounds[lc]['name'])+' with strain '+str(s))
        else:
            deep_rp2.deepRP(laser_compounds[lc]['name'], laser_compounds[lc]['inchi'], in_max_steps, in_min_steps, s, path_strain)
        ##########################################################
        ################# rp2paths ###############################
        ##########################################################
        rp2_pathways = os.path.join(path_strain, 'rp_pathways.csv')
        if not os.path.exists(rp2_pathways):
            logging.warning('There are no rp2_pathways output')
        else:
            logging.info('#################### rp2paths  ######################')
            rp2paths_compounds = os.path.join(path_strain, 'rp2paths_compounds.csv')
            rp2paths_pathways = os.path.join(path_strain, 'rp2paths_pathways.csv')
            if not os.path.exists(rp2paths_compounds) and not os.path.exists(rp2paths_pathways):
                run_rp2paths.main(rp2_pathways, rp2paths_pathways, rp2paths_compounds)
            if not os.path.exists(rp2paths_compounds) or not os.path.exists(rp2paths_pathways):
                logging.error('rp2paths did not generate files')
