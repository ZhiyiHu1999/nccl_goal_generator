import argparse
import subprocess
import tempfile

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--training_script",
        type=str,
        required=True,
        help="script for training"
    )

    parser.add_argument(
        '--config_node_gpu', 
        type=str, 
        required=False, 
        help='yaml file for configuration of nodes and GPUs'
    )

    parser.add_argument(
        '--results_dir', 
        type=str, 
        required=True, 
        help='directory for results'
    )

    args = parser.parse_args()

    temp_dir = tempfile.mkdtemp()
    print(f"Temporary Directory Name: {temp_dir}")

    commands = f"""
        rm -rf {temp_dir}
        mkdir -p {temp_dir}

        export NSYS_REPORT_DIR="{temp_dir}/nsys_reports"
        rm -rf $NSYS_REPORT_DIR
        mkdir -p $NSYS_REPORT_DIR

        srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile \
        --trace=nvtx,cuda \
        --cuda-memory-usage=false \
        --cuda-um-cpu-page-faults=false \
        --cuda-um-gpu-page-faults=false \
        -s none \
        --output=${{NSYS_REPORT_DIR}}/nsys_report_%h_%p \
        bash {args.training_script}

        for report_file in ${{NSYS_REPORT_DIR}}/*.nsys-rep; do
            if [ -f "$report_file" ]; then
                sqlite_file="${{report_file%.nsys-rep}}.sqlite"
                ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite \
                --ts-normalize=true --output="$sqlite_file" "$report_file"
                echo "Exported $report_file to $sqlite_file"
            fi
        done

        python3 get_traced_events.py --config_node_gpu {args.config_node_gpu} --results_dir {temp_dir}

        rm -rf {args.results_dir}
        mkdir -p {args.results_dir}
        cp {temp_dir}/InterNode_MicroEvents_Dependency.goal {args.results_dir}
    """

        # python3 goal2dot.py
        # dot -Tsvg ./results/Events_Dependency.dot -o ./results/Events_Dependency.svg
        # dot -Tsvg ./results/InGPU_MicroEvents_Dependency.dot -o ./results/InGPU_MicroEvents_Dependency.svg
        # dot -Tsvg ./results/InterNode_MicroEvents_Dependency.dot -o ./results/InterNode_MicroEvents_Dependency.svg    

    subprocess.run(commands, shell=True, executable="/bin/bash", check=True)

if __name__ == '__main__':
    main()
