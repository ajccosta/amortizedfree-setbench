# change following parameters only in define_experiment()
# RECLAIMER_ALGOS
# __trials
#  TOTAL_THREADS
# INS_DEL_HALF
#  DS_SIZE

###this script runs compiles, runs and then produces nice figures using Setbenches tool framework.

import sys 
sys.path.append('../tools/data_framework')
from run_experiment import *

from _basic_functions import *
import pandas
import matplotlib as mpl

#extract max res size in MB
def get_maxres(exp_dict, file_name, field_name):
    ## manually parse the maximum resident size from the output of `time` and add it to the data file
    maxres_kb_str = shell_to_str('grep "maxres" {} | cut -d" " -f6 | cut -d"m" -f1'.format(file_name))
    return float(maxres_kb_str) / 1000

def get_algotype(exp_dict, file_name, field_name):
    ## manually parse the maximum resident size from the output of `time` and add it to the data file
    maxres_kb_str = shell_to_str('grep "type_algo" {} | cut -d":" -f2 | tr -d " "'.format(file_name))
    print(maxres_kb_str)

    return maxres_kb_str


def define_experiment(exp_dict, args):
    set_dir_tools    (exp_dict, os.getcwd() + '/../tools') ## tools library for plotting
    set_dir_compile  (exp_dict, os.getcwd() + '/../microbench')     ## working dir for compiling
    set_dir_run      (exp_dict, os.getcwd() + '/../microbench/bin') ## working dir for running
    set_cmd_compile  (exp_dict, './compile.sh')
    set_dir_data    ( exp_dict, os.getcwd() + '/data_exp2' )               ## directory for data files

    fr = open("inputs/reclaimer_exp2.txt", "r")
    reclaimers=fr.readline().rstrip('\n') #remove new line
    reclaimers=reclaimers.split(',') # split
    reclaimers = [i.strip() for i in reclaimers] #remove white space
    # reclaimers=fr.readline().split(',')
    fr.close()
    
    ft = open("inputs/threadsequence.txt", "r")
    thread_list=ft.readline().rstrip('\n') #remove new line
    thread_list=thread_list.split(',') # split
    thread_list = [i.strip() for i in thread_list] #remove white space
    thread_list = [int(i) for i in thread_list]
    ft.close()

    fw = open("inputs/workloadtype.txt", "r")
    worktype=fw.readline().rstrip('\n') #remove new line
    worktype=worktype.split(',') # split
    worktype = [i.strip() for i in worktype] #remove white space
    worktype = [int(i) for i in worktype]
    fw.close()

    fs = open("inputs/steps.txt", "r")
    steps=fs.readline().rstrip('\n') #remove new line
    steps=steps.split(',') # split
    steps = [i.strip() for i in steps] #remove white space
    steps = [int(i) for i in steps]
    fs.close()


    fsz = open("inputs/dssize.txt", "r")
    dssize=fsz.readline().rstrip('\n') #remove new line
    dssize=dssize.split(',') # split
    dssize = [i.strip() for i in dssize] #remove white space
    dssize = [int(i) for i in dssize]
    fsz.close() 


    print("INPUTS:")
    print ("reclaimers=", reclaimers) 
    print("thread_list=", thread_list)
    print("workloadtype=", worktype)
    print("steps=", steps)
    print("DGT size=", dssize)

    add_run_param (exp_dict, 'DS_ALGOS', ['brown_ext_abtree_lf', 'guerraoui_ext_bst_ticket'])
    add_run_param (exp_dict, 'RECLAIMER_ALGOS', reclaimers)
    # ['debra', 'debra_df', 'nbrplus', 'nbrplus_df', 'nbr', 'nbr_df', 'ibr_rcu', 'ibr_rcu_df', 'qsbr', 'qsbr_df', '2geibr', '2geibr_df', 'ibr_hp', 'ibr_hp_df', 'he', 'he_df', 'wfe', 'wfe_df', 'token1', 'token4']
    # ['debra', 'debra_df', 'nbrplus', 'nbrplus_df', 'nbr', 'nbr_df', 'token1', 'token4']

    add_run_param (exp_dict, '__trials', steps) #[1,2,3]
    add_run_param     ( exp_dict, 'thread_pinning'  , ['-pin ' + shell_to_str('cd ' + get_dir_tools(exp_dict) + ' ; ./get_pinning_cluster.sh', exit_on_error=True)] )
    add_run_param    (exp_dict, 'TOTAL_THREADS', thread_list) #WARNING: give only single thread 
    #[1,2,4,8,16,32,48,72,96,120,144,168,192,216,240,264,512]
    # add_run_param     ( exp_dict, 'TOTAL_THREADS'   , [1] + shell_to_listi('cd ' + get_dir_tools(exp_dict) + ' ; ./get_thread_counts_numa_nodes.sh', exit_on_error=True) )
    add_run_param    (exp_dict, 'INS_DEL_HALF', worktype)#[0,25,50]
    add_run_param    (exp_dict, 'DS_SIZE', dssize) #[200, 2000, 20000] [60000, 6000000]

    set_cmd_run      (exp_dict, 'LD_PRELOAD=../../lib/libjemalloc.so numactl --interleave=all time ./ubench_{DS_ALGOS}.alloc_new.reclaim_{RECLAIMER_ALGOS}.pool_none.out -nwork {TOTAL_THREADS} -nprefill {TOTAL_THREADS} -i {INS_DEL_HALF} -d {INS_DEL_HALF} -rq 0 -rqsize 1 -k {DS_SIZE} -t 5000') #removed thread pinning.

    add_data_field   (exp_dict, 'total_throughput', coltype='INTEGER')
    add_data_field   (exp_dict, 'type_algo', coltype='TEXT', extractor=get_algotype)
    add_data_field   (exp_dict, 'maxresident_mb', coltype='REAL', extractor=get_maxres)
    add_plot_set(exp_dict, name='throughput-{DS_ALGOS}-u{INS_DEL_HALF}-sz{DS_SIZE}.png', series='type_algo', title='Throughput Original vs AF implementations'
          , x_axis='RECLAIMER_ALGOS'
          , y_axis='total_throughput'
          , plot_type='bars'
          ,plot_cmd_args='--legend-include --x-title "Reclaimer" --y-title "Throughput (ops/sec)"' )
    
    add_plot_set(exp_dict, name='memusage-{DS_ALGOS}-u{INS_DEL_HALF}-sz{DS_SIZE}.png', series='type_algo', title='MemUsage Original vs AF implementations'
          , x_axis='RECLAIMER_ALGOS'
          , y_axis='maxresident_mb'
          , plot_type='bars'
          ,plot_cmd_args='--legend-include --x-title "Reclaimer" --y-title "Memory Usage (MB)"' )
