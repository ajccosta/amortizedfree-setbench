# change following parameters only in define_experiment()
# RECLAIMER_ALGOS
# __trials
#  TOTAL_THREADS
# INS_DEL_HALF
#  DS_SIZE

###this script runs compiles, runs and then produces nice figures using Setbenches tool framework for ht

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
    data=data.groupby(['RECLAIMER_ALGOS', 'TOTAL_THREADS'])['total_throughput'].mean().reset_index()
    table = pandas.pivot_table(data, index=x_name, columns=series_name, values=y_name, aggfunc='mean')
    
    ax = table.plot(kind='line', title=title+' '+filename.rsplit('/',1)[1])
    ax.set_xlabel("num threads")
    ax.set_ylabel("throughput")

    markers=['o', '+', 'x', '*', '.', 'X', 'h', 'D', 's', '^', '1','p','v','>']

    if len(ax.get_lines()) >= len (markers):
        print ("number markers less than lines in my_plot_func")
    else:
        for i, line in enumerate(ax.get_lines()):
            line.set_marker(markers[i])
    
    plt.legend()
    plt.grid()
    # ax.set_prop_cycle(color=['red', 'green', 'blue', 'orange', 'cyan', 'brown', 'purple', 'pink', 'gray', 'olive'], marker=['o', '+', 'x', '*', '.', 'X', 'h', 'D', 's', '^'])
    mpl.pyplot.savefig(filename)
    print('## SAVED FIGURE {}'.format(filename))    

def my_memplot_func(filename, column_filters, data, series_name, x_name, y_name, title, exp_dict=None):
    # print(data.head(20))
    data=data.groupby(['RECLAIMER_ALGOS', 'TOTAL_THREADS'])['maxresident_mb'].mean().reset_index()
    table = pandas.pivot_table(data, index=x_name, columns=series_name, values=y_name, aggfunc='mean')
    
    ax = table.plot(kind='line', title=title)
    ax.set_xlabel("num threads")
    ax.set_ylabel("maxresident_mb")

    markers=['o', '+', 'x', '*', '.', 'X', 'h', 'D', 's', '^', '1','p','v','>']

    if len(ax.get_lines()) >= len (markers):
        print ("number markers less than lines in my_plot_func")
    else:
        for i, line in enumerate(ax.get_lines()):
            line.set_marker(markers[i])
    
    plt.legend()
    plt.grid()
    # ax.set_prop_cycle(color=['red', 'green', 'blue', 'orange', 'cyan', 'brown', 'purple', 'pink', 'gray', 'olive'], marker=['o', '+', 'x', '*', '.', 'X', 'h', 'D', 's', '^'])
    mpl.pyplot.savefig(filename)
    print('## SAVED FIGURE {}'.format(filename))    


def define_experiment(exp_dict, args):
    set_dir_tools    (exp_dict, os.getcwd() + '/../tools') ## tools library for plotting
    set_dir_compile  (exp_dict, os.getcwd() + '/../microbench')     ## working dir for compiling
    set_dir_run      (exp_dict, os.getcwd() + '/../microbench/bin') ## working dir for running
    set_cmd_compile  (exp_dict, './compile.sh')
    set_dir_data    ( exp_dict, os.getcwd() + '/data_abtree' )               ## directory for data files

    add_run_param (exp_dict, 'DS_ALGOS', ['brown_ext_abtree_lf'])
    add_run_param (exp_dict, 'RECLAIMER_ALGOS', ['nbr','nbrplus','nbr_orig','debra', 'none','2geibr','qsbr', 'ibr_rcu','he','ibr_hp','wfe']) #['nbr','nbrplus','nbr_orig','debra', 'none','2geibr','qsbr', 'ibr_rcu','he','ibr_hp','wfe'] #['nbrplus', 'debra', 'none', 'ibr', 'qsbr', 'ibr_rcu', 'hazardptr']
    add_run_param (exp_dict, '__trials', [1,2,3,4,5]) #[1,2,3]
    add_run_param     ( exp_dict, 'thread_pinning'  , ['-pin ' + shell_to_str('cd ' + get_dir_tools(exp_dict) + ' ; ./get_pinning_cluster.sh', exit_on_error=True)] )
    add_run_param    (exp_dict, 'TOTAL_THREADS', [1,2,4,8,16,32,48,72,96,120,144,168,192,216,240,264,512]) #[1,2,4,8,16,32,48,72,96,120,144,168,192,216,240,264,512]
    # add_run_param     ( exp_dict, 'TOTAL_THREADS'   , [1] + shell_to_listi('cd ' + get_dir_tools(exp_dict) + ' ; ./get_thread_counts_numa_nodes.sh', exit_on_error=True) )
    add_run_param    (exp_dict, 'INS_DEL_HALF', [0,25,50])#[0,25,50]
    add_run_param    (exp_dict, 'DS_SIZE', [200000, 2000000, 20000000]) #[200, 2000, 20000] [60000, 6000000]

    set_cmd_run      (exp_dict, 'LD_PRELOAD=../../lib/libjemalloc.so numactl --interleave=all time ./ubench_{DS_ALGOS}.alloc_new.reclaim_{RECLAIMER_ALGOS}.pool_none.out -nwork {TOTAL_THREADS} -nprefill {TOTAL_THREADS} -i {INS_DEL_HALF} -d {INS_DEL_HALF} -rq 0 -rqsize 1 -k {DS_SIZE} -t 5000 {thread_pinning}')

    add_data_field   (exp_dict, 'total_throughput', coltype='INTEGER')
    add_data_field   (exp_dict, 'maxresident_mb', coltype='REAL', extractor=get_maxres)
    add_plot_set(exp_dict, name='throughput-{DS_ALGOS}-u{INS_DEL_HALF}-sz{DS_SIZE}.png', series='RECLAIMER_ALGOS', title=''
          , x_axis='TOTAL_THREADS'
          , y_axis='total_throughput'
          , plot_type=my_plot_func
          , varying_cols_list=['INS_DEL_HALF','DS_SIZE']
          ,plot_cmd_args='--x_label threads --y_label throughput' )

    add_plot_set(
            exp_dict
          , name='maxresident-{DS_ALGOS}-u{INS_DEL_HALF}-k{DS_SIZE}.png'
          , series='RECLAIMER_ALGOS'
          , title='Max resident size (MB)'
        #   , filter=filter_string
          , varying_cols_list=['INS_DEL_HALF','DS_SIZE']
          , x_axis='TOTAL_THREADS'
          , y_axis='maxresident_mb'
          , plot_type=my_memplot_func
          , plot_cmd_args='--x_label threads --y_label throughput'
    )

# import sys ; sys.path.append('../tools/data_framework') ; from run_experiment import *
# run_in_jupyter(define_experiment_dgt, cmdline_args='-dp')