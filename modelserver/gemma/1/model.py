import numpy as np
import triton_python_backend_utils as pb_utils
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import itertools

class TritonPythonModel:
    
    def initialize(self, args):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = AutoModelForCausalLM.from_pretrained("google/gemma-7b", torch_dtype="auto", trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b", trust_remote_code=True).to(self.device)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def execute(self, requests):
    
        input_list = []
        for request in requests:
            inp = pb_utils.get_input_tensor_by_name(request, "input_text")
            input = inp.as_numpy().astype(str)
            input = list(itertools.chain(*input))
            input_list.extend(input)
        
        input_ids = self.tokenizer(
                    input_list,
                    padding=True,
                    truncation=True,
                    return_tensors='pt'
                ).to(self.device)
        
        with torch.no_grad():
                outputs = self.model.generate(**input_ids)
        outputs_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        responses = []
        start_idx = 0
        for request in requests:
            inp = pb_utils.get_input_tensor_by_name(request, "input_text")
            num_texts = inp.as_numpy().shape[0]
            end_idx = start_idx + num_texts
            batch_response_text = outputs_text[start_idx:end_idx]

            inference_response = pb_utils.InferenceResponse(output_tensors=[
                pb_utils.Tensor(
                    "output_text",
                    np.array([s.encode('utf-8') for s in batch_response_text])
                )
            ])

            responses.append(inference_response)
            start_idx = end_idx


        return responses
