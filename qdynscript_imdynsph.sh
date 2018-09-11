#!/bin/bash
#SBATCH -J quenchImdyn
#SBATCH -n 2
#SBATCH -N 1
#SBATCH -t 2-12:00
#SBATCH -p shared
#SBATCH --mem=10000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=kis@mit.edu 
#SBATCH --open-mode=append
#SBATCH -o /n/regal/demler_lab/kis/genPol_data/std/quenchImdyn_%A_%a.out
#SBATCH -e /n/regal/demler_lab/kis/genPol_data/std/quenchImdyn_%A_%a.err

module load Anaconda3/5.0.1-fasrc01
source activate anaclone
python datagen_qdynamics_imdyn_sph.py