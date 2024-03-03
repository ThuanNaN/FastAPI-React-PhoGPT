import argparse
from typing import List, Dict
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model import ModelPredictor


class Instruction_Request(BaseModel):
    input_prompt: str

class Chat_Request(BaseModel):
    input_prompt:  List[Dict[str, str]]

class Response(BaseModel):
    text: str


class API_Predictor:
    def __init__(self, 
                 predictors:  Dict[str, ModelPredictor], 
                 origin_urls: List[str]
                 ):
        
        self.predictors = predictors
        self.app = FastAPI()
        self.init_middleware(origin_urls)

        @self.app.get("/")
        def health():
            return "OK"
        
        @self.app.post(f"/instruction", response_model=Response)
        def instruction_predict(request: Instruction_Request):
            response = self.predictors["instruction"](request.input_prompt)
            return Response(text=response)

        @self.app.post(f"/chat", response_model=Response)
        def chat_predict(request: Chat_Request):
            response = self.predictors["chat"](request.input_prompt)
            return Response(text=response)


    def run(self, host: str = "0.0.0.0", port: int = 5000):
        uvicorn.run(self.app, host=host, port=port)

    def init_middleware(self, origins: List[str]):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="vinai/PhoGPT-4B-Chat")
    parser.add_argument("--task", type=str, default="instruction")
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    predictors = {
        "instruction": ModelPredictor(args.model_name, "instruction", args.device),
        "chat": ModelPredictor(args.model_name, "chat", args.device)
    }

    api_predictor = API_Predictor(predictors, origins)
    api_predictor.run(args.host, args.port)

