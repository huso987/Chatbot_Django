from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, 'user')
                return redirect('chatbot')
            except:
                error_message = "Hesap oluşturuldu"
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Şifreler ayni değil'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')