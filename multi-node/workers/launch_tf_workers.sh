#!/bin/bash

#PBS -l partition=gpu
#PBS -l nodes=2:ppn=1:gpus=4
#PBS -W x=nmatchpolicy:exactnode
#PBS -l walltime=0:10:00
#PBS -A lpt2_pilot_2018
#PBS -N tf_workers 
#PBS -j oe

# Make MPI commands available
module load OpenMPI
# Activate appropriate conda environment
. /data/leuven/319/vsc31962/miniconda3/etc/profile.d/conda.sh
conda activate py27-tf
# Change to appropriate directory
cd $VSC_DATA/tf-distribution-strategy/multi-node/workers

# Store ClusterSpec in TF_CONFIG
source export_TF_CONFIG.sh

# Launch workers ($hosts should be available after sourcing export_TF_CONFIG.sh)
mpirun -np 1 --map-by node python task_0.py
mpirun -np 1 --map-by node python task_1.py
python simple_estimator_example.py 

