import json, re, torch, ipdb
from tqdm import tqdm
from lmdeploy.serve.openai.api_client import APIClient
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig
from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification


def prepare_prompt_comp(prompt, item):
    conversation = f'[begin of conversation] user: {item["prompt"]} [end of conversation]'
    ipt = prompt.format(conversation=conversation, responsea=item['response 1'], responseb=item['response 2'])
    return [{'role': 'user', 'content': ipt}]

def prepare_prompt_comp_reward_model(prompt, item, response_name):
    return [{'role': 'user', 'content': item['prompt']}, {'role':'assistant', 'content': item[response_name]}]


class OpenLLM:

    def __init__(self, model_name):
        self.model_name = model_name
        backend_config = PytorchEngineConfig(session_len=32768, tp=1)

        if 'llama' in model_name.lower():
            model_base_name = 'llama3'
        elif 'qwen' in model_name.lower():
            model_base_name = 'qwen'
        elif model_name == 'internlm2-20b-reward':
            self.model = AutoModel.from_pretrained("/home/lt/reward_models/internlm/internlm2-20b-reward",torch_dtype=torch.float16,device_map='auto',trust_remote_code=True)
            self.tokenizer = AutoTokenizer.from_pretrained("/home/lt/reward_models/internlm/internlm2-20b-reward", trust_remote_code=True) 
        elif model_name == 'skywork-reward-8b':
            self.device = "cuda:0"
            model_name = '/home/lt/reward_models/Skywork-Reward-Llama-3.1-8B'
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                torch_dtype=torch.bfloat16,
                device_map=self.device,
                num_labels=1,
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
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

    @torch.no_grad()
    def batch_chat_reward_model(self, msgs, bsz=1):
        outputs_ = []
        for response_name in ['response 1', 'response 2']:
            index = 0
            pbar = tqdm(total=len(msgs))
            outputs = []
            while index < len(msgs):
                msgs_ = [prepare_prompt_comp_reward_model(self.prompt, sample, response_name) for sample in msgs[index:index+bsz]]
                if self.model_name == 'internlm2-20b-reward':
                    responses = self.model.get_scores(self.tokenizer, msgs_)
                    if type(responses) == float:
                        responses = [responses]
                else:
                    responses = []
                    for msgs_one in msgs_:
                        conv1_formatted = self.tokenizer.apply_chat_template(msgs_one, tokenize=False)
                        conv1_tokenized = self.tokenizer(conv1_formatted, return_tensors="pt").to(self.device)
                        with torch.no_grad():
                            score = self.model(**conv1_tokenized).logits[0][0].item()
                        responses.append(score)
                outputs.extend(responses)
                pbar.update(len(msgs_))
                index += bsz 
            outputs_.append(outputs)
        rests = []
        for a, b in zip(outputs_[0], outputs_[1]):
            if a > b:
                rests.append('Label: A')
            else:
                rests.append('Label: B')
        return rests 
