from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Workflow import Workflow
import pickle
from typing import Dict, Any

import warnings
warnings.filterwarnings("ignore")

app = FastAPI()

class InputData(BaseModel):
    data: Dict

@app.post("/predict")
async def predict(input_data:InputData):
    try:
        
       graph = Workflow()
       inputs = input_data.data
       response= graph.execute(inputs)
       

       return {"predictions": response.get("final_response",None)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))