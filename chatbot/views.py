from django.shortcuts import render
from django.http import JsonResponse
from .utils import send_message_to_gemini

def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        conversation_id = request.session.get('conversation_id', None)
        response = send_message_to_gemini(user_message, conversation_id)

        # Update session with conversation_id for context
        if 'conversation_id' in response:
            request.session['conversation_id'] = response['conversation_id']

        bot_reply = response.get('reply', "Sorry, I couldn't process that.")
        return JsonResponse({"reply": bot_reply})

    return render(request, 'chatbot.html')
