from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import json

app = FastAPI()

model_server_address = "http://localhost:8000"

class EssayEvaluationRequest(BaseModel):
    prompt_id: int
    model_raw_output: str
    student_id: str
    model_name: str 

class EssayEvaluationResponse(BaseModel):
    criticism: str
    student_id: str
    prompt_id: int

@app.post("/evaluate", response_model=EssayEvaluationResponse)
async def evaluate_essay(request: EssayEvaluationRequest):
    try:
        input_text = f"Generate criticism for essay based on a user prompt: {request.model_raw_output}"
        
        if request.model_name not in ["phi-2", "gemma"]:
            raise HTTPException(status_code=400, detail="Unsupported model name")

        model_server_path = f"/v2/models/{request.model_name}/versions/1/infer"

        triton_request = {
            "inputs": [{
                "name": "input_text",
                "shape": [1, len(input_text)],
                "datatype": "STRING",
                "data": [input_text]
            }],
            "outputs": [{
                "name": "output_text"
            }]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                model_server_address + model_server_path,
                data=json.dumps(triton_request)
            )
        
        response.raise_for_status()  

        output_text = response.json().get("outputs", [{}])[0].get("data", ["No response"])[0]

        return EssayEvaluationResponse(
            criticism=output_text,
            student_id=request.student_id,
            prompt_id=request.prompt_id
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
