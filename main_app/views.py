from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User, Article

import requests, re
import environ 
env = environ.Env()
env.read_env()


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def queried_articles(request):
    date = request.GET.get('begin_date', '')
    begin_date = re.sub(r'-', '', date)
    print(begin_date)
    
    date = request.GET.get('end_date', '')
    end_date = re.sub(r'-', '', date)
    print(end_date)
    query = request.GET.get('query')

    
    base_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={env('NYT_KEY')}'

    if begin_date:
        base_url += f'&begin_date={begin_date}'
        print(base_url)
    if end_date:
        base_url += f'&end_date={end_date}'

    response = requests.get(base_url).json()
    articles = response['response']['docs']  
    return render(request, 'queried_articles.html', {'articles': articles, 'query': query})

def home(request):
    return render(request, 'home.html')

# def save_article(request, article):

