from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Article, Tag
from .forms import TagForm
from datetime import datetime
from django import forms
from django.forms import Select
from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from bs4 import BeautifulSoup

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
    the_guardian_begin_date = date
    begin_date = re.sub(r'-', '', date)
    
    date = request.GET.get('end_date', '')
    the_guardian_end_date = date
    end_date = re.sub(r'-', '', date)
    query = request.GET.get('query')
    
    base_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={env('NYT_KEY')}'
    the_guardian_base_url = f'https://content.guardianapis.com/search?q={query}&api-key={env('THE_GUARDIAN_KEY')}'
    democracy_now_url = 'https://www.democracynow.org/topics/{query}'

    if begin_date:
        base_url += f'&begin_date={begin_date}'
        the_guardian_base_url += f'&from-date={the_guardian_begin_date}'

    if end_date:
        base_url += f'&end_date={end_date}'
        the_guardian_base_url += f'&to-date={the_guardian_end_date}'

    response = requests.get(base_url).json()
    articles = response['response']['docs']  

    the_guardian_response = requests.get(the_guardian_base_url).json()
    the_guardian_articles = the_guardian_response['response']['results']


    democracy_now_articles = scrapper(query)
   
    print(democracy_now_articles)
    return render(request, 'queried_articles.html', {'articles': articles, 'the_guardian_articles': the_guardian_articles, 'query': query, 'democracy_now_articles': democracy_now_articles})

def scrapper(query):
  response = requests.get(f'https://www.democracynow.org/topics/{query}')
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", attrs={"data-ga-action": "Topic: Story Headline"})

    if articles: 
       article_list = []
       for article in articles:
         article_dict = {"title": article.text.strip(), "url": "https://www.democracynow.org/" + article["href"]}
         article_list.append(article_dict) 
       return article_list
    else: 
       return "No articles found."
  else:
    return "Failed to retrieve the page."

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
    return redirect('saved_articles')


def saved_articles(request):
  articles = Article.objects.all()
  tag_form = TagForm()
  return render(request, 'articles/saved_articles.html', {
    'articles': articles, 'tag_form': tag_form
})

# def add_tag(request, article_id):
#     tag_form = TagForm(request.POST)
#     article = Article.objects.get(id=article_id)
#     if tag_form.is_valid():
#         tag = tag_form.save()
#         article.tags.add(tag)
#     return redirect('saved_articles')

def add_tag(request, article_id):
    article = Article.objects.get(id=article_id)
    tag_name = request.POST.get('name')
    tag = Tag.objects.filter(name=tag_name).first()
    if not tag:
        tag = Tag.objects.create(name=tag_name)
    article.tags.add(tag)
    return redirect('saved_articles')


def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'articles/detail.html', {'article': article})

def show_tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    articles = tag.article_set.all()
    return render(request, 'tags/show_tag.html', {'articles': articles, 'tag': tag})


class TagUpdate(UpdateView):
  model = Tag
  fields = ['name']

# class TagDelete(DeleteView):
#     model = Tag
#     success_url = '/saved_articles'

def delete_tag(request, article_id, tag_id):
    article = Article.objects.get(id=article_id)
    tag = Tag.objects.get(id=tag_id)

    article.tags.remove(tag)

    if tag.article_set.count() == 0:
        tag.delete()    
    return redirect('saved_articles')

