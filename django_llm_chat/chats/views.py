from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import asyncio
import websockets

def chat_page(request):
    return render(request, 'chats/chat.html')

# @csrf_exempt
# def chat_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message', '')
        
#         # ここにチャットボットのロジックを実装します
#         bot_response = f"あなたのメッセージ: {user_message}"
        
#         return JsonResponse({'response': bot_response})
#     return JsonResponse({'error': '無効なリクエストです'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def chat_response(request):
    message = json.loads(request.body).get('message', '')
    
    try:
        response = asyncio.run(send_message_to_pc2(message))
        return JsonResponse({'response': response})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

async def send_message_to_pc2(message):
    uri = "ws://PC2のIPアドレス:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
    return response