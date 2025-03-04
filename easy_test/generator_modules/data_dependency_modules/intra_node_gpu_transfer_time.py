def get_intra_node_gpu_transfer_time(data_size, transfer_type):  
    """
    data_size [byte]: data + flag, not just data
    Here we use the bandwidth of NVLink 3.0, which is 50 GT/s , each transfer is 1 byte
    """

    if transfer_type == 'Send':
        return data_size * 10**9 // (50 * 10**9 * 1 * 2)  ## ns

    elif transfer_type == 'Recv':
        return data_size * 10**9 // (50 * 10**9 * 1 * 2)  ## ns
    