import json
import random
import numpy as np
from scipy import interpolate

with open('npkit_data_summary_Simple.json', 'r') as f_simple:
    DATA_SIMPLE = json.load(f_simple)

with open('npkit_data_summary_LL.json', 'r') as f_ll:
    DATA_LL = json.load(f_ll)

def get_reduction_time(data_size, protocol):  ## data_size: size of data, not data + flag
    if protocol == '2':
        data = DATA_SIMPLE
    elif protocol == '0':
        data = DATA_LL

    if str(data_size) in data['NPKIT_EVENT_GPU_RECV_REDUCE_SEND']:
        reduction_times = data['NPKIT_EVENT_GPU_RECV_REDUCE_SEND'][str(data_size)]
        return random.choice(reduction_times)

    sizes = [int(size) for size in data['NPKIT_EVENT_GPU_RECV_REDUCE_SEND'].keys()]
    sizes.sort()

    if data_size < sizes[0]:
        return random.choice(data['NPKIT_EVENT_GPU_RECV_REDUCE_SEND'][str(sizes[0])])
    if data_size > sizes[-1]:
        return random.choice(data['NPKIT_EVENT_GPU_RECV_REDUCE_SEND'][str(sizes[-1])])

    f = interpolate.interp1d(sizes, [np.mean(data['NPKIT_EVENT_GPU_RECV_REDUCE_SEND'][str(size)]) for size in sizes], kind='linear', fill_value="extrapolate")
    interpolated_value = f(data_size)
    
    return int(random.gauss(interpolated_value, interpolated_value * 0.01))

def get_copy_time(data_size, protocol):  ## data_size: size of data, not data + flag
    if protocol == '2':
        data = DATA_SIMPLE
    elif protocol == '0':
        data = DATA_LL

    if str(data_size) in data['NPKIT_EVENT_GPU_DIRECT_RECV_COPY_SEND']:
        reduction_times = data['NPKIT_EVENT_GPU_DIRECT_RECV_COPY_SEND'][str(data_size)]
        return random.choice(reduction_times)

    sizes = [int(size) for size in data['NPKIT_EVENT_GPU_DIRECT_RECV_COPY_SEND'].keys()]
    sizes.sort()

    if data_size < sizes[0]:
        return random.choice(data['NPKIT_EVENT_GPU_DIRECT_RECV_COPY_SEND'][str(sizes[0])])
    if data_size > sizes[-1]:
        return random.choice(data['NPKIT_EVENT_GPU_DIRECT_RECV_COPY_SEND'][str(sizes[-1])])

    f = interpolate.interp1d(sizes, [np.mean(data['NPKIT_EVENT_GPU_DIRECT_RECV_COPY_SEND'][str(size)]) for size in sizes], kind='linear', fill_value="extrapolate")
    interpolated_value = f(data_size)
    
    return int(random.gauss(interpolated_value, interpolated_value * 0.01))
