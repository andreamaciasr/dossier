from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

import requests, json
import environ 
env = environ.Env()
env.read_env()


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    response = requests.get(f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={env('NYT_KEY')}').json()
    articles = response['response']['docs']  
    return render(request, 'home.html', {'articles': articles})