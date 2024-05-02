from django.urls import path
from . import views

urlpatterns = [
    path("queried_articles", views.queried_articles, name="queried_articles"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("save_article", views.save_article, name="save_article"),
    path("articles/article/<int:article_id>/", views.article_detail, name="detail"),
    path("saved_articles", views.saved_articles, name="saved_articles"),
    path("articles/<int:article_id>/add_tag/", views.add_tag, name="add_tag"),
    path("articles/<int:tag_id>/", views.show_tag, name="show_tag"),
    path("tags/<int:pk>/update/", views.TagUpdate.as_view(), name="tags_update"),
    path(
        "tags/<int:article_id>/<int:tag_id>/delete/",
        views.delete_tag,
        name="delete_tag",
    ),
    path('accounts/signup/', views.signup, name='signup'),
]
