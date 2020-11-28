import deep_rp2
import os
import json
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')




strains = ['e_coli', 'b_subtilis', 's_cerevisiae', 'y_lipolytica', 'p_putida']
in_max_steps = 6
in_min_steps = 1

laser_compounds = json.load(open('laser_targets_20190726.json', 'r'))

if not os.path.exists('laser_compounds_run'):
    os.mkdir('laser_compounds_run')

for lc in laser_compounds:
    path = os.path.join('laser_compounds_run', str(lc.replace('/', ''))+'_'+laser_compounds[lc]['name'].replace('/', ''))
    if not os.path.exists(path):
        os.mkdir(path)
    for s in strains:
        path_s = os.path.join(path, s)
        if not os.path.exists(path_s):
            os.mkdir(path_s)
        if os.path.exists(os.path.join(path_s, 'rp_pathways.csv')):
            logging.warning('Already have results for '+str(laser_compounds[lc]['name'])+' with strain '+str(s))
            continue
        deep_rp2.deepRP(laser_compounds[lc]['name'], laser_compounds[lc]['inchi'], in_max_steps, in_min_steps, s, path_s)
        
