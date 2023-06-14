import os

CWD = os.path.dirname(os.path.realpath(__file__))

def load_prompts():
    prompts = {}
    for filename in os.listdir(CWD):
        if filename.endswith('.txt'):
            with open(os.path.join(CWD, filename), 'r') as f:
                prompts[filename.split('.')[0]] = f.read()
    return prompts

PROMPTS = load_prompts()