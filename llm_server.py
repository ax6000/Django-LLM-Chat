from fastapi import FastAPI, WebSocket
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

model_name = "あなたのLLMモデル名"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to("cuda")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        input_ids = tokenizer.encode(data, return_tensors="pt").to("cuda")
        with torch.no_grad():
            output = model.generate(input_ids, max_length=100)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        await websocket.send_text(response)