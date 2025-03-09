import json
import os
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def plot_probability_distributions(json_data, output_dir='./plots'):
    os.makedirs(output_dir, exist_ok=True) 

    for top_key, sub_data in json_data.items():
        plt.figure(figsize=(12, 8))

        sorted_keys = sorted(sub_data.keys(), key=lambda x: int(x))  

        x_keys = []
        y_values = []
        
        for key in sorted_keys:
            values = sub_data[key]
            x_keys.extend([key] * len(values))  
            y_values.extend(values)            

        sns.violinplot(x=x_keys, y=y_values, inner='quart', density_norm='width', order=sorted_keys)
        plt.title(f'Value Distribution for {top_key}')
        plt.xlabel('Keys (Second Level)')
        plt.ylabel('Values')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45) 
        plt.tight_layout()
        
        save_path = os.path.join(output_dir, f'{top_key}_distribution.png')
        plt.savefig(save_path) 
        print(f'Saved plot: {save_path}')
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot probability distributions from a JSON file.")
    parser.add_argument("-i", "--json_file", type=str, help="Path to the JSON file.")
    parser.add_argument("--output_dir", type=str, default="./plots", help="Directory to save the plots.")
    
    args = parser.parse_args()

    data = load_json(args.json_file)
    plot_probability_distributions(data, args.output_dir)

if __name__ == "__main__":
    main()
