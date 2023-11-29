#!/bin/bash
##this script quickly compiles and runs all the tests.  

echo " "
echo "############################################"
echo "Compiling benchmark..."
echo "############################################"

python3 ../tools/data_framework/run_experiment.py exp1_run_tree.py -c

echo " "
echo "############################################"
echo "Running Quick Tests... for  throughput and peak memory usage."
echo "############################################"

echo " "
echo "############################################"
echo "Running Quick Tests... for  Figure 11a."
echo "############################################"

data_dir="data_exp1"
exp_file=exp1_run_tree.py
python3 ../tools/data_framework/run_experiment.py $exp_file -tr


echo " "
echo "############################################"
echo "Running Quick Tests... for  Figure 11b."
echo "############################################"

data_dir="data_exp2"
exp_file=exp2_run_tree.py
python3 ../tools/data_framework/run_experiment.py $exp_file -tr

echo " "
echo "############################################"
echo "Running Quick Tests... for  Figure 1."
echo "############################################"
data_dir="data_fig1"
exp_file=fig1_run.py
python3 ../tools/data_framework/run_experiment.py $exp_file -tr

echo " "
echo "############################################"
echo "Running Quick Tests... for  Figure 10."
echo "############################################"
data_dir="data_fig10"
exp_file=fig10_run.py
python3 ../tools/data_framework/run_experiment.py $exp_file -tr