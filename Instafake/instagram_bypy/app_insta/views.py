from django.shortcuts import render

# Create your views here.

def tela_login(request):
    return render(request, "login/index.html")
