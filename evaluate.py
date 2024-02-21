import json 
import os  

import trueskill

env = trueskill.TrueSkill(draw_probability=0.1)  # 可以根据实际情况调整平局概率
agents = [env.create_rating(), env.create_rating(), env.create_rating(),env.create_rating(),env.create_rating()]

# agent_names = ['CoRAG-3.5 (0-shot)', 'CoRAG-3.5-causal (0-shot)', 'gpt-3.5-turbo (0-shot)']
agent_names = ['CoRAG', 'RAG-1', 'RAG-5', 'DIRECT', 'COT']

group = "all"
instructions = []

with open('creative.json', 'r') as f:
    tasks = json.load(f)
    for task in tasks:
        if group == "all":
            instructions.append(task['question'])
        if task['group'] == group:
            instructions.append(task['question'])

logs_dir = './out/creative'
for file in os.listdir(logs_dir):
    if file.endswith('.json'):
        with open(os.path.join(logs_dir, file)) as f:
            data = json.load(f)
        instruction = data['instruction']
        if instruction not in instructions:
            continue

        model_A = data['model_a']
        model_B = data['model_b']
        winner = data['winner']
        if model_A and model_B in agent_names:
            a_index = agent_names.index(model_A)
            b_index = agent_names.index(model_B)
            if winner == 'model_a':
                agents[a_index], agents[b_index] = env.rate_1vs1(agents[a_index], agents[b_index])
            elif winner == 'model_b':
                agents[b_index], agents[a_index] = env.rate_1vs1(agents[b_index], agents[a_index])
            elif winner == 'tie': 
                agents[a_index], agents[b_index] = env.rate_1vs1(agents[a_index], agents[b_index], drawn = True)
            else:
                pass

print(f"Group Name: {group}")
for i, rate in enumerate(agents):
    print(agent_names[i], rate.mu, rate.sigma)


win_rates = {
    "CoRAG": [],
    "RAG-1": [],
    "RAG-5": [],
    "DIRECT": [],
    "COT": []
}

logs_dir = './out/creative'
for file in os.listdir(logs_dir):
    if file.endswith('.json'):
        with open(os.path.join(logs_dir, file)) as f:
            data = json.load(f)
        model_A = data['model_a']
        model_B = data['model_b']
        winner = data['winner']

        if winner == 'model_a':
            win_rates[model_B].append(0)
            win_rates[model_A].append(1)
        elif winner == 'model_b':
            win_rates[model_B].append(1)
            win_rates[model_A].append(0)
        else:
            pass
        

for k, v in win_rates.items():
    print(k, sum(v) / len(v))


