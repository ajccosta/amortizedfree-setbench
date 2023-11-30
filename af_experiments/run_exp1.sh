#!/bin/sh
##this script runs compiles, runs and then produces nice figures using Setbenches tool framework for DGT and lazylist.  

data_dir="data_exp1"
exp_file=exp1_run_tree.py

# echo " "
# echo "############################################"
# echo "Compiling benchmark..."
# echo "############################################"

# python3 ../tools/data_framework/run_experiment.py $exp_file -c

# export PATH=$PATH:.
# `chmod +x get_lscpu_numa_nodes.sh`
# `get_lscpu_numa_nodes.sh | awk '{row[NR]=(NR > 1 ? row[NR-1] : 0)+NF} END { row[NR]-=2 ; row[NR+1]=row[1]/2 ; for (i in row) print row[i] }' | sort -n > numa_thread_count.txt`

# echo "############################################"
# echo "Executing and generating FIGURES for Tree..."
# echo "############################################"

python3 ../tools/data_framework/run_experiment.py $exp_file -rdp #-tr

# echo "copying FIGURES to plots/expected_plots/ "
# cp data/*.png plots/expected_plots/
mkdir plots/plot_$data_dir
echo "copying FIGURES to plots/plot_$data_dir/ "
cp $data_dir/*.png plots/plot_$data_dir/

