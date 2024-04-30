from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User, Article
from datetime import datetime
from django import forms
from django.forms import Select
from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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
    
    date = request.GET.get('end_date', '')
    end_date = re.sub(r'-', '', date)
    query = request.GET.get('query')

    
    base_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={env('NYT_KEY')}'

    if begin_date:
        base_url += f'&begin_date={begin_date}'
    if end_date:
        base_url += f'&end_date={end_date}'

    response = requests.get(base_url).json()
    articles = response['response']['docs']  
    return render(request, 'queried_articles.html', {'articles': articles, 'query': query})

def home(request):
    return render(request, 'home.html')

def save_article(request):
    web_url = request.POST.get('web_url')
    headline = request.POST.get('headline')
    date = request.POST.get('pub_date')
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    date = date.strftime("%Y-%m-%d")
    user = request.user
    article = Article(headline=headline, link=web_url, user=user, date=date)
    article.save()
    return render(request, 'articles/detail.html', {'article': article})




