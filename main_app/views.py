from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Article, Tag
from .forms import TagForm
from .functions import format_date, scrapper
from datetime import datetime
from django import forms
from django.forms import Select
from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import requests, re
import environ

env = environ.Env()
env.read_env()


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def queried_articles(request):
    date = request.GET.get("begin_date", "")
    the_guardian_begin_date = date
    nyt_begin_date = re.sub(r"-", "", date)

    date = request.GET.get("end_date", "")
    the_guardian_end_date = date
    nyt_end_date = re.sub(r"-", "", date)
    query = request.GET.get("query")

    nyt_base_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={env('NYT_KEY')}"
    the_guardian_base_url = f"https://content.guardianapis.com/search?q={query}&api-key={env('THE_GUARDIAN_KEY')}"

    if nyt_begin_date:
        nyt_base_url += f"&begin_date={nyt_begin_date}"
        the_guardian_base_url += f"&from-date={the_guardian_begin_date}"

    if nyt_end_date:
        nyt_base_url += f"&end_date={nyt_end_date}"
        the_guardian_base_url += f"&to-date={the_guardian_end_date}"

    nyt_response = requests.get(nyt_base_url).json()
    nyt_articles = nyt_response["response"]["docs"]

    the_guardian_response = requests.get(the_guardian_base_url).json()
    articles = the_guardian_response["response"]["results"]
    the_guardian_articles = sorted(
        articles, key=lambda x: x["webPublicationDate"], reverse=True
    )

    democracy_now_articles = scrapper(query)

    return render(
        request,
        "queried_articles.html",
        {
            "nyt_articles": nyt_articles,
            "the_guardian_articles": the_guardian_articles,
            "democracy_now_articles": democracy_now_articles,
            "query": query,
        },
    )


def home(request):
    return render(request, "home.html")


@login_required
def save_article(request):
    web_url = request.POST.get("web_url")
    headline = request.POST.get("headline")
    date_str = request.POST.get("pub_date")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return

    date = date.strftime("%Y-%m-%d")
    user = request.user
    article = Article(headline=headline, link=web_url, user=user, date=date)
    article.save()
    return redirect("saved_articles")


@login_required
def saved_articles(request):
    articles = Article.objects.filter(user=request.user)
    tag_form = TagForm()
    return render(
        request,
        "articles/saved_articles.html",
        {"articles": articles, "tag_form": tag_form},
    )


def add_tag(request, article_id):
    article = Article.objects.get(id=article_id)
    tag_name = request.POST.get("name")
    tag = Tag.objects.filter(name=tag_name).first()
    if not tag:
        tag = Tag.objects.create(name=tag_name)
    article.tags.add(tag)
    return redirect("saved_articles")


def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, "articles/detail.html", {"article": article})


@login_required
def show_tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    articles = tag.article_set.all()
    return render(request, "tags/show_tag.html", {"articles": articles, "tag": tag})


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ["name"]


@login_required
def delete_tag(request, article_id, tag_id):
    article = Article.objects.get(id=article_id)
    tag = Tag.objects.get(id=tag_id)

    article.tags.remove(tag)

    if tag.article_set.count() == 0:
        tag.delete()
    return redirect("saved_articles")


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)
