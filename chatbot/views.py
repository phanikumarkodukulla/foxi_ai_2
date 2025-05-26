import os
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import google.generativeai as genai

# Read API key from file
API_KEY_PATH = os.path.join(settings.BASE_DIR, 'api_key.txt')
try:
    with open(API_KEY_PATH, 'r') as f:
        API_KEY = f.read().strip()
    genai.configure(api_key=API_KEY)
except FileNotFoundError:
    print("API key file not found!")
    API_KEY = None

def home(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def ask_gemini(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            
            if not API_KEY:
                return JsonResponse({'error': 'API key not configured'}, status=500)
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            return JsonResponse({'response': response.text})
        except Exception as e:
            print(f"Error: {str(e)}")  # This will show in Django console
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)