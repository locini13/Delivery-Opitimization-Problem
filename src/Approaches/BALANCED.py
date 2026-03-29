import csv

word_to_number = {
    "one": 1, "two": 2, "three": 3,
    "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9,
    "ten": 10
}

def parse_distance(value):
    try:
        value = value.strip().lower().replace("km", "").strip()
        if value in word_to_number:
            return float(word_to_number[value])
        return float(value)
    except:
        return None

priority_order = {'High': 1, 'Medium': 2, 'Low': 3}

deliveries = []

with open('../data/sample1.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        distance = parse_distance(row['Distance'])
        if distance is None:
            continue
        deliveries.append({
            'id': row['LocationID'],
            'distance': distance,
            'priority': row['Priority']
        })

# Sort (descending helps best results)
deliveries.sort(key=lambda x: (priority_order[x['priority']], -x['distance']))

agents = {a: {'tasks': [], 'total_distance': 0} for a in ['A', 'B', 'C']}

# Balanced assignment
for d in deliveries:
    best_agent = None
    best_balance = float('inf')

    for agent in agents:
        # simulate
        agents[agent]['tasks'].append(d['id'])
        agents[agent]['total_distance'] += d['distance']

        distances = [agents[a]['total_distance'] for a in agents]
        balance = max(distances) - min(distances)

        # undo
        agents[agent]['tasks'].pop()
        agents[agent]['total_distance'] -= d['distance']

        if balance < best_balance:
            best_balance = balance
            best_agent = agent

    # assign
    agents[best_agent]['tasks'].append(d['id'])
    agents[best_agent]['total_distance'] += d['distance']

print("\n--- BALANCED METHOD ---\n")
for a, d in agents.items():
    print(f"{a}: {d['tasks']} → {d['total_distance']} km")