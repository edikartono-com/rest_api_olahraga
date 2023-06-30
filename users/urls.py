from django.urls import include, path

from . import views

urlpatterns = [
    path('user/', include([
        path('login/', views.LoginApiView.as_view(), name='login'),
        path('register/', views.RegisterApiView.as_view(), name='register')
    ])),
    path('add/', views.Add, name='add'),
    path('delete/<int:id>/',views.Delete, name='delete'),
    path('list/',views.List, name='list'),
    path('update/<int:id>/',views.Update, name='update'),
    path('', views.index),
]