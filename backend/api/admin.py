from django.contrib import admin
from .models import Team, Player, Contract

class ContractInline(admin.TabularInline):
    """
    Inline admin for Contract model, allowing contracts to be added in Player and Team views.

    Attributes:
    - model (Contract): Specifies the model to be used for inline.
    - extra (int): Number of empty inline forms to display by default.
    - fields (tuple): Fields to display in the inline form.
    """
    model = Contract
    extra = 1
    fields = ('team', 'contract_start_date', 'contract_end_date', 'salary', 'active')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin view for managing Team model instances.

    Attributes:
    - list_display (tuple): Fields to display in the team list view.
    - search_fields (tuple): Fields to search for teams.
    - inlines (list): Inlines to include in the Team admin view.
    """
    list_display = ('name', 'city', 'founded')
    search_fields = ('name', 'city')
    inlines = [ContractInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Admin view for managing Player model instances.

    Attributes:
    - list_display (tuple): Fields to display in the player list view.
    - search_fields (tuple): Fields to search for players.
    - inlines (list): Inlines to include in the Player admin view.
    """
    list_display = ('name', 'position', 'nationality')
    search_fields = ('name', 'position', 'nationality')
    inlines = [ContractInline]
