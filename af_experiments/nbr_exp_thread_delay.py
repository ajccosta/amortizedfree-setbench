# change following parameters only in define_experiment()
# RECLAIMER_ALGOS
# __trials
#  TOTAL_THREADS
# INS_DEL_HALF
#  DS_SIZE
##this script runs compiles, runs and then produces nice figures using Setbenches tool framework for DGT for thread delay experiment.

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

def my_plot_func(filename, column_filters, data, series_name, x_name, y_name, title, exp_dict=None):
    # print(data.head(20))
    data=data.groupby(['RECLAIMER_ALGOS', 'TOTAL_THREADS'])['maxresident_mb'].mean().reset_index()
    table = pandas.pivot_table(data, index=x_name, columns=series_name, values=y_name, aggfunc='mean')
    
    ax = table.plot(kind='line', title=title+' '+filename.rsplit('/',1)[1])
    ax.set_xlabel("num threads")
    ax.set_ylabel("maxresident mem (MB)")

    markers=['o', '+', 'x', '*', '.', 'X', 'h', 'D', 's', '^']

    if len(ax.get_lines()) >= len (markers):
        print ("number markers less than lines in my_plot_func")
    else:
        for i, line in enumerate(ax.get_lines()):
            line.set_marker(markers[i])
    
    plt.legend()
    # ax.set_prop_cycle(color=['red', 'green', 'blue', 'orange', 'cyan', 'brown', 'purple', 'pink', 'gray', 'olive'], marker=['o', '+', 'x', '*', '.', 'X', 'h', 'D', 's', '^'])
    mpl.pyplot.savefig(filename)
    print('## SAVED FIGURE {}'.format(filename))    

def define_experiment(exp_dict, args):
    set_dir_tools    (exp_dict, os.getcwd() + '/../tools') ## tools library for plotting
    set_dir_compile  (exp_dict, os.getcwd() + '/../microbench')     ## working dir for compiling
    set_dir_run      (exp_dict, os.getcwd() + '/../microbench/bin') ## working dir for running
    set_cmd_compile  (exp_dict, './compile.sh')

    fr = open("inputs/reclaimer.txt", "r")
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

    # fw = open("inputs/workloadtype.txt", "r")
    # worktype = fw.readline().split(',')
    # worktype = [int(i) for i in worktype]
    # fw.close()

    # fs = open("inputs/steps.txt", "r")
    # steps = fs.readline().split(',')
    # steps = [int(i) for i in steps]
    # fs.close() 

    fsz = open("inputs/treesize.txt", "r")
    dssize=fsz.readline().rstrip('\n') #remove new line
    dssize=dssize.split(',') # split
    dssize = [i.strip() for i in dssize] #remove white space
    dssize = [int(i) for i in dssize]
    fsz.close() 


    print("INPUTS:")
    print ("reclaimers=", reclaimers) 
    print("thread_list=", thread_list)
    print("workloadtype=", [50])
    print("steps=", [1])
    print("DGT size=", dssize)


    add_run_param (exp_dict, 'DS_ALGOS', ['guerraoui_ext_bst_ticket']) #or use herlihy_lazylist with 2000 ds size
    add_run_param (exp_dict, 'RECLAIMER_ALGOS', reclaimers) #['nbrplus_td', 'debra_td', 'none_td', 'ibr_td', 'qsbr_td', 'ibr_rcu_td', 'hazardptr_td']  ['nbrplus_td', 'debra_td']
    add_run_param (exp_dict, '__trials', [1]) #[1,2,3]


    add_run_param    (exp_dict, 'TOTAL_THREADS', thread_list) #[18, 36, 54, 72, 90, 108, 126, 144, 162, 180, 198, 216, 234, 252]
    add_run_param    (exp_dict, 'INS_DEL_HALF', [50])
    add_run_param    (exp_dict, 'DS_SIZE', dssize) #[2000000]  or [20000, 200000, 2000000]

    set_cmd_run      (exp_dict, 'LD_PRELOAD=../../lib/libjemalloc.so numactl --interleave=all time ./ubench_{DS_ALGOS}.alloc_new.reclaim_{RECLAIMER_ALGOS}.pool_none.out -nwork {TOTAL_THREADS} -nprefill 0 -i {INS_DEL_HALF} -d {INS_DEL_HALF} -rq 0 -rqsize 1 -k {DS_SIZE} -t 25000')

    # add_data_field   (exp_dict, 'total_throughput', coltype='INTEGER')
    # add_data_field   (exp_dict, 'maxresident_mb', coltype='REAL', extractor=get_maxres)
    # add_plot_set(exp_dict, name='mem_usage-{DS_ALGOS}-i{INS_DEL_HALF}-d{INS_DEL_HALF}.png', series='RECLAIMER_ALGOS', title='DGT Tree'
    #       , x_axis='TOTAL_THREADS'
    #       , y_axis='maxresident mem (GB)'
    #       , plot_type=my_plot_func
    #       , varying_cols_list=['INS_DEL_HALF']
    #       ,plot_cmd_args='--x_label threads --y_label throughput' )

    add_data_field   (exp_dict, 'total_throughput', coltype='INTEGER')
    add_data_field   (exp_dict, 'maxresident_mb', coltype='REAL', extractor=get_maxres)
    add_plot_set(exp_dict, name='mem_usage-{DS_ALGOS}-i{INS_DEL_HALF}-d{INS_DEL_HALF}.png', series='RECLAIMER_ALGOS', title='DGT Tree'
          , x_axis='TOTAL_THREADS'
          , y_axis='maxresident_mb'
          , plot_type=my_plot_func
          , varying_cols_list=['INS_DEL_HALF']
          ,plot_cmd_args='--x_label threads --y_label throughput' )


# import sys ; sys.path.append('../tools/data_framework') ; from run_experiment import *
# run_in_jupyter(define_experiment_dgt, cmdline_args='-dp')