#!/bin/bash

# python3 ../tools/data_framework/run_experiment.py fig10_run.py -crdp


data_dir="data_fig10"
exp_file=fig10_run.py

python3 ../tools/data_framework/run_experiment.py $exp_file -crdp #-tr

# echo "copying FIGURES to plots/expected_plots/ "
# cp data/*.png plots/expected_plots/
mkdir plots/plot_$data_dir
echo "copying FIGURES to plots/plot_$data_dir/ "
cp $data_dir/*.png plots/plot_$data_dir/
