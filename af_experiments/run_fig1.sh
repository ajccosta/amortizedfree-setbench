#!/bin/bash

# python3 ../tools/data_framework/run_experiment.py fig1_run.py -crdp

data_dir="data_fig1"
exp_file=fig1_run.py

python3 ../tools/data_framework/run_experiment.py $exp_file -crdp #-tr

# echo "copying FIGURES to plots/expected_plots/ "
# cp data/*.png plots/expected_plots/
mkdir ../plots/generated_plots/plot_Fig1
echo "copying FIGURES to plots/generated_plots/plot_Fig1/ "
cp $data_dir/*.png ../plots/generated_plots/plot_Fig1/
