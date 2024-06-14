import os
import numpy as np
import pickle 
import sys
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import argparse
 
 
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-pt", "--plot_type", default="study_monolithic",help = "Plot Type 1. study_monolithic 2. study_sequence_of_ILoSA")
 
# Read arguments from command line
args = parser.parse_args()

dir_path = os.path.dirname(os.path.realpath(__file__))
data_folder =dir_path+"/"+args.plot_type+"/"
results_folder=data_folder+"results/"
print(data_folder)

#Plot Function

def plot_trajectory(traj,data_folder,name_traj,tag="demo"):
    
    for i, trajectory in enumerate(traj):
        ax = plt.axes(projection='3d')
        if tag=="demo":
            ax.plot(trajectory[:,0], trajectory[:,1], trajectory[:,2])
            ax.scatter(trajectory[0,0], trajectory[0,1], trajectory[0,2], c='r', marker='o')
            ax.scatter(trajectory[-1,0], trajectory[-1,1], trajectory[-1,2], c='g', marker='o')
        else:
            ax.plot(trajectory[0,:], trajectory[1,:], trajectory[2,:])
            ax.scatter(trajectory[0,0], trajectory[1,0], trajectory[2,0], c='r', marker='o')
            ax.scatter(trajectory[0,-1], trajectory[1,-1], trajectory[2,-1], c='g', marker='o')
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, 0.5)
        ax.set_zlim(0, 1)
        
        plt.savefig(f'{data_folder}plots/{tag}/{name_traj[i]}.png', bbox_inches='tight') 

# Structuring NPZ files for demo and execution trajectory plots


traj = []
traj_ori = []
name_traj = []
name_traj_ori = []

test_traj_ori_cart = []
test_traj_cart=[]
name_test_traj_cart = []
name_test_traj_ori_cart = []

test_traj_ori_attractor = []
test_traj_attractor=[]
name_test_traj_attractor = []
name_test_traj_ori_attractor = []


for filename in sorted(os.listdir(results_folder)):
    
    if filename.endswith(".npz") and not "exec" in filename:
        data=np.load(results_folder+ filename)
        keys = list(data.keys())
        traj_ori.append(data[keys[1]])
        name_traj_ori.append(os.path.splitext(filename)[0])
        traj.append(data[keys[0]])
        name_traj.append(os.path.splitext(filename)[0])

    else:
        data=np.load(results_folder+ filename)
        keys = list(data.keys())

        # Cart Data
        test_traj_cart.append(data[keys[0]][:3,:])
        name_test_traj_cart.append(os.path.splitext(filename)[0])
        test_traj_ori_cart.append(data[keys[0]][3:7,:])
        name_test_traj_ori_cart.append(os.path.splitext(filename)[0])

        # Attractor Data
        test_traj_attractor.append(data[keys[1]][:3,:])
        name_test_traj_attractor.append(os.path.splitext(filename)[0])
        test_traj_ori_attractor.append(data[keys[1]][3:7,:])
        name_test_traj_ori_attractor.append(os.path.splitext(filename)[0])

plot_trajectory(traj,data_folder,name_traj,tag="demo")
plot_trajectory(test_traj_cart,data_folder,name_test_traj_cart,tag="test_attractor")
plot_trajectory(test_traj_attractor,data_folder,name_test_traj_attractor,tag="test_cart")