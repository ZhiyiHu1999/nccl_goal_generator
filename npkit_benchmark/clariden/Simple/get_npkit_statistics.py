import json
import os

def get_statistics(input_file):
    with open(input_file, "r") as f:
        traced_data = json.load(f)

    traced_events = traced_data['traceEvents']

    gpu_events = {}
    prim_events = {}
    events_statistics = {}

    for event in traced_events:
        pid = event['pid']
        tid = event['tid']
        ph = event['ph']
        ts = event['ts']
        name = event['name']
        
        if pid not in gpu_events:
            gpu_events[pid] = {}

        if tid not in gpu_events[pid]:
            gpu_events[pid][tid] = []

        if pid not in prim_events:
            prim_events[pid] = {}

        if tid not in prim_events[pid]:
            prim_events[pid][tid] = []

        if name.startswith('NPKIT_EVENT_GPU'):
            trimmed_name = name.rsplit("_", 1)[0]

            if trimmed_name not in events_statistics:
                events_statistics[trimmed_name] = {}

            if ph == 'B':
                gpu_events[pid][tid].append(
                    {
                        'event_name': trimmed_name,
                        'ts_start': ts
                    }
                )
            
            elif ph == 'E':
                gpu_events[pid][tid][-1]['ts_end'] = ts

        elif name.startswith('NPKIT_EVENT_PRIM'):
            trimmed_name = name.rsplit("_", 1)[0]

            if ph == 'E':
                prim_events[pid][tid].append(
                    {
                    'event_name': trimmed_name,
                    'size': event['args']['size_0'],
                    'calc_time': int(event['args']['rsvd_0']),
                    'ts': ts
                    }
                )

    for pid in gpu_events:
        for tid in gpu_events[pid]:
            for i in range(len(gpu_events[pid][tid])):
                gpu_event_name = gpu_events[pid][tid][i]['event_name']
                gpu_ts_start = gpu_events[pid][tid][i]['ts_start']
                gpu_ts_end = gpu_events[pid][tid][i]['ts_end']

                for j in range(len(prim_events[pid][tid])):
                    prim_ts = prim_events[pid][tid][j]['ts']
                    size = prim_events[pid][tid][j]['size']
                    calc_time = prim_events[pid][tid][j]['calc_time']

                    if gpu_ts_start <= prim_ts <= gpu_ts_end:
                        if size not in events_statistics[gpu_event_name]:
                            events_statistics[gpu_event_name][size] = []

                        events_statistics[gpu_event_name][size].append(calc_time)

    return events_statistics

def process_all_files(results_dir):
    for root, _, files in os.walk(results_dir):
        for file in files:
            if file == 'npkit_event_trace.json':
                input_path = os.path.join(root, file)
                output_path = os.path.join(root, 'events_statistics.json')

                print(f"Processing {input_path}...")

                events_statistics = get_statistics(input_path)

                with open(output_path, 'w') as json_file:
                    json.dump(events_statistics, json_file, indent=4)
                    json_file.write('\n\n')

                print(f"Saved statistics to {output_path}")

def main():
    results_dir = './results'
    process_all_files(results_dir)

if __name__ == '__main__':
    main()
