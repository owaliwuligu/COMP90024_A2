#!/bin/bash
# Created by the University of Melbourne job script generator for SLURM
#SBATCH --job-name=CCC-A2-Restaurant
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:50:00


module purge
module load foss/2019b
module load python/3.7.4

echo $(hostname ) $SLURM_JOB_NAME
time srun -n 16 python3 RestaurantMiner.py
