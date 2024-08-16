from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def chat_page(request):
    return render(request, 'chats/chat.html')

@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # ここにチャットボットのロジックを実装します
        bot_response = f"あなたのメッセージ: {user_message}"
        
        return JsonResponse({'response': bot_response})
    return JsonResponse({'error': '無効なリクエストです'}, status=400)