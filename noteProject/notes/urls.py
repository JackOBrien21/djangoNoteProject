from django.urls import path

from . import views


app_name = 'notes'
urlpatterns = [
    path('', views.index, name="index"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('addnote', views.addnote, name="addnote"),
    path('detail/<int:id>/', views.detail, name="detail"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('update/<int:id>/', views.update, name="update")
]