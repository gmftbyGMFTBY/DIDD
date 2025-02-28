import json, re, torch, ipdb
from tqdm import tqdm
from lmdeploy.serve.openai.api_client import APIClient
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig


def prepare_prompt_comp(prompt, prompt_, chosen, reject):
    conversation = f'[begin of conversation] user: {prompt_} [end of conversation]'
    ipt = prompt.format(conversation=conversation, responsea=chosen, responseb=reject)
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
        self.gen_config = GenerationConfig(temperature=0.6, max_new_tokens=2048, top_k=50, top_p=0.95)
        self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name=model_base_name))
        self.prompt = open('prompts/pairwise_critique.md').read()

    @torch.no_grad()
    def batch_chat(self, msgs, bsz=32):
        index = 0
        pbar = tqdm(total=len(msgs))
        outputs = []
        while index < len(msgs):
            prompts = msgs[index:index+bsz]['prompt']
            chosens = msgs[index:index+bsz]['chosen']
            rejects = msgs[index:index+bsz]['rejected']
            msgs_ = [prepare_prompt_comp(self.prompt, prompt, chosen, reject) for prompt, chosen, reject in zip(prompts, chosens, rejects)]
            responses = self.pipe(msgs_, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            outputs.extend(responses)
            pbar.update(len(msgs_))
            index += bsz 
        return outputs
