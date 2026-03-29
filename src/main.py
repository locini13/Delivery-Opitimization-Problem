import csv
import matplotlib.pyplot as plt
import os

# --- Word → Number Mapping ---
word_to_number = {
    "one": 1, "two": 2, "three": 3,
    "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9,
    "ten": 10
}

# --- Distance Parser ---
def parse_distance(value):
    try:
        if not value or value.strip() == "":
            return None
        value = value.lower().replace("km", "").strip()
        if value in word_to_number:
            return float(word_to_number[value])
        return float(value)
    except:
        return None

# --- Read CSV ---
deliveries = []
skipped_rows = []

with open('../data/sample1.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        distance = parse_distance(row['Distance'])
        if distance is None:
            skipped_rows.append(row)
            continue
        deliveries.append({
            'id': row['LocationID'],
            'distance': distance,
            'priority': row['Priority']
        })

# --- Priority Mapping ---
priority_order = {'High': 1, 'Medium': 2, 'Low': 3}

# --- Greedy Assignment Helper ---
def assign_greedy(sorted_deliveries):
    agents = {
        'A': {'tasks': [], 'total_distance': 0},
        'B': {'tasks': [], 'total_distance': 0},
        'C': {'tasks': [], 'total_distance': 0}
    }
    for d in sorted_deliveries:
        agent = min(agents, key=lambda x: agents[x]['total_distance'])
        agents[agent]['tasks'].append(d['id'])
        agents[agent]['total_distance'] += d['distance']
    return agents

# --- Algorithms ---
def greedy_algorithm(deliveries):
    sorted_deliveries = sorted(deliveries, key=lambda x: (priority_order.get(x['priority'], 4), x['distance']))
    return assign_greedy(sorted_deliveries)

def descending_greedy_algorithm(deliveries):
    sorted_deliveries = sorted(deliveries, key=lambda x: (priority_order.get(x['priority'], 4), -x['distance']))
    return assign_greedy(sorted_deliveries)

def balanced_algorithm(deliveries):
    # Use descending + greedy as heuristic for balanced assignment
    return descending_greedy_algorithm(deliveries)

# --- Run All Algorithms ---
results = {}
algorithms = {
    'Greedy': greedy_algorithm,
    'Descending + Greedy': descending_greedy_algorithm,
    'Balanced': balanced_algorithm
}

for name, func in algorithms.items():
    agents = func(deliveries)
    total_distances = [agents[a]['total_distance'] for a in agents]
    max_min_diff = max(total_distances) - min(total_distances)
    results[name] = {'agents': agents, 'max_min_diff': max_min_diff}

# --- Determine Optimal ---
optimal_algo = min(results, key=lambda x: results[x]['max_min_diff'])
optimal_agents = results[optimal_algo]['agents']

# --- Ensure Output Folder Exists ---
os.makedirs('output', exist_ok=True)

# --- Save Text Output ---
output_file = os.path.join('output', 'output.txt')
with open(output_file, 'w') as f:
    for name, res in results.items():
        agents = res['agents']
        f.write(f"--- {name} ---\n\n")
        f.write("========== DELIVERY PLAN ==========\n")
        for agent, data in agents.items():
            f.write(f"Agent {agent}\n")
            f.write(f"  Deliveries     : {', '.join(data['tasks'])}\n")
            f.write(f"  Total Distance : {data['total_distance']} km\n\n")
        f.write(f"Difference (Balance Gap) : {res['max_min_diff']}\n")
        if name == optimal_algo:
            f.write("This is the Optimal Algorithm (Minimum Distance Gap)\n")
        f.write("-"*50 + "\n")

# --- Display All Algorithms ---
for name, res in results.items():
    agents = res['agents']
    print(f"\n--- {name} ---\n")
    print("========== DELIVERY PLAN ==========")
    for agent, data in agents.items():
        print(f"Agent {agent}")
        print(f"  Deliveries     : {', '.join(data['tasks'])}")
        print(f"  Total Distance : {data['total_distance']} km\n")
    print(f"Difference (Balance Gap) : {res['max_min_diff']}")
    if name == optimal_algo:
        print("This is the Optimal Algorithm (Minimum Distance Gap)")
    print("-"*50)

# --- Visualization ---
def visualize_agents(results, save_path):
    agents_names = ['A', 'B', 'C']
    fig, ax = plt.subplots(figsize=(10,6))
    bar_width = 0.2
    x = range(len(agents_names))

    for i, algo_name in enumerate(results):
        agents = results[algo_name]['agents']
        heights = [agents[a]['total_distance'] for a in agents_names]
        ax.bar([p + bar_width*i for p in x], heights, width=bar_width, label=algo_name)

    ax.set_xticks([p + bar_width for p in x])
    ax.set_xticklabels(agents_names)
    ax.set_ylabel('Total Distance (km)')
    ax.set_title('Total Distance per Agent for Each Algorithm')
    ax.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

# Save visualization
visualize_agents(results, os.path.join('output', 'delivery_plan_visual.png'))
print(f"\nText output saved to {output_file}")
print(f" Visualization saved to output/delivery_plan_visual.png")