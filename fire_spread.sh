#!/bin/bash
#$ -m e
#$ -N fire_sim
#$ -j y
source /opt/rh/rh-python36/enable
#virtualenv venv36
source venv36/bin/activate
#pip install --upgrade pip
#pip install numpy
#pip install matplotlib
python main.py