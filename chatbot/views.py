from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import google.generativeai as genai
import json
import pandas as pd
import PyPDF2
from django.core.files.storage import FileSystemStorage



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

def query_data(user_message):
    # Example: Search stored data for relevant information
    # You can use a more sophisticated NLP approach for better matching
    data = retrieve_data()
    for item in data:
        if user_message.lower() in item["content"].lower():
            return item["content"]
    return None

def retrieve_data():
    # Example: Fetch from database or cache
    return []

def upload_file_view(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # Parse file based on type
        if filename.endswith(".pdf"):
            data = parse_pdf(file_path)
        elif filename.endswith(".csv"):
            data = parse_csv(file_path)
        elif filename.endswith(".xlsx"):
            data = parse_excel(file_path)
        else:
            return JsonResponse({"error": "Unsupported file type"}, status=400)

        # Store data in database or cache
        store_data(data)

        return JsonResponse({"message": "File uploaded and processed successfully"})

    return render(request, "upload_file.html")

def parse_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return {"type": "pdf", "content": text}

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    return {"type": "csv", "content": df.to_dict()}

def parse_excel(file_path):
    df = pd.read_excel(file_path)
    return {"type": "excel", "content": df.to_dict()}

def store_data(data):
    # Example: Store in cache or database
    pass