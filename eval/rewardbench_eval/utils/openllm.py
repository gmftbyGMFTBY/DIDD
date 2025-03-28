import json, re, torch, ipdb
from tqdm import tqdm
from lmdeploy.serve.openai.api_client import APIClient
from .openai_utils import *
#from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModel
from transformers import pipeline, LlamaTokenizer, LlamaForCausalLM
from .constants_prompt import *


ultracm_instruction_template = """Given my answer to an instruction, your role is to provide specific and constructive feedback for me. You should find the best way for me to learn from your feedback and improve my performance. 

You should consider multiple aspects of my answer, including helpfulness, truthfulness, honesty, and to what extent the answer follows instructions.
---

### Instruction
{instruction}

### Answer
{completion}
---

Please act as a teacher and provide specific and constructive feedback. Besides describing the weaknesses of the answer, you should also provide specific suggestions to guide me toward understanding how to improve. Please note, however, that your suggestions should help me better complete the instructions, but you should not introduce new requirements that are not mentioned in the instructions. Your feedback should focus on enhancing my ability to think critically and respond accurately. However, never explicitly provide the reference answer, nor do polite phrases be required. Only respond with concise feedback in chat style. Finally, score the overall quality of the answer from 1 to 10, where 1 is the worst and 10 is the best.

*Format*
### Feedback
Overall Score: [1-10]
[Your feedback]

---

### Feedback
Overall Score: 
"""

def prepare_prompt_comp(prompt, prompt_, chosen, reject):
    conversation = f'[begin of conversation] user: {prompt_} [end of conversation]'
    ipt = prompt.format(conversation=conversation, responsea=chosen, responseb=reject)
    return [{'role': 'user', 'content': ipt}]


def prepare_prompt_comp_reward_model(prompt, response):
    return [{'role': 'user', 'content': prompt}, {'role':'assistant', 'content': response}]

def prepare_prompt_comp_api_model(prompt, item):
    llm_name = 'gpt-4o'
    conversation = f'[begin of conversation] user: {item["prompt"]} [end of conversation]'
    ipt = prompt.format(conversation=conversation, responsea=item['response 1'], responseb=item['response 2'])
    return [
        {
            'role': 'user',
            'content': ipt
        }
    ]

def prepare_prompt_ultracm(query, response):
    system_prompt = "User: A one-turn chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, very detailed, and polite answers to the user's questions.</s>"
    conv = [system_prompt]
    conv.append("User: " + ultracm_instruction_template.format(
        instruction=query,
        completion=response,
    ) + "</s>")
    conv.append("Assistant: ")
    prompt = "\n".join(conv)
    return prompt


def prepare_prompt_autoj(query, response_1, response_2):
    input_pairwise = build_autoj_input(prompt=query,
        resp1 = response_1,  resp2 = response_2, 
        protocol = "pairwise_tie")
    return [{'role': 'user', 'content': input_pairwise}]

class OpenLLM:

    def __init__(self, model_name):
        self.model_name = model_name
        #backend_config = PytorchEngineConfig(session_len=32768, tp=1)
        if model_name in ['deepseek-v3', 'deepseek-r1']:
            self.model_name = model_name
        elif model_name == 'auto-j-13b':
            model_name = '/home/lt/models/auto-j-13b'
            backend_config = PytorchEngineConfig(session_len=32768, tp=2)
            self.gen_config = GenerationConfig(temperature=0.8, max_new_tokens=1024, top_k=50, top_p=1.0)
            self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name='llama2'))
        elif model_name == 'ultracm-13b':
            model_name = '/home/lt/models/openbmb/UltraCM-13b'
            self.tokenizer = LlamaTokenizer.from_pretrained(model_name)
            self.model = LlamaForCausalLM.from_pretrained(model_name, device_map="auto")
            self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        elif 'llama' in model_name.lower():
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
        #self.gen_config = GenerationConfig(temperature=0.6, max_new_tokens=2048, top_k=50, top_p=0.95)
        #self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name=model_base_name))
        self.prompt = open('prompts/pairwise_critique.md').read()

    @torch.no_grad()
    def batch_chat_ultracm(self, msgs, bsz=4):
        outputs = []
        prompts = [msg['prompt'] for msg in msgs]
        chosens = [msg['chosen'] for msg in msgs]
        rejects = [msg['rejected'] for msg in msgs]
        for prompt, chosen, reject in tqdm(list(zip(prompts, chosens, rejects))):
            msgs_chosen = prepare_prompt_ultracm(prompt, chosen)
            msgs_rejected = prepare_prompt_ultracm(prompt, reject) 

            with torch.no_grad():
                response = self.generator(msgs_chosen, num_return_sequences=1, return_full_text=False, handle_long_generation="hole", temperature=0.5, top_p=1.0, max_new_tokens=8, repetition_penalty=1.2, do_sample=False)
                response_a = response[0]["generated_text"].strip("\n").strip()

            with torch.no_grad():
                response = self.generator(msgs_rejected, num_return_sequences=1, return_full_text=False, handle_long_generation="hole", temperature=0.5, top_p=1.0, max_new_tokens=8, repetition_penalty=1.2, do_sample=False)
                response_b = response[0]["generated_text"].strip("\n").strip()

            outputs.append(response_a + '\n=====\n=====\n' + response_b)
        return outputs

    @torch.no_grad()
    def batch_chat_autoj(self, msgs, bsz=32):
        index = 0
        pbar = tqdm(total=len(msgs))
        outputs = []
        while index < len(msgs):
            prompts = msgs[index:index+bsz]['prompt']
            chosens = msgs[index:index+bsz]['chosen']
            rejects = msgs[index:index+bsz]['rejected']
            msgs_ = [prepare_prompt_autoj(prompt, chosen, reject) for prompt, chosen, reject in zip(prompts, chosens, rejects)]
            responses = self.pipe(msgs_, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            outputs.extend(responses)
            pbar.update(len(msgs_))
            index += bsz 
        return outputs

    @torch.no_grad()
    def batch_chat_api_model(self, msgs, bsz=1):
        index = 0
        pbar = tqdm(total=len(msgs))
        outputs = []
        while index < len(msgs):
            msgs_ = [prepare_prompt_comp_api_model(self.prompt, sample) for sample in msgs[index:index+bsz]]
            responses = batch_chat(msgs_, model_name=self.model_name)
            outputs.extend(responses)
            pbar.update(len(msgs_))
            index += bsz 
        return outputs

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

    @torch.no_grad()
    def batch_chat_reward_model(self, msgs, bsz=1):
        outputs_ = []
        for response_name in ['chosen', 'rejected']:
            index = 0
            pbar = tqdm(total=len(msgs))
            outputs = []
            while index < len(msgs):
                prompts = msgs[index:index+bsz]['prompt']
                chosens = msgs[index:index+bsz]['chosen']
                rejects = msgs[index:index+bsz]['rejected']
                if response_name == 'chosen':
                    msgs_ = [prepare_prompt_comp_reward_model(prompt, response) for prompt, response in zip(prompts, chosens)]
                else:
                    msgs_ = [prepare_prompt_comp_reward_model(prompt, response) for prompt, response in zip(prompts, chosens)]
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
                ipdb.set_trace()
            outputs_.append(outputs)
        rests = []
        for a, b in zip(outputs_[0], outputs_[1]):
            if a > b:
                rests.append('Label: A')
            else:
                rests.append('Label: B')
        return rests
