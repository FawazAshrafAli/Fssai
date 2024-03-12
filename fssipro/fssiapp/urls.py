from django.urls import path
from . import views

urlpatterns = [
    path("",views.register, name="register"),
    path("admin/", views.user_login, name="login"),    
    path("home/", views.home, name="home"),    
    path('delete/<pk>', views.delete, name="delete"),
    path("logout/", views.user_logout, name="logout"),
    path('reset_password/', views.reset_password, name="reset_password"),

    path('opened/<pk>/', views.opened, name='opened'),
    path('unread/<pk>/', views.unread, name='unread'),
]
