import re
from collections import defaultdict

def parse_goal_file(file_path):
    # Modify graphs to create a subgraph for each rank
    graphs = defaultdict(lambda: {'nodes': set(), 'edges': []})
    task_infos = defaultdict(lambda: defaultdict(dict))
    current_rank = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Process rank information
            if line.startswith("rank"):
                current_rank = re.match(r"rank (\d+)", line).group(1)

            elif line.startswith("l"):
                match = re.match(r"(l\d+):(.*)", line)
                if match:
                    node = match.group(1)
                    task_infos[current_rank][node] = match.group(2).strip()
                    # Add all task nodes to the subgraph for the current rank
                    graphs[current_rank]['nodes'].add(node)

                else:        
                    # Process dependency relationships
                    if "requires" in line or "irequires" in line:
                        match = re.match(r"(l\d+) (i?requires) (l\d+)", line)
                        if match:
                            src, edge_type, dst = match.groups()
                            graphs[current_rank]['edges'].append((src, dst, edge_type))

    # Print the result
    for rank, graph_data in graphs.items():
        print(f"(rank {rank}):")
        for key, value in graph_data.items():
            print(f"    {key}:")
            for data in value:
                print(f"        {data}")

    return graphs, task_infos

def generate_graphviz(graphs, task_infos):
    graphviz_input = "digraph G {\n"
    graphviz_input += "    rankdir=LR;\n"

    for rank, graph_data in graphs.items():
        subgraph_name = f"cluster_rank_{rank}"
        graphviz_input += f'    subgraph "{subgraph_name}" {{\n'
        graphviz_input += f'        label = "Rank {rank}";\n'

        for node in graph_data['nodes']:
            unique_node = f"{node}_rank{rank}: {task_infos[rank][node]}"
            # Set node colors: nodes with "recv" are light red, nodes with "send" are light blue
            if "recv" in task_infos[rank][node]:
                color = "lightcoral"  # Light red
            elif "send" in task_infos[rank][node]:
                color = "lightblue"  # Light blue
            else:
                color = "white"  # Default color
            graphviz_input += f'        "{unique_node}" [style=filled, fillcolor="{color}"];\n'

        for src, dst, edge_type in graph_data['edges']:
            unique_src = f"{src}_rank{rank}: {task_infos[rank][src]}"
            unique_dst = f"{dst}_rank{rank}: {task_infos[rank][dst]}"
            color = "black" if edge_type == "requires" else "red"
            graphviz_input += f'        "{unique_dst}" -> "{unique_src}" [label="{edge_type}", color="{color}"];\n'

        graphviz_input += "    }\n"

    graphviz_input += "}\n"
    return graphviz_input

def main():
    input_file = "./results/Events_Dependency.goal" 
    output_file = "./results/Events_Dependency.dot"

    # Parse the input file and generate the graph data
    graphs, task_infos = parse_goal_file(input_file)
    graphviz_input = generate_graphviz(graphs, task_infos)

    # Write the Graphviz output to the file
    with open(output_file, 'w') as file:
        file.write(graphviz_input)

    print(f"Graphviz output written to {output_file}")

    input_file = "./results/InGPU_MicroEvents_Dependency.goal" 
    output_file = "./results/InGPU_MicroEvents_Dependency.dot"

    # Parse the input file and generate the graph data
    graphs, task_infos = parse_goal_file(input_file)
    graphviz_input = generate_graphviz(graphs, task_infos)

    # Write the Graphviz output to the file
    with open(output_file, 'w') as file:
        file.write(graphviz_input)

    print(f"Graphviz output written to {output_file}")

    input_file = "./results/InterNode_MicroEvents_Dependency.goal" 
    output_file = "./results/InterNode_MicroEvents_Dependency.dot"

    # Parse the input file and generate the graph data
    graphs, task_infos = parse_goal_file(input_file)
    graphviz_input = generate_graphviz(graphs, task_infos)

    # Write the Graphviz output to the file
    with open(output_file, 'w') as file:
        file.write(graphviz_input)

    print(f"Graphviz output written to {output_file}")

if __name__ == "__main__":
    main()