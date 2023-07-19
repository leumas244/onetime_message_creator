from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', LoginView.as_view(template_name='sites/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('Passwort-aendern/', views.password_change, name="change_password"),
    path('Einstellungen/', views.settings, name='settings'),
    path('Verlauf', views.history, name="history"),
    path('neuer_Passwort-Link', views.new_password, name="new_password"),
    path('neuer_Nachrichten-Link', views.new_message, name="new_message"),
    path('Passwort_teilen/<str:token>/', views.share_password_by_token, name='share_password_by_token'),
]
