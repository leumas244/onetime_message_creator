from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', LoginView.as_view(template_name='sites/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('Passwort_aendern/', views.password_change, name="change_password"),
    path('Einstellungen/', views.settings, name='settings'),
    path('neuer_Passwort-Link/', views.new_password, name="new_password"),
    path('neuer_Nachrichten-Link/', views.new_message, name="new_message"),
    path('Teilen/<str:token>/', views.share_by_token, name='share_by_token'),
    path('Link/<str:link_type>/<int:identifier>/', views.show_link_by_id, name='show_link_by_id'),
    path('Bearbeiten/<str:link_type>/<int:identifier>/', views.edit_by_id, name='edit_by_id'),
    path('base/', views.base, name="base"),
]
