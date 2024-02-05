import gradio as gr
import os
import random 
import json
import uuid
import datetime

rating_models = [
    'gpt-3.5-turbo (0-shot)',
    'gpt-4 (0-shot)',
    'gpt-3.5-turbo (1-shot)',
]

BATTLE_TARGETS = {
    'gpt-3.5-turbo (0-shot)': ['CoRAG-3.5 (0-shot)', 'CoRAG-3.5-causal (0-shot)'],
    'gpt-4 (0-shot)': ['CoRAG-4 (0-shot)'],
    'gpt-3.5-turbo (1-shot)': ['CoRAG-3.5-causal (1-shot)'],
}

DATA_FOLDER = 'data/minecraft/'
OUT_FOLDER = 'out/minecraft/'

def get_data(data_folder=DATA_FOLDER):
    while True:
        file = random.choice(os.listdir(data_folder))
        if not file.endswith('.json'):
            print(f"File {file} is not a json file")
            continue
        file_path = os.path.join(data_folder, file)
        with open(file_path, 'r') as f:
            context = json.load(f)
        
        baseline = random.choice(rating_models)
        if baseline not in context.keys():
            continue
        
        target = random.choice(BATTLE_TARGETS[baseline])
        if target not in context.keys():
            continue
        
        models = [baseline, target]
        random.shuffle(models)

        instruction = context['instruction']

        model_a_name, model_b_name = models

        model_a_response = random.choice(context[model_a_name])
        model_b_response = random.choice(context[model_b_name])
        break
    data = {
        # 'uuid': str(uuid.uuid4()),
        # 'abbr': file.replace('.json', ''),
        'instruction': instruction,
        'model_a': model_a_name,
        'model_a_response': model_a_response,
        'model_b': model_b_name,
        'model_b_response': model_b_response
        # 'judge': "Anonymous",
        # 'timestamp': datetime.datetime.now().isoformat()
    }
    return data

def save_data(data, out_folder=OUT_FOLDER):
    file_name = data['timestamp'] + '.json'
    out_file = os.path.join(out_folder, file_name)
    with open(out_file, 'w') as f:
        json.dump(data, f, indent = 4)

title="ELO Rating System"
# description="This is a simple ELO rating system for answers. It takes in the ELO ratings of the two players and the result of the game, and outputs the updated ELO ratings."

notice_markdown = """
# ⚔️  Chatbot Arena ⚔️ : Benchmarking LLMs in the Wild

## 📜 Rules
- Refresh to obtain question and its corresponding answers from two anonymous models.
- Vote for the better answer. And then click "New Round" to get a new question.
- If both answers are bad, vote for "Both are bad".
- If you want to skip, click "Skip".

## 📊 Principle
你可以从以下几个方面考察模型的表现：
1. **相关性**：回答是否与问题相关？
2. **准确性**：回答是否准确？比如crafting table是由4个木板合成的，而不是4个木头；diamond axe需要使用3个diamond和2个stick合成，而不是3个stick和2个diamond。
2. **完整性**：回答是否完整？比如从木头合成wooden pickaxe需要先合成木板再合成stick，最后才能合成pickaxe。中间步骤不可以被忽略
3. **可读性**：回答是否通顺？
5. **可执行性**：考虑到游戏的特性，回答是否可执行？

## 👇 Vote now!

"""

def newround_response(group):
    data = get_data()
    gr.update(elem_id='model_a_from', visible=False)
    gr.update(elem_id='model_b_from', visible=False)
    return data['instruction'], data['model_a'], data['model_a_response'], "[MASK]", data['model_b'], data['model_b_response'], "[MASK]" # visible

def leftvote_response(instruction, model_a_name, model_a_response, model_b_name, model_b_response):
    data = {
        'uuid': str(uuid.uuid4()),
        # 'abbr': file.replace('.json', ''),
        'model_a': model_a_name,
        'model_b': model_b_name,
        'judge': "Anonymous",
        'winner': 'model_a',
        'timestamp': datetime.datetime.now().isoformat(),
        'instruction': instruction,
        'model_a_response': model_a_response,
        'model_b_response': model_b_response,
    }
    save_data(data)
    # gr.update(elem_id="model_a_from", visible=True)
    # gr.update(elem_id="model_b_from", visible=True)
    return model_a_name, model_b_name 
    

def rightvote_response(instruction, model_a_name, model_a_response, model_b_name, model_b_response):
    data = {
        'uuid': str(uuid.uuid4()),
        # 'abbr': file.replace('.json', ''),
        'model_a': model_a_name,
        'model_b': model_b_name,
        'judge': "Anonymous",
        'winner': 'model_b',
        'timestamp': datetime.datetime.now().isoformat(),
        'instruction': instruction,
        'model_a_response': model_a_response,
        'model_b_response': model_b_response,
    }
    save_data(data)
    # gr.update(elem_id="model_a_from", visible=True)
    # gr.update(elem_id="model_b_from", visible=True)
    return model_a_name, model_b_name 

def tie_response(instruction, model_a_name, model_a_response, model_b_name, model_b_response):
    data = {
        'uuid': str(uuid.uuid4()),
        # 'abbr': file.replace('.json', ''),
        'model_a': model_a_name,
        'model_b': model_b_name,
        'judge': "Anonymous",
        'winner': 'tie',
        'timestamp': datetime.datetime.now().isoformat(),
        'instruction': instruction,
        'model_a_response': model_a_response,
        'model_b_response': model_b_response,
    }
    save_data(data)
    # gr.update(elem_id="model_a_from", visible=True)
    # gr.update(elem_id="model_b_from", visible=True)
    return model_a_name, model_b_name 

def bothbad_response(instruction, model_a_name, model_a_response, model_b_name, model_b_response):
    data = {
        'uuid': str(uuid.uuid4()),
        # 'abbr': file.replace('.json', ''),
        'model_a': model_a_name,
        'model_b': model_b_name,
        'judge': "Anonymous",
        'winner': 'bothbad',
        'timestamp': datetime.datetime.now().isoformat(),
        'instruction': instruction,
        'model_a_response': model_a_response,
        'model_b_response': model_b_response,
    }
    save_data(data)
    # gr.update(elem_id="model_a_from", visible=True)
    # gr.update(elem_id="model_b_from", visible=True)
    return model_a_name, model_b_name 

with gr.Blocks(title=title) as demo:

    init_data = get_data()
    init_visible_state = False

    gr.Markdown(notice_markdown)

    with gr.Row():
        group_drop = gr.Dropdown(
            ["Minecraft Planning", "Creative Writing"], 
            label="Task Group", 
            value = "Minecraft Planning",
            interactive=True
        )
        # update_task_btn = gr.Button("Update Group", scale=0.1)

    with gr.Row():
        instruction_box = gr.Textbox(label="Instruction", value = init_data['instruction'], interactive=True)
    
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            model_A_response = gr.Textbox(label="Model A Response:", value = init_data['model_a_response'], visible = True, interactive=False)
            hidden_A_name = gr.Textbox(elem_id="model_a_from", label="Model A From:", value=init_data['model_a'], visible=False, interactive=False)
            model_A_name = gr.Textbox(elem_id="model_a_from", label="Model A From:", value="[MASK]", visible=True, interactive=False)
            # model_A_name = gr.Markdown(elem_id="model_a_from", label="A From:", value=init_data['model_a'], visible=True)
        with gr.Column(scale=1, min_width=600):
            model_B_response = gr.Textbox(label="Model B Response:", value = init_data['model_b_response'], visible = True, interactive=False)
            hidden_B_name = gr.Textbox(elem_id="model_b_from", label="Model B From:", value=init_data['model_b'], visible=False, interactive=False)
            model_B_name = gr.Textbox(elem_id="model_a_from", label="Model A From:", value="[MASK]", visible=True, interactive=False)
            # model_B_name = gr.Markdown(elem_id="model_b_from", label="B From:", value=init_data['model_b'], visible=True)

    # print(model_A_name.value, model_B_name.value)

    # gr.update(model_A_name, vars = "hello")

    with gr.Row():
        leftvote_btn = gr.Button(
            value="👈  A is better", visible=True, interactive=True
        )
        rightvote_btn = gr.Button(
            value="👉  B is better", visible=True, interactive=True
        )
        tie_btn = gr.Button(value="🤝  Tie", visible=True, interactive=True)
        bothbad_btn = gr.Button(
            value="👎  Both are bad", visible=True, interactive=True
        )

    with gr.Row():
        skip_btn = gr.Button(
            value="👋  Skip", visible=True, interactive=True
        )
        new_round_btn = gr.Button(
            value="🔄  New Round", visible=True, interactive=True
        )

    # # Register listeners
    # btn_list = [
    #     leftvote_btn,
    #     rightvote_btn,
    #     tie_btn,
    #     bothbad_btn,
    # ]
    leftvote_btn.click(
        fn = leftvote_response,
        inputs = [instruction_box, hidden_A_name, model_A_response, hidden_B_name, model_B_response],
        outputs = [model_A_name, model_B_name]
        # outputs= [model_A_name, model_B_name]
    )
    rightvote_btn.click(
        fn = rightvote_response,
        inputs = [instruction_box, hidden_A_name, model_A_response, hidden_B_name, model_B_response],
        outputs = [model_A_name, model_B_name]
        # outputs= [model_A_name, model_B_name]
    )
    tie_btn.click(
        fn = tie_response,
        inputs = [instruction_box, hidden_A_name, model_A_response, hidden_B_name, model_B_response],
        outputs = [model_A_name, model_B_name]
    )
    bothbad_btn.click(
        fn = bothbad_response,
        inputs = [instruction_box, hidden_A_name, model_A_response, hidden_B_name, model_B_response],
        outputs = [model_A_name, model_B_name]
    )
    new_round_btn.click(
        fn = newround_response,
        inputs = [group_drop],
        outputs= [instruction_box, hidden_A_name, model_A_response, model_A_name, hidden_B_name, model_B_response, model_B_name]
    )
    skip_btn.click(
        fn = newround_response,
        inputs = [group_drop],
        outputs= [instruction_box, hidden_A_name, model_A_response, model_A_name, hidden_B_name, model_B_response, model_B_name]
    )

    # 将可见性状态与 model_A_name 和 model_B_name 的 visible 参数绑定
    # visibility_state.bind_to(model_A_name, "visible")
    # visibility_state.bind_to(model_B_name, "visible")


demo.launch()