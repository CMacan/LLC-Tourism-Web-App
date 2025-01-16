from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import google.generativeai as genai
import json

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def chatbot_view(request):
    if request.method == "POST":
        try:
            # Log incoming data for debugging
            print("Request Body:", request.body)
            print("Headers:", request.headers)

            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_message = data.get("message", "")
            
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # Call the Gemini API
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_message)
            return JsonResponse({"response": response.text})

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            print("Unhandled Exception:", e)
            return JsonResponse({"error": str(e)}, status=500)