import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Player, Team, Contract
from django.views.generic import TemplateView

class IndexView(TemplateView):
    """
    Renders the main index page where the Vue.js frontend is mounted.
    """
    template_name = "index.html"


@csrf_exempt
def list_players(request):
    """
    Handles GET requests to list all players.

    Returns:
    - JsonResponse: A JSON response with a list of players.
    """
    if request.method == 'GET':
        players = list(Player.objects.values())
        return JsonResponse({'players': players})


@csrf_exempt
def create_player(request):
    """
    Handles POST requests to create a new player.

    Returns:
    - JsonResponse: A JSON response with the created player's information.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        player = Player.objects.create(
            name=data['name'],
            position=data['position'],
            nationality=data['nationality']
        )
        return JsonResponse({'message': 'Player created successfully', 'player': {'id': player.id, 'name': player.name}})


@csrf_exempt
def update_player(request, pk):
    """
    Handles PUT requests to update a specific player's details.

    Parameters:
    - pk (int): The primary key of the player to update.

    Returns:
    - JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == 'PUT':
        try:
            player = Player.objects.get(pk=pk)
            data = json.loads(request.body)
            player.name = data.get('name', player.name)
            player.position = data.get('position', player.position)
            player.nationality = data.get('nationality', player.nationality)
            player.save()
            return JsonResponse({'message': 'Player updated successfully'})
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Player not found'}, status=404)


@csrf_exempt
def delete_player(request, pk):
    """
    Handles DELETE requests to remove a player from the system.

    Parameters:
    - pk (int): The primary key of the player to delete.

    Returns:
    - JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == 'DELETE':
        try:
            player = Player.objects.get(pk=pk)
            player.delete()
            return JsonResponse({'message': 'Player deleted successfully'})
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Player not found'}, status=404)

# Team Views

@csrf_exempt
def list_teams(request):
    """
    Handles GET requests to list all teams.

    Returns:
    - JsonResponse: A JSON response with a list of teams.
    """
    if request.method == 'GET':
        teams = list(Team.objects.values())
        return JsonResponse({'teams': teams})


@csrf_exempt
def create_team(request):
    """
    Handles POST requests to create a new team.

    Returns:
    - JsonResponse: A JSON response with the created team's information.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        team = Team.objects.create(
            name=data['name'],
            city=data['city'],
            founded=data['founded'],
            description=data.get('description', '')
        )
        return JsonResponse({'message': 'Team created successfully', 'team': {'id': team.id, 'name': team.name}})


@csrf_exempt
def update_team(request, pk):
    """
    Handles PUT requests to update a specific team's details.

    Parameters:
    - pk (int): The primary key of the team to update.

    Returns:
    - JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == 'PUT':
        try:
            team = Team.objects.get(pk=pk)
            data = json.loads(request.body)
            team.name = data.get('name', team.name)
            team.city = data.get('city', team.city)
            team.founded = data.get('founded', team.founded)
            team.description = data.get('description', team.description)
            team.save()
            return JsonResponse({'message': 'Team updated successfully'})
        except Team.DoesNotExist:
            return JsonResponse({'error': 'Team not found'}, status=404)


@csrf_exempt
def delete_team(request, pk):
    """
    Handles DELETE requests to remove a team from the system.

    Parameters:
    - pk (int): The primary key of the team to delete.

    Returns:
    - JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == 'DELETE':
        try:
            team = Team.objects.get(pk=pk)
            team.delete()
            return JsonResponse({'message': 'Team deleted successfully'})
        except Team.DoesNotExist:
            return JsonResponse({'error': 'Team not found'}, status=404)

# Contract Views

@csrf_exempt
def list_contracts(request):
    """
    Handles GET requests to list all contracts with player and team names.

    Returns:
    - JsonResponse: A JSON response with a list of contracts.
    """
    if request.method == 'GET':
        contracts = Contract.objects.values(
            'id', 
            'contract_start_date', 
            'contract_end_date', 
            'salary', 
            'active',
            'player__name',
            'team__name'
        )
        contracts_data = [
            {
                "id": contract["id"],
                "contract_start_date": contract["contract_start_date"],
                "contract_end_date": contract["contract_end_date"],
                "salary": contract["salary"],
                "active": contract["active"],
                "player_name": contract["player__name"],
                "team_name": contract["team__name"]
            }
            for contract in contracts
        ]
        return JsonResponse({'contracts': contracts_data})


@csrf_exempt
def create_contract(request):
    """
    Handles POST requests to create a new contract.

    Returns:
    - JsonResponse: A JSON response with the created contract's information.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            player = Player.objects.get(id=data['player_id'])
            team = Team.objects.get(id=data['team_id'])
            contract = Contract.objects.create(
                player=player,
                team=team,
                contract_start_date=data['contract_start_date'],
                contract_end_date=data['contract_end_date'],
                salary=data['salary'],
                active=data.get('active', True)
            )
            return JsonResponse({'message': 'Contract created successfully', 'contract': {'id': contract.id}})
        except (Player.DoesNotExist, Team.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)
