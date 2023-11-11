#!/bin/sh
##this script runs compiles, runs and then produces nice figures using Setbenches tool framework for DGT for mem usage (thread delay) experiment.  


data_dir="data_dgt"
exp_file=nbr_exp_run_dgttd_nodebra.py
echo "############################################"
echo "Executing and generating FIGURES for DGT..."
echo "############################################"

python3 ../tools/data_framework/run_experiment.py $exp_file -dp

# echo "copying FIGURES to plots/expected_plots/ "
# cp data/*.png plots/expected_plots/
mkdir plots/plot_$data_dir
echo "copying FIGURES to plots/plot_$data_dir/ "
cp $data_dir/*.png plots/plot_$data_dir/