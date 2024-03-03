from typing import List, Dict, Union
import torch
from transformers import BitsAndBytesConfig, AutoConfig, AutoModelForCausalLM, AutoTokenizer


class ModelPredictor:
    def __init__(self, model_name: str, task: str, device: str = "cuda"):
        self.model_name = model_name    
        self.task = task
        self.device = device
        self.model = self.get_model()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.generate_kwargs = {
            "do_sample": True,
            "temperature": 1.0,
            "top_k": 50,
            "top_p": 0.9,
            "max_new_tokens": 1024,
            "eos_token_id": self.tokenizer.eos_token_id, 
            "pad_token_id": self.tokenizer.pad_token_id,
        }
    
    @torch.inference_mode()
    def __call__(self, prompt: Union[str, List[Dict[str, str]]]):
        if self.task == "instruction":
            input_prompt = f"### Câu hỏi: {prompt}\n### Trả lời:"   
        elif self.task == "chat":
            input_prompt = self.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
        else:
            raise ValueError(f"Task {self.task} is not supported")

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")
        outputs = self.model.generate(  
            inputs=input_ids["input_ids"].to(self.device),  
            attention_mask=input_ids["attention_mask"].to(self.device),  
            **self.generate_kwargs
        ).detach().cpu().numpy()
        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0] 
        torch.cuda.empty_cache()
        return response.split("### Trả lời:")[-1]
        
    
    def get_model(self):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
        config = AutoConfig.from_pretrained(self.model_name, trust_remote_code=True)
        config.init_device = "cuda"
        model_path = f"./model_repository/{self.model_name}"
        model = AutoModelForCausalLM.from_pretrained(model_path, 
                                            quantization_config=quantization_config, 
                                            config=config, 
                                            trust_remote_code=True,
                                            low_cpu_mem_usage=True)
        return model.eval()
