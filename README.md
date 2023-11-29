This repo contains the code and experiment setup used to evaluate the amortized freeing and token EBR algorithm presented in PPOPP23 paper titled: "Are Your Epochs Too Epic? Batch Free Can Be Harmful".

The experiments we run for the paper are of two kinds:
1. [TYPE1] Performance and peak memory usage experiments.
          - These experiements are run from directory: amortizedfree-setbench/af_experiments
2. [TYPE2] Timeline graph experiments
          - These experiments are run from directory: amortizedfree-setbench/microbench/experiments/timelines/

#CREDITS:
This repo builds upon the  nbr_setbench_plus project used for neutralization based reclamation techniques, which in turn used the original [setbench](https://gitlab.com/trbot86/setbench) of [Multicore Lab](https://mc.uwaterloo.ca/) headed by Prof. Trevor Brown to test and evaluate lockfree data structures and reclamation algorithms.


# 🏁 Getting Started

These instructions will get you a copy of the artifact up and running on your machine for development and testing purposes. This can be done in two ways: 1) use our docker provided image or 2) alternatively prepare your machine to run our artifact.

## Running on Docker
* Install the latest version of Docker on your system. We tested the artifact with the Docker version 19.03.6, build 369ce74a3c. Instructions to install Docker may be found at https://docs.docker.com/engine/install/ubuntu/. Or you may refer to the "Installing Docker" section at the end of this README.

  To check the version of docker on your machine use: 

    ``` ~$ docker -v```
* First, download the artifact named amortizedfree-setbench.zip from the ppopp2023 artifact submission link.

* Find docker image named amortizedfree_docker.tar.gz in amortizedfree-setbench/ directory. 
  And load the downloaded docker image with the following command.

    ```~$ sudo docker load -i amortizedfree_docker.tar.gz ```
* Verify that image was loaded.

    ```~$ sudo docker images```
* start a docker container from the loaded image

    ```~$ sudo docker run --name amortizedfree -it --privileged amortizedfree-setbench /bin/bash ```
* run ls to see several files/folders of the artifact: Dockerfile README.md, common, ds, install.sh, lib, microbench, af_experiments, tools. 

    ```~$ ls ```
If this succeeds you can move to the quick test section and skip the following section which discusses alternative ways to prepare your machine to run the artifact.

## *Alternative Way:* Preparing Host Machine:
In case you may want to prepare the host machine itself to run the artifact locally follow these instructions.

First, download the artifact named amortizedfree-setbench.zip from ppopp2023 artifact submission link.

The artifact requires the following packages/softwares on your Linux machine to compile and run the artifact.

```
 Use your system's package manager to install:
 > build-essential dos2unix g++ libnuma-dev make numactl parallel python3 python3-pip time zip micro bc
```

```
 Use your pip3 to install:
 > numpy matplotlib pandas seaborn ipython ipykernel jinja2 colorama
```

### Installing

Required packages can be installed in two ways:

##### Alternative 1 (use install.sh):
```
~$ cd nbr_setbench
~$ ./install.sh
```

##### Alternative 2 (manually):
```
Use the following commands: 

~$ sudo apt-get update

~$ sudo apt-get install -y build-essential dos2unix g++ libnuma-dev make numactl parallel \
 python3 python3-pip time zip bc

~$ pip3 install numpy matplotlib pandas seaborn ipython ipykernel jinja2 colorama
```

Once the required software/packages are installed we are ready to run the experiments and generate the figures discussed in  the submitted version of the paper.

## 🔧 Quick Test [approximately takes ~2 mins]
Until now, we have prepared the setup needed to compile and run the artifact. Now, let's do a quick test where we will compile and run  TYPE1 experiments to verify that the original experiment (described later) would work correctly.

Change directory to amortizedfree-setbench (if you used the alternative way to prepare your machine to execute the artifact) otherwise if you are in the docker container you would already be in amortizedfree-setbench/ directory.

To quickly compile, run and see default results for throughput experiment follow these steps:

* *step1*. Assuming you are currently in amortizedfree-setbench, execute the following command:

    ```~$ cd af_experiments```.

* *step2*. Run the following script: 

    ```~$ ./run_quicktest.sh```

This compiles the benchmark and run quick trials for all the experiments on a subset of run parameters which we will be run in detail in next sections.

**WARNING:** if you are running the experiment in the docker container **DO NOT** exit the terminal after the Quick test finishes as we would need to copy the generated figures on the host machine to be able to see them.  

### Analyze generated figures:
In case you chose to run the experiment on your system locally then you can simply find the figures in /amortizedfree-setbench/af_experiments/plots/ directory and analyse them.

Otherwise if you are running inside The Docker container follow below steps to fetch figures: 

To copy generated figures on your host machine copy the plots from the docker container to your host system by following these steps.

* Verify the name of the docker container. Use the following command which would give us the name of the loaded docker container under NAMES column which is 'nbr'.


    ```~$ sudo docker container ls```

Open a new terminal on the same machine. Move to any directory where you would want the generated plots to be copied (use cd). And execute the following command. 

* Copy the generated plots from the nbr_experiments/plots/ folder to your current directory.

    ```~$ sudo docker cp nbramortizedfree:/amortizedfree-setbench/af_experiments/plots/ .```

Now you can analyse the generated plots.

* Each plot for throughput experiments follows a naming convention: throughput-[data structure name]-[number of inserts]-[number of deletes].png. For example, a plot showing throughput of DGT with 50% inserts and 50% deletes is named as: throughput-guerraoui_ext_bst_ticket-i50-d50.png.

* Similarly the plot for peak memory usage experiments follows a naming convention: mem_usage-[data structure name]-[number of inserts]-[number of deletes].png. For example, a plot showing mem_usage of DGT with 50% inserts and 50% deletes is named as: mem_usage-guerraoui_ext_bst_ticket-i50-d50.png.

## 🔧 Running the tests with configuration reported in submitted paper [full experiments takes ~5 hrs]:

### TYPE1 Experiments:
TYPE1 experiments refer to all the experiments reported in paper that correspond to measuring performance and peak memory usage. This includes experiments correponding to Figure 11a, b, Figure 1 and Figure 10 in the paper.

* *step1*. Assuming you are currently in amortizedfree-setbench, execute the following command:

    ```~$ cd af_experiments```.

* *step2*. Run the following script to run experiment similar to Fig 11 a: 

    ```~$ ./run_exp1.sh```

    - This by default compiles, runs and produces plots similar to the experiment in Fig 11 a of the paper that compares throughput of amortized free token-EBR (token_af in paper and token4 in code) with other reclaimation algorithms.  
    
    - generated graphs can be found in  af_experiments/plots/plot_data_exp1

* *step3*. Run the following script to run experiment similar to Fig 11 b: 

    ```~$ ./run_exp2.sh```

    - This by default compiles, runs and produces plots similar to the experiment in Fig 11 b of the paper that compares throughput of each reclamation algorithm with its amortized free version.  

    - generated graphs can be found in  af_experiments/plots/plot_data_exp2

* *step4*. Run the following script to run experiment similar to Fig 1: 

    ```~$ ./run_fig1.sh```

    - This by default compiles, runs and produces plots similar to the experiment in Fig 1 of the paper that compares throughput and peak memory usage of  DEBRA and leaky implementation of two popular trees.

    - generated graphs can be found in  af_experiments/plots/plot_data_fig1

* *step5*. Run the following script to run experiment similar to Fig 10: 

    ```~$ ./run_fig10.sh```

    - This by default compiles, runs and produces plots similar to the experiment in Fig 10 of the paper that compares throughput of each variant of the proposed token algorithm, namely naive token(token1 in code), pass first token(token2 in code), periodic token(token3 in code) and amortized token(token4 in code).

    - generated graphs can be found in  af_experiments/plots/plot_data_fig10

All the above bash scripts execute python scripts (namely, exp1_run_tree.py, exp2_run_tree.py, fig1_run.py, fig10_run.py) that sets up the experiment, runs the trials and generates plots similar to those in paper.
The plots are generated in a subfolder within af_experiments/plots whose names is self explanatory. 

It is possible to run the experiments with run parameters other than those used in the paper (also set as defaults in scripts).

#### [Optional] How to change default run parameters?:

The python scripts exp1_run_tree.py, exp2_run_tree.py, fig1_run.py, fig10_run.py have define_experiment() method wherein following named run parametrs are declared.
Within these python scripts one can change their values.

- RECLAIMER_ALGOS: To provide any of the reclamatin algorithms supported by the benchmark
- __trials : To specify number of times a trial shoud repeat
-  TOTAL_THREADS : To specify number threads a trial should be run 
- INS_DEL_HALF: To specify the workload type (fraction of inserts deletes)
-  DS_SIZE : To specify the maximum size of a data structure
- DS_TYPENAME: To specify one of the supported data structures


#### ⛏️ Analyze generated figures:

If you are using the docker container, then copy the generated plots from the af_experiments/plots/expected_plots folder to your current directory.

    ```~$ sudo docker cp amortizedfree:/amortizedfree-setbench/af_experiments/plots/ .```

Now, you can analyse the generated plots and compare them with the expected plots (in af_experiments/plots/expected_plots/) assuming you have access to similar hardware.

Once the above test completes the resultant figures could be found in af_experiments/plots/. All plots follow the naming convention mentioned in the quick test section.

graphs in af_experiments/plots/plot_data_exp1 (fig 11 a, 11 b) use jemalloc allocator and have the following naming convention:
  - throughput-[dsname]-u[updatefraction]-sz[DS_size].png 
    For example, throughput-brown_ext_abtree_lf-u50-sz20000000.png represented throughput graph for ABTree with updates- 50%inserts and 50% deletes- and abtree size 20M nodes.

  - maxresident-[dsname]-u[updatefraction]-sz[DS_size].png
    For example, maxresident-brown_ext_abtree_lf-u50-sz20000000.png represented peak mmeory usage graph for ABTree with updates- 50%inserts and 50% deletes- and abtree size 20M nodes.

graphs in af_experiments/plots/plot_data_exp1 (fig 1 and 10) use ABtree data structure with 20M nodes and have the following naming convention:
  - throughput-[reclaimer]-[allocator].png 
    For example, throughput-debra-jemalloc.png represented throughput graph for ABTree with updates- 50%inserts and 50% deletes- and abtree size 20M nodes and jemalloc allocaor.

  - maxresident-[dsname]-[allocator].png
    For example, maxresident-brown_ext_abtree_lf-jemalloc.png represented peak memory usage graph for ABTree with updates- 50%inserts and 50% deletes- and abtree size 20M nodes.


#### 🚀 Types of machines we evaluated amortizedfree-setbench on:

* Smallest NUMA machine we have tested NBR has following configuration:
  * Architecture        : Intel x86_64
  * CPU(s)              : 8
  * Socket(s)           : 1
  * Thread(s) per core  : 2
  * Core(s) per socket  : 4
  * Memory              : 16G
* Largest NUMA machine we have tested NBR has following configuration:
  * Architecture        : Intel x86_64
  * CPU(s)              : 192
  * Socket(s)           : 4
  * Thread(s) per core  : 2
  * Core(s) per socket  : 24
  * Memory              : 377G

#### 🎉 Claims from the paper supported by the artifact:
- *claim 1*. Amortized-free Token-EBR (token4 in code) is faster than other reclamation algorithms considered in the paper.
  - please check throughput plots in af_experiments/plots/plot_data_exp1.

- *claim 2*. The amortized freeing significantly improves the performance of majority of the state of the art relciamers.
  - please check af_experiments/plots/plot_data_exp2





### TYPE2 Experiments:

TYPE2 experiments refer to all the experiments reported in paper that correspond to generating timeline graphs. This includes experiments correponding to Figure 2, 3, 4 (related to Debra) and Figure 6, 7, 8, 9 (related to token-EBR) in the paper.

* *step1*. Assuming you are currently in amortizedfree-setbench, execute the following command to run DEBRA related timeline experiments:

    ```~$ cd microbench/experiments/timelines/debra```.

* *step2*. Run the following script to run experiment similar to Fig 2: 

    ```~$ ./run_bf_threads.sh```

    - This by default compiles, runs and produces plots (in debra/data/) similar to the experiment in Fig 2 of the paper that compares time spent freeing batches of retired nodes for DEBRA when used with ABtree and jemalloc at 96 and 192 threads.  
    
    - generated graphs freetime_batch_jemalloc_96_interleave_pinyes.png shows timeline for 96 threads and 
    and freetime_batch_jemalloc_192_interleave_pinyes.png shows timeline for 192 threads


* *step3*. Run the following script to run experiment similar to Fig 3,4: 

    ```~$ ./run_bf_vs_af.sh```

    - This by default compiles, runs and produces plots similar to the experiment in Fig 3 of the paper that compares time spent by individual free calls at 192 threads for original DEBRA(batch free, freeOne_batch_jemalloc_192_interleave_pinyes.png) and amortized DEBRA (amortized free, freeOne_amortized_jemalloc_192_interleave_pinyes.png) for ABtree using jemalloc.  
    
    - Additionally it also produces plots (in debra/data/) similar to the experiment in Fig 4 of the paper that number of garbage nodes in each epoch for batch free (upper, unreclaimed_batch_jemalloc_192_interleave_pinyes.png) and amortized free (lower, unreclaimed_amortized_jemalloc_192_interleave_pinyes.png) for DEBRA when used with ABtree and jemalloc at 192 threads.  

If you are in docker machine the generated graphs can be copied in the way as described above.

To generate token algorithms related timeline graphs:

* *step1*. Assuming you are currently in amortizedfree-setbench, execute the following command to run TOKEN related timeline experiments:

    ```~$ cd microbench/experiments/timelines/tokens```.

* *step2*. Run the following script to run experiment similar to Fig 6,7,8,9: 

    ```~$ ./run.sh```

    - This by default compiles, runs and produces plots (in debra/data/) similar to the experiment in Fig 6,7,8,9 of the paper that compares time spent freeing batches of retired nodes for all 4 variants of token algorithms when used with ABtree and jemalloc at 192 threads.  

    - generated graphs would be found in tokens/data whihc are generated for abtree at 192 threads and jemalloc for each token variant.
    
    - Fig 6 (upper) depicting  timeline for batch freeing is shown by freeOne_token1_jemalloc_192_interleave_pinyes.png and (lower)depicting number of grabage nodes is shown by unreclaimed_token1_jemalloc_192_interleave_pinyes.png for token1 (Naive Token EBR)

    - Fig 7 (upper) depicting  timeline for batch freeing is shown by freeOne_token2_jemalloc_192_interleave_pinyes.png and (lower)depicting number of grabage nodes is shown by unreclaimed_token2_jemalloc_192_interleave_pinyes.png for token2 (Pass-First Token EBR)

    - Fig 8 (upper) depicting  timeline for batch freeing is shown by freeOne_token3_jemalloc_192_interleave_pinyes.png and (lower)depicting number of grabage nodes is shown by unreclaimed_token3_jemalloc_192_interleave_pinyes.png for token3 (Periodic Token EBR)

    - Fig 9 (upper) depicting  timeline for batch freeing is shown by freeOne_token4_jemalloc_192_interleave_pinyes.png and (lower)depicting number of grabage nodes is shown by unreclaimed_token4_jemalloc_192_interleave_pinyes.png for token4 (Amortized-Free Token EBR)
    
## ✍️ References
1. https://gitlab.com/trbot86/setbench
2. https://mc.uwaterloo.ca/code.html
3. https://github.com/urcs-sync/Interval-Based-Reclamation






## Installing Docker
Please follow these commands in order:

``` ~$ sudo apt update```

``` ~$ sudo apt-get install curl apt-transport-https ca-certificates software-properties-common ```

``` ~$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - ```

``` ~$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"  ``` 

``` ~$ sudo apt update ```

``` ~$ sudo apt install docker-ce  ```

verify installation:

``` ~$ docker -v ```

## Misc:

### Build Docker image
``` sudo docker build -t amortizedfree-setbench . ```

### Save docker image
``` sudo docker save amortizedfree-setbench:latest | gzip > amortizedfree_docker.tar.gz ```

### erase all docker containers in the system
``` docker system prune -a ```
