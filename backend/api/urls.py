from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # API endpoints for Players
    path('api/players/', views.list_players, name='list_players'),
    path('api/player/', views.create_player, name='create_player'),
    path('api/player/<int:pk>/', views.update_player, name='update_player'),
    path('api/player/delete/<int:pk>/', views.delete_player, name='delete_player'),

    # API endpoints for Teams
    path('api/teams/', views.list_teams, name='list_teams'),
    path('api/team/', views.create_team, name='create_team'),
    path('api/team/<int:pk>/', views.update_team, name='update_team'),
    path('api/team/delete/<int:pk>/', views.delete_team, name='delete_team'),

    # API endpoints for Contracts
    path('api/contracts/', views.list_contracts, name='list_contracts'),
    path('api/contract/', views.create_contract, name='create_contract'),
    path('api/contract/<int:pk>/', views.update_contract, name='update_contract'),
    path('api/contract/delete/<int:pk>/', views.delete_contract, name='delete_contract'),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

