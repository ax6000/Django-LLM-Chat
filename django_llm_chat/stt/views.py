from django.shortcuts import render

# Create your views here.
import asyncio
import websockets
import sounddevice as sd
import numpy as np
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# processor = WhisperProcessor.from_pretrained("openai/whisper-small")
# model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
model_id = "kotoba-tech/kotoba-whisper-v1.1"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model_kwargs = {"attn_implementation": "sdpa"} if torch.cuda.is_available() else {}
generate_kwargs = {"language": "japanese", "task": "transcribe"}


# pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base", device=0)
pipe = pipeline(
    model=model_id,
    torch_dtype=torch_dtype,
    device=device,
    model_kwargs=model_kwargs,
#     chunk_length_s=15,
    # batch_size=16,
    trust_remote_code=True,
    stable_ts=True,
    punctuator=True
)

@csrf_exempt
async def websocket_view(request):
    if request.method == 'GET':
        return HttpResponse("WebSocket server is running.")
    
    async def receive_audio():
        async with websockets.connect('ws://localhost:8000/ws/') as websocket:
            while True:
                audio_data = await websocket.recv()
                audio_array = np.frombuffer(audio_data, dtype=np.float32)
                # input_features = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
                # predicted_ids = model.generate(input_features)
                # transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
                sample = audio_array
                transcription = pipe(sample, return_timestamps=True, generate_kwargs=generate_kwargs)
                await websocket.send(transcription)

    await receive_audio()