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
    res = int(float(maxres_kb_str) / 1000)
    print(res)
    return res

# run param = DS_ALGOS. values={brown_ext_abtree_lf, guerraoui_ext_bst_ticket}

# run param = RECLAIMER_ALGOS. values=['nbr','nbrplus','debra','debra_df', 'token4', 'none','2geibr','qsbr', 'ibr_rcu','he','ibr_hp','wfe']
# token4 is code name of token based ebr with amortizing enabled.
# token1 is naive token based ebr algorithm.
# 2geibr is ibr algorithm
# algos with _df suffix are amortized freeing versions of original algorithms. For eg. debra_df is the amortized freeing version of debra.

# run param = __trials. Number of trails eac experiment needs to be averaged over.
# run param = TOTAL_THREADS. values = [24,48,72,96,120,144,168,192,240]

# run param = INS_DEL_HALF. values = [25, 50].
# For eg 50 mins 50%inserts and 50% deletes. 25 means 25% inserts and 25% deletes and rest is contains.

# run param = DS_SIZE. values [200, 2000, 20000]
def define_experiment(exp_dict, args):
    set_dir_tools    (exp_dict, os.getcwd() + '/../tools') ## tools library for plotting
    set_dir_compile  (exp_dict, os.getcwd() + '/../microbench')     ## working dir for compiling
    set_dir_run      (exp_dict, os.getcwd() + '/../microbench/bin') ## working dir for running
    set_cmd_compile  (exp_dict, './compile.sh')
    set_dir_data    ( exp_dict, os.getcwd() + '/data_exp1' )               ## directory for data files

    # fr = open("inputs/reclaimer_exp1.txt", "r")
    # reclaimers=fr.readline().rstrip('\n') #remove new line
    # reclaimers=reclaimers.split(',') # split
    # reclaimers = [i.strip() for i in reclaimers] #remove white space
    # # reclaimers=fr.readline().split(',')
    # fr.close()
    
    # ft = open("inputs/threadsequence.txt", "r")
    # thread_list=ft.readline().rstrip('\n') #remove new line
    # thread_list=thread_list.split(',') # split
    # thread_list = [i.strip() for i in thread_list] #remove white space
    # thread_list = [int(i) for i in thread_list]
    # ft.close()

    # fw = open("inputs/workloadtype.txt", "r")
    # worktype=fw.readline().rstrip('\n') #remove new line
    # worktype=worktype.split(',') # split
    # worktype = [i.strip() for i in worktype] #remove white space
    # worktype = [int(i) for i in worktype]
    # fw.close()

    # fs = open("inputs/steps.txt", "r")
    # steps=fs.readline().rstrip('\n') #remove new line
    # steps=steps.split(',') # split
    # steps = [i.strip() for i in steps] #remove white space
    # steps = [int(i) for i in steps]
    # fs.close()


    # fsz = open("inputs/dssize.txt", "r")
    # dssize=fsz.readline().rstrip('\n') #remove new line
    # dssize=dssize.split(',') # split
    # dssize = [i.strip() for i in dssize] #remove white space
    # dssize = [int(i) for i in dssize]
    # fsz.close() 

    # fn = open("inputs/dsname.txt", "r")
    # dsname=fn.readline().rstrip('\n') #remove new line
    # dsname=dsname.split(',') # split
    # dsname = [i.strip() for i in dsname] #remove white space
    # fn.close() 

    # print("INPUTS:")
    # print ("reclaimers=", reclaimers) 
    # print("thread_list=", thread_list)
    # print("workloadtype=", worktype)
    # print("steps=", steps)
    # print("DS size=", dssize)
    # print("DS name=", dsname)

    add_run_param (exp_dict, 'DS_ALGOS', ['brown_ext_abtree_lf']) #['brown_ext_abtree_lf', 'guerraoui_ext_bst_ticket']
    add_run_param (exp_dict, 'RECLAIMER_ALGOS', ['nbr','nbrplus','debra','debra_df', 'token4', 'none','2geibr','qsbr', 'ibr_rcu','he','ibr_hp','wfe']) 
    # ['nbr','nbrplus','debra','debra_df', 'token4', 'none','2geibr','qsbr', 'ibr_rcu','he','ibr_hp','wfe']
 
    add_run_param (exp_dict, '__trials', [1]) #[1,2,3]
    add_run_param     ( exp_dict, 'thread_pinning'  , ['-pin ' + shell_to_str('cd ' + get_dir_tools(exp_dict) + ' ; ./get_pinning_cluster.sh', exit_on_error=True)] )
    add_run_param    (exp_dict, 'TOTAL_THREADS', [24,48,72,96,120,144,168,192,240]) 
    # [24,48,72,96,120,144,168,192,240]
    # [1,2,4,8,16,32,48,72,96,120,144,168,192,216,240,264,512]
    # add_run_param     ( exp_dict, 'TOTAL_THREADS'   , [1] + shell_to_listi('cd ' + get_dir_tools(exp_dict) + ' ; ./get_thread_counts_numa_nodes.sh', exit_on_error=True) )
    add_run_param    (exp_dict, 'INS_DEL_HALF', [50])#[0,25,50]
    add_run_param    (exp_dict, 'DS_SIZE', [20000000]) #[200, 2000, 20000] [60000, 6000000]

    if args.testing:
        add_run_param     ( exp_dict, 'DS_ALGOS', ['brown_ext_abtree_lf'] )
        add_run_param ( exp_dict, '__trials'        , [1])
        add_run_param ( exp_dict, 'TOTAL_THREADS'   , [24])
        add_run_param     (exp_dict, 'RECLAIMER_ALGOS', ['debra', 'token4'])


    if args.testing:
        set_cmd_run      (exp_dict, 'LD_PRELOAD=../../lib/libjemalloc.so numactl --interleave=all time ./ubench_{DS_ALGOS}.alloc_new.reclaim_{RECLAIMER_ALGOS}.pool_none.out -nwork {TOTAL_THREADS} -nprefill {TOTAL_THREADS} -i {INS_DEL_HALF} -d {INS_DEL_HALF} -rq 0 -rqsize 1 -k {DS_SIZE} -t 5000') #removed thread pinning.
    else:
        set_cmd_run      (exp_dict, 'LD_PRELOAD=../../lib/libjemalloc.so numactl --interleave=all time ./ubench_{DS_ALGOS}.alloc_new.reclaim_{RECLAIMER_ALGOS}.pool_none.out -nwork {TOTAL_THREADS} -nprefill {TOTAL_THREADS} -i {INS_DEL_HALF} -d {INS_DEL_HALF} -rq 0 -rqsize 1 -k {DS_SIZE} -t 5000') #removed thread pinning.


    # set_cmd_run      (exp_dict, 'LD_PRELOAD=../../lib/libjemalloc.so numactl --interleave=all time ./ubench_{DS_ALGOS}.alloc_new.reclaim_{RECLAIMER_ALGOS}.pool_none.out -nwork {TOTAL_THREADS} -nprefill {TOTAL_THREADS} -i {INS_DEL_HALF} -d {INS_DEL_HALF} -rq 0 -rqsize 1 -k {DS_SIZE} -t 5000') #removed thread pinning.

    add_data_field   (exp_dict, 'total_throughput', coltype='INTEGER')
    add_data_field   (exp_dict, 'maxresident_mb', coltype='REAL', extractor=get_maxres)
    add_plot_set(exp_dict, name='throughput-{DS_ALGOS}-u{INS_DEL_HALF}-sz{DS_SIZE}.png', series='RECLAIMER_ALGOS', title=''
          , x_axis='TOTAL_THREADS'
          , y_axis='total_throughput'
          , plot_type='line'
          , varying_cols_list=['DS_ALGOS','DS_SIZE']
          ,plot_cmd_args='--x_label threads --y_label "throughput(ops/sec)"' )

    add_plot_set(exp_dict, name='maxresident-{DS_ALGOS}-u{INS_DEL_HALF}-sz{DS_SIZE}.png', series='RECLAIMER_ALGOS', title=''
          , x_axis='TOTAL_THREADS'
          , y_axis='maxresident_mb'
          , plot_type='line'
          , varying_cols_list=['DS_ALGOS','DS_SIZE']
          , plot_cmd_args='--x_label threads --y_label "maxresident(mb)"' )
    