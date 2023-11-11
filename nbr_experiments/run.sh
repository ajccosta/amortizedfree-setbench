#!/bin/sh
##this script runs compiles, runs and then produces nice figures using Setbenches tool framework for DGT and lazylist.  

echo " "
echo "############################################"
echo "Compiling benchmark..."
echo "############################################"

# python3 ../tools/data_framework/run_experiment.py nbr_exp_run_list.py -c

# export PATH=$PATH:.
# `chmod +x get_lscpu_numa_nodes.sh`
# `get_lscpu_numa_nodes.sh | awk '{row[NR]=(NR > 1 ? row[NR-1] : 0)+NF} END { row[NR]-=2 ; row[NR+1]=row[1]/2 ; for (i in row) print row[i] }' | sort -n > numa_thread_count.txt`


# data_dir="data_ll"
# exp_file=nbr_exp_run_ll.py
# echo "############################################"
# echo "Executing and generating FIGURES for LL..."
# echo "############################################"
# python3 ../tools/data_framework/run_experiment.py $exp_file -rdp

# # echo "copying FIGURES to plots/expected_plots/ "
# # cp data/*.png plots/expected_plots/
# mkdir plots/plot_$data_dir
# echo "copying FIGURES to plots/plot_$data_dir/ "
# cp $data_dir/*.png plots/plot_$data_dir/


# data_dir="data_hl"
# exp_file=nbr_exp_run_hl.py
# echo "############################################"
# echo "Executing and generating FIGURES for HL..."
# echo "############################################"

# python3 ../tools/data_framework/run_experiment.py $exp_file -rdp

# # echo "copying FIGURES to plots/expected_plots/ "
# # cp data/*.png plots/expected_plots/
# mkdir plots/plot_$data_dir
# echo "copying FIGURES to plots/plot_$data_dir/ "
# cp $data_dir/*.png plots/plot_$data_dir/


# data_dir="data_hm"
# exp_file=nbr_exp_run_hm.py
# echo "############################################"
# echo "Executing and generating FIGURES for HM..."
# echo "############################################"

# python3 ../tools/data_framework/run_experiment.py $exp_file -rdp

# # echo "copying FIGURES to plots/expected_plots/ "
# # cp data/*.png plots/expected_plots/
# mkdir plots/plot_$data_dir
# echo "copying FIGURES to plots/plot_$data_dir/ "
# cp $data_dir/*.png plots/plot_$data_dir/

# data_dir="data_hmht"
# exp_file=nbr_exp_run_hmht.py
# echo "############################################"
# echo "Executing and generating FIGURES for HMHT..."
# echo "############################################"

# python3 ../tools/data_framework/run_experiment.py $exp_file -dp

# # echo "copying FIGURES to plots/expected_plots/ "
# # cp data/*.png plots/expected_plots/
# mkdir plots/plot_$data_dir
# echo "copying FIGURES to plots/plot_$data_dir/ "
# cp $data_dir/*.png plots/plot_$data_dir/


# data_dir="data_dgt"
# exp_file=nbr_exp_run_dgt.py
# echo "############################################"
# echo "Executing and generating FIGURES for DGT..."
# echo "############################################"

# python3 ../tools/data_framework/run_experiment.py $exp_file -dp

# # echo "copying FIGURES to plots/expected_plots/ "
# # cp data/*.png plots/expected_plots/
# mkdir plots/plot_$data_dir
# echo "copying FIGURES to plots/plot_$data_dir/ "
# cp $data_dir/*.png plots/plot_$data_dir/

# data_dir="data_abt"
# exp_file=nbr_exp_run_abt.py
# echo "############################################"
# echo "Executing and generating FIGURES for ABT..."
# echo "############################################"

# python3 ../tools/data_framework/run_experiment.py $exp_file -dp

# # echo "copying FIGURES to plots/expected_plots/ "
# # cp data/*.png plots/expected_plots/
# mkdir plots/plot_$data_dir
# echo "copying FIGURES to plots/plot_$data_dir/ "
# cp $data_dir/*.png plots/plot_$data_dir/

data_dir="data_dgttd"
exp_file=nbr_exp_run_dgttd.py
echo "############################################"
echo "Executing and generating FIGURES for DGT..."
echo "############################################"

python3 ../tools/data_framework/run_experiment.py $exp_file -rdp

# echo "copying FIGURES to plots/expected_plots/ "
# cp data/*.png plots/expected_plots/
mkdir plots/plot_$data_dir
echo "copying FIGURES to plots/plot_$data_dir/ "
cp $data_dir/*.png plots/plot_$data_dir/

# data_dir="data_dgtntd"
# exp_file=nbr_exp_run_dgtntd.py
# echo "############################################"
# echo "Executing and generating FIGURES for DGT..."
# echo "############################################"

# python3 ../tools/data_framework/run_experiment.py $exp_file -p

# # echo "copying FIGURES to plots/expected_plots/ "
# # cp data/*.png plots/expected_plots/
# mkdir plots/plot_$data_dir
# echo "copying FIGURES to plots/plot_$data_dir/ "
# cp $data_dir/*.png plots/plot_$data_dir/