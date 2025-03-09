import json
import os

def merge_statistics(results_dir, output_file):
    merged_statistics = {}

    for root, _, files in os.walk(results_dir):
        for file in files:
            if file == 'events_statistics.json':
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    try:
                        file_statistics = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse {file_path}, skipping.")
                        continue

                for event, sizes in file_statistics.items():
                    if event not in merged_statistics:
                        merged_statistics[event] = {}

                    for size, values in sizes.items():
                        if size not in merged_statistics[event]:
                            merged_statistics[event][size] = []

                        merged_statistics[event][size].extend(values)  # 合并 list

    with open(output_file, 'w') as json_file:
        json.dump(merged_statistics, json_file, indent=4)
        json_file.write('\n\n')

    print(f"Merged statistics saved to {output_file}")

def main():
    results_dir = './results'
    output_file = './npkit_data_summary_LL.json'
    merge_statistics(results_dir, output_file)

if __name__ == '__main__':
    main()
