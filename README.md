This repo contains the code and experiment setup used to evaluate the amortized freeing and token EBR algorithm presented in PPOPP23 paper titled: "Are Your Epochs Too Epic? Batch Free Can Be Harmful".

#to reproduce exp1 and exp2:
1. switch to af_experiments/
2. ./run_exp1.sh for exp1 and ./run_exp2.sh for exp2.
3. To change experiment parameters like workload, data structure, change in exp1_run_tree.py or exp2_run_tree.py
4. After experiments completes plots will be generated inside plots/

#CREDITS:
This repo builds upon the  nbr_setbench_plus project used for neutralization based reclamation techniques, which in turn used the original [setbench](https://gitlab.com/trbot86/setbench) of [Multicore Lab](https://mc.uwaterloo.ca/) headed by Prof. Trevor Brown to test and evaluate lockfree data structures and reclamation algorithms.


###TODO: Daewoo and I gonna use following style of readme for ppopp23 AE.

## 🏁 Getting Started

These instructions will get you a copy of the artifact up and running on your machine for development and testing purposes. This can be done in two ways: 1) use our docker provided image or 2) alternatively prepare your machine to run our artifact.

``` NOTE: To better reproduce results of NBR we suggest to run nbr_setbench on a multicore NUMA machine with at least two NUMA nodes.```

# Running on Docker
* Install the latest version of Docker on your system. We tested the artifact with the Docker version 19.03.6, build 369ce74a3c. Instructions to install Docker may be found at https://docs.docker.com/engine/install/ubuntu/. Or you may refer to the "Installing Docker" section at the end of this README.

  To check the version of docker on your machine use: 

    ``` ~$ docker -v```
* First, download the artifact named nbr_setbench.zip from the ppopp2021 artifact submission link (or at https://zenodo.org/record/4295604).

* Find docker image named nbr_docker.tar.gz in nbr_setbench/ directory. 
  And load the downloaded docker image with the following command.

    ```~$ sudo docker load -i nbr_docker.tar.gz ```
* Verify that image was loaded.

    ```~$ sudo docker images```
* start a docker container from the loaded image

    ```~$ sudo docker run --name nbr -i -t --privileged nbr_setbench /bin/bash ```
* run ls to see several files/folders of the artifact: Dockerfile README.md, common, ds, install.sh, lib, microbench, nbr_experiments, tools. 

    ```~$ ls ```
If this succeeds you can move to the quick test section and skip the following section which discusses alternative ways to prepare your machine to run the artifact.

# *Alternative Way:* Preparing Host Machine:
In case you may want to prepare the host machine itself to run the artifact locally follow these instructions.

First, download the artifact named nbr_setbench.zip from ppopp2021 artifact submission link (or at https://zenodo.org/record/4295604).

The artifact requires the following packages/softwares on your Linux machine to compile and run the artifact.

```
 Use your system's package manager to install:
 > build-essential dos2unix g++ libnuma-dev make numactl parallel python3 python3-pip time zip micro
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
 python3 python3-pip time zip

~$ pip3 install numpy matplotlib pandas seaborn ipython ipykernel jinja2 colorama
```

Once the required software/packages are installed we are ready to run the experiments and generate the figures discussed in  the submitted version of the paper.

## 🔧 Quick Test
Until now, we have prepared the setup needed to compile and run the artifact. Now, let's do a quick test where we will compile, run and generate results to verify that the original experiment (described later) would work correctly.

We would run two types of experiments. First, experiment to evaluate throughput (Figure 3 in the paper) and second experiment to evaluate peak memory usage (Figure 4 in the paper)

Change directory to nbr_setbench (if you used the alternative way to prepare your machine to execute the artifact) otherwise if you are in the docker container you would already be in nbr_setbench/ directory.

### Evaluate throughput: 
To quickly compile, run and see default results for throughput experiment follow these steps:

* *step1*. Assuming you are currently in nbr_setbench, execute the following command:

    ```~$ cd nbr_experiments```.
* *step2*. Run the following command: 

    ```~$ ./run.sh```

The Quick test uses inputs provided from files in nbr_experiments/inputs/.

Default content of the files is comma separated values:

  * *reclaimer.txt*      : nbrplus,debra
  * *steps.txt*          : 1
  * *threadsequence.txt* : 2,4,8,16
  * *workloadtype.txt*   : 50
  * *treesize.txt*       : 2000000
  * *listsize.txt*       : 20000

### Evaluate memory usage: 
To quickly compile, run and see default results for peak memory usage experiment follow these steps:

* *step1*. Assuming you are currently in nbr_setbench, execute the following command:

  ```~$ cd nbr_experiments```.
* *step2*. Run the following command: 

  ```~$ ./run_memusage.sh```

**WARNING:** if you are running the experiment in the docker container **DO NOT** exit the terminal after the Quick test finishes as we would need to copy the generated figures on the host machine to be able to see them.  

### Analyze generated figures:
In case you chose to run the experiment on your system locally then you can simply find the figures in /nbr_setbench/nbr_experiments/plots/generated_plots/ directory and analyse them.

Otherwise if you are running inside The Docker container follow below steps to fetch figures: 

To copy generated figures on your host machine copy the plots from the docker container to your host system by following these steps.

* Verify the name of the docker container. Use the following command which would give us the name of the loaded docker container under NAMES column which is 'nbr'.


    ```~$ sudo docker container ls```

Open a new terminal on the same machine. Move to any directory where you would want the generated plots to be copied (use cd). And execute the following command. 

* Copy the generated plots from the nbr_experiments/plots/generated_plots folder to your current directory.

    ```~$ sudo docker cp nbr:/nbr_setbench/nbr_experiments/plots/generated_plots/ .```

Now you can analyse the generated plots.

* Each plot for throughput experiments follows a naming convention: throughput-[data structure name]-[number of inserts]-[number of deletes].png. For example, a plot showing throughput of DGT with 50% inserts and 50% deletes is named as: throughput-guerraoui_ext_bst_ticket-i50-d50.png.

* Similarly the plot for peak memory usage experiments follows a naming convention: mem_usage-[data structure name]-[number of inserts]-[number of deletes].png. For example, a plot showing mem_usage of DGT with 50% inserts and 50% deletes is named as: mem_usage-guerraoui_ext_bst_ticket-i50-d50.png.

## 🔧 Running the tests with configuration reported in submitted paper [full experiments takes ~5 hrs]:

### Throughput experiments:
To reproduce figures reported in the submitted version of the paper please change inputs as indicated below:

Inside nbr_experiments/inputs/ change:

  * *reclaimer.txt*      : nbrplus,debra,none,ibr,qsbr,ibr_rcu,hazardptr
  * *steps.txt*          : 1,2,3
  * *threadsequence.txt* : 18,36,54,72,90,108,126,144,162,180,198,216,234,252
  * *workloadtype.txt*   : 5,25,50
  * *treesize.txt*       : 2000000
  * *listsize.txt*       : 20000       #this was list size used in experiments of submitted version. The paper's typo where it mentions 2K for the list size woud be corrected in the Camera ready version.

> Please ensure that comma separated values are provided. Simply copy pasting the aforementioned values in each corresponding input files should work, make sure not to introduce any space or newline at the end of a line in input files as that could cause errors in the script.

> **Warning**: Using a list size more than 20K will take long time in prefilling the list. Therefore, we suggest to use a list size of less than or equal to 20K. 

### Steps to change inputs inside the docker container:
``` ~$ cd nbr_experiments/inputs/ ```

Now change the appropriate '.txt' file using micro text editor (or editor of your choice, we have micro text editors pre-installed in the docker image) using following example command:

``` ~$ micro reclaimer.txt ```

save your changes and repeat this process for other input files listed above.

Next, repeat the following steps as done in the Quick test.
### Evaluate throughput:

* *step1*. Assuming you are currently in nbr_setbench, execute the following command:

    ```~$ cd nbr_experiments```.
* *step2*. Run the following command: 

    ```~$ ./run.sh```

 For the figures in the submitted paper we tested NBR on a NUMA machine with the following configuration:

    * Architecture        : Intel x86_64
    * CPU(s)              : 144
    * Sockets(s)          : 4
    * Thread(s) per core  : 2
    * Core(s) per socket  : 18
    * Memory              : 188G

Note: as long as the nbr_setbench is run on a 144 thread machine with 4 NUMA nodes the generated plots should match the expected plots.

### Evaluate memory usage: 

* *step1*. Assuming you are currently in nbr_setbench, execute the following command:

    ```~$ cd nbr_experiments```.
* *step2*. Run the following command:
    
    ```~$ ./run_memusage.sh```

### ⛏️ Analyze generated figures:

Once the above test completes the resultant figures could be found in nbr_experiments/plots/generated_plots. All plots follow the naming convention mentioned in the quick test section.

We have put the expected figures for this experiment in the nbr_experiments/plots/expected_plots/ directory. Please copy this directory in the same way as we copied  nbr_experiments/plots/generated_plots/

* Copy the generated plots from the nbr_experiments/plots/expected_plots folder to your current directory.

    ```~$ sudo docker cp nbr:/nbr_setbench/nbr_experiments/plots/expected_plots/ .```

Now you can analyse the generated plots and compare them with the expected plots assuming you have access to similar hardware.



## 🎉 What does run.sh do?

Inputs for experiments are provided from the following files:

  * *reclaimer.txt*      : comma separated list of reclamation algorithm names
  * *steps.txt*          : comma separated list of number of steps each run needs to repeat.
  * *threadsequence.txt* : comma separated list of thread sequence you want to run experiements with. This sequence becomes the X-axis for the generated throughput figures.
  * *workloadtype.txt*   : comma separated list of workload types. For eg., to evaluate with workload type of 50% inserts and 50% deletes enter 50 in workloadtype.txt.
  * *treesize.txt*       : Max number of nodes in tree.
  * *listsize.txt*       : Max number of nodes in list.


run.sh will do the following:

1. Compile the benchmark with reclamation algorithms and data structures.
2. Run all reclamation algorithms (NBR+, Debra, QSBR, RCU, IBR, Hazard Pointer, None), for a sequence of threads (say, 18, 36, 54, .... 234, 252), for varying workloads (say, 50% inserts 50% deletes, 25% inserts 25% deletes, and 5% inserts 5% deletes) for DGT. One reclamation algorithm is run several times. Each run is called one step. For example, NBR+ executing with 18 threads for a workload type that has 50% inserts and 50% deletes is called one step in our experiments.
3. Produce figures in directory nbr_setbench/nbr_experiments/plots/generated_plots.
4. Run all reclamation algorithms, for a sequence of threads, for varying workloads with lazylist. One reclamation algorithm is run several times. Each run is called one step. For example, NBR+ executing with 18 threads for a workload type that has 50% inserts and 50% deletes is called one step in our experiments.
5. Produce figures in directory nbr_setbench/nbr_experiments/plots/generated_plots.


## 🚀 Types of machines we evaluated NBR-setnbench on:

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

## 🎉 Claims from the paper supported by the artifact:
- *claim 1*. NBR+ is faster than other reclamation algorithms considered in the paper.
  - please check throughput plots in nbr_setbench/nbr_experiments/plots/generated_plots.
  - On our 144 CPUs and 4 sockets machine with 188G memory NBR+ has better throughput after 72 threads than other reclamation algorithms. 
- *claim 2*. NBR+ has approximately constant peak memory usage across different threads.
  - please check mem-usage plots in nbr_setbench/nbr_experiments/plots/generated_plots
  - On our 144 CPUs and 4 sockets machine with 188G memory NBR+ has approximately constant peak memory usage.

## ✍️ References
1. https://gitlab.com/trbot86/setbench
2. https://mc.uwaterloo.ca/code.html
3. David, T., Guerraoui, R., & Trigonakis, V. (2015). Asynchronized concurrency: The secret to scaling concurrent search data structures. ACM SIGARCH Computer Architecture News, 43(1), 631-644.
4. Heller, S., Herlihy, M., Luchangco, V., Moir, M., Scherer, W. N., & Shavit, N. (2005, December). A lazy concurrent list-based set algorithm. In International Conference On Principles Of Distributed Systems (pp. 3-16). Springer, Berlin, Heidelberg.
5. https://github.com/urcs-sync/Interval-Based-Reclamation






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
``` sudo docker build -t nbr_setbench . ```

### Save docker image
``` sudo docker save nbr_setbench:latest | gzip > nbr_docker.tar.gz ```

### erase all docker containers in the system
``` docker system prune -a ```
