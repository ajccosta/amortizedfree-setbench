#!/bin/bash

cd af_experiments
bash clean.sh
bash run_exp1.sh
bash run_exp2.sh
bash run_fig1.sh
bash run_fig10.sh

cd ../ebrtimelines/microbench/experiments/timelines; bash clean.sh; cd debra
bash run_bf_threads.sh
rm -rf data
bash run_bf_vs_af.sh
cd ../tokens
bash run.sh