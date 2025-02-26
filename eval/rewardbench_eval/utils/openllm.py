import json, re, torch, ipdb
from tqdm import tqdm
from lmdeploy.serve.openai.api_client import APIClient
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig


def prepare_prompt_comp(prompt, item):
    conversation = f'[begin of conversation] user: {item["prompt"]} [end of conversation]'
    ipt = prompt.format(conversation=conversation, responsea=item['chosen'], responseb=item['rejected'])
    return [{'role': 'user', 'content': ipt}]


class OpenLLM:

    def __init__(self, model_name):
        self.model_name = model_name
        backend_config = PytorchEngineConfig(session_len=32768, tp=1)
        if 'llama' in model_name.lower():
            model_base_name = 'llama3'
        elif 'qwen' in model_name.lower():
            model_base_name = 'qwen'
        else:
            model_base_name = 'internlm2'
        self.gen_config = GenerationConfig(temperature=0.0, max_new_tokens=2048)
        self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name=model_base_name))
        self.prompt = open('prompts/pairwise_critique.md').read()

    @torch.no_grad()
    def batch_chat(self, msgs, bsz=32):
        index = 0
        pbar = tqdm(total=len(msgs))
        outputs = []
        while index < len(msgs):
            msgs_ = [prepare_prompt_comp(self.prompt, sample) for sample in msgs[index:index+bsz]]
            responses = self.pipe(msgs_, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            outputs.extend(responses)
            pbar.update(len(msgs_))
            index += bsz 
        return outputs
