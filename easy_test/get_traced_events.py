import argparse
import yaml
import os
import json
import math
import sqlite3
import re
import numpy as np
import random
from scipy import interpolate
from collections import defaultdict
from queue import Queue
from tqdm import tqdm

from generator_modules.nsys_events import get_nsys_events
from generator_modules.manipulate_events import merge_nsys_events, check_events_pair, get_events_parallel_group

from generator_modules.apply_config import apply_user_config
from generator_modules.data_dependency_modules.events_dependency import get_events_dependency
from generator_modules.data_dependency_modules.in_gpu_dependency import get_in_gpu_microevents_dependency
from generator_modules.data_dependency_modules.inter_node_dependency import get_inter_node_microevents_dependency

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_node_gpu', type=str, required=False, help='yaml file for configuration of nodes and GPUs')
    args = parser.parse_args()

    # Get nsys events
    Dir_Path = './results/nsys_reports'
    Comm_Init_Events, NCCL_Events, CUPTI_Kernel_Results, Comm_Info, HostName_To_GoalRank = get_nsys_events(Dir_Path)  ## nccl_events, cupti_kernel_results, comm_info, HostName_To_GoalRank
    intermediate_output = {
        "hostname_to_rank": HostName_To_GoalRank,
        "comm_info": Comm_Info,
        "cupti_kernel_results": CUPTI_Kernel_Results,
        "nccl_events": NCCL_Events,
        "comm_init_events": Comm_Init_Events
    }
    with open('./results/nsys_events_intermediate_output.json', 'w') as json_file:
        json.dump(intermediate_output, json_file, indent=4)
    print('Nsys_Events has been exported to nsys_events_intermediate_output.json')
    # exit(0)
    Merged_Events = merge_nsys_events(NCCL_Events, CUPTI_Kernel_Results, Comm_Info)
    with open('./results/nsys_events_merged_output.json', 'w') as json_file:
        json.dump(Merged_Events, json_file, indent=4)
        json_file.write("\n\n")
    print('Merged_Events has been exported to nsys_events_merged_output.json')

    Events_Pair = check_events_pair(Merged_Events)
    with open('./results/nsys_events_pair_output.json', 'w') as json_file:
        json.dump(Events_Pair, json_file, indent=4)
        json_file.write("\n\n")

    # Expanded_Events = expand_group_events(Merged_Events)
    # with open('./results/nsys_events_expanded_output.json', 'w') as json_file:
    #     json.dump(Expanded_Events, json_file, indent=4)
    #     json_file.write("\n\n")

    Events_Parallel_Group = get_events_parallel_group(Merged_Events)
    with open('./results/nsys_events_parallel_group_output.json', 'w') as json_file:
        json.dump(Events_Parallel_Group, json_file, indent=4)
        json_file.write("\n\n")

    if args.config_node_gpu is not None:
        Events_Parallel_Group, Comm_Init_Events, Comm_Info = apply_user_config(args.config_node_gpu, Events_Parallel_Group, Comm_Init_Events, Comm_Info)
        with open('./results/Restructured_Comm_Info.json', 'w') as json_file:
            json.dump(Comm_Info, json_file, indent=4)
            json_file.write("\n\n")

    # Goal_File_Name = './results/Events_Dependency.goal'
    # get_events_dependency(Events_Parallel_Group, Comm_Init_Events, Goal_File_Name)
    # print('Events goal file has been exported to Events_Dependency.goal')

    print(f"[INFO] Start to generate goal file for In-GPU and Internode events")
    Goal_File_Name = './results/InGPU_MicroEvents_Dependency.goal'
    SendRecvEvents_To_TaskCounter = get_in_gpu_microevents_dependency(Events_Parallel_Group, Comm_Init_Events, Comm_Info, Goal_File_Name)
    with open('./results/SendRecvEvents_To_TaskCounter.json', 'w') as json_file:
        json.dump(SendRecvEvents_To_TaskCounter, json_file, indent=4)
        json_file.write("\n\n")
    print('In-GPU goal file has been exported to InGPU_MicroEvents_Dependency.goal')

    Goal_File_Name = './results/InterNode_MicroEvents_Dependency.goal'
    get_inter_node_microevents_dependency(Events_Parallel_Group, Comm_Init_Events, Comm_Info, SendRecvEvents_To_TaskCounter, Goal_File_Name)
    print('Internode goal file has been exported to InterNode_MicroEvents_Dependency.goal')

if __name__ == '__main__':
    main()