from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [

 
    path("", views.ArtistsHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("login", views.LoginUser.as_view(), name="login"),
    path("register", views.RegisterUser.as_view(), name="register"),
    path("logout", views.logout_user, name="logout"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", views.ArtistsCategory.as_view(), name="category"),


]
