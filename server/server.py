from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains.llm import LLMChain
import torch
import os
import logging

app = FastAPI()

if not os.path.exists('logs'):
    os.makedirs('logs')
    print("Logs directory created successfully!")

logging.basicConfig(level=logging.INFO, filename='logs/server.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

model_name = os.getenv("MODEL_NAME", "microsoft/phi-2")
logger.info(f"Using model: {model_name}")

prompt_dict = {
    0: "Write an explanatory essay to inform fellow citizens about the advantages of limiting car usage. Your essay must be based on ideas and information that can be found in the passage set. Manage your time carefully so that you can read the passages",
    1: "Write a letter to your state senator in which you argue in favor of keeping the Electoral College or changing to election by popular vote for the president of the United States. Use the information from the texts in your essay. Manage your time carefully so that you can read the passages"
}

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map='auto',
    torch_dtype=torch.bfloat16
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=1024,
    temperature=0.4
)

pipe.model.config.pad_token_id = pipe.model.config.eos_token_id

local_llm = HuggingFacePipeline(pipeline=pipe)

template = """You a response evaluator. You are tasked with generating criticisms for the relevance of an essay or letter written below as per the question asked:
### Question:
{prompt}

### Answer:
{instruction}

Evaluation:"""

prompt = PromptTemplate(template=template, input_variables=["prompt", "instruction"])
llm_chain = LLMChain(prompt=prompt, llm=local_llm)

class EssayEvaluationRequest(BaseModel):
    prompt_id: int
    essay_output: str
    student_id: str

class EssayEvaluationResponse(BaseModel):
    criticism: str
    student_id: str
    prompt_id: int

@app.post("/evaluate", response_model=EssayEvaluationResponse)
async def evaluate_essay(request: EssayEvaluationRequest):
    try:
        logger.info(f"Received request for prompt_id={request.prompt_id}, student_id={request.student_id}")


        input_dict = {
            "prompt": prompt_dict[request.prompt_id],  
            "instruction": request.essay_output  
        }
        result = llm_chain.invoke(input_dict)  
        logger.info("Successfully generated a response: ", result)
        return EssayEvaluationResponse(criticism=result, student_id=request.student_id, prompt_id=request.prompt_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
