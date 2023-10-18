from django.shortcuts import render
from django.http import JsonResponse
import openai


openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer
# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({ 'message': message, 'response': response})

    return render(request, 'chatbot.html')

def login(request):
    return render(request, 'login.html')