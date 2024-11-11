from django.db import models

class Team(models.Model):
    """
    Represents a team in the system.

    Attributes:
    - name (CharField): The team's name.
    - city (CharField): The city where the team is based.
    - founded (IntegerField): The year the team was founded.
    - description (TextField): A description of the team.
    """
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    founded = models.IntegerField()
    description = models.TextField()

    def __str__(self):

        """Returns a string representation of the Team. """
        
        return self.name


class Player(models.Model):
    """
    Represents a player in the system.

    Attributes:
    - name (CharField): The player's name.
    - position (CharField): The player's position on the team.
    - nationality (CharField): The player's nationality.
    - teams (ManyToManyField): A many-to-many relationship with the Team model, through the Contract model.
    """
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, through='Contract')

    def __str__(self):
        """
        Returns a string representation of the Player.

        """
        return self.name


class Contract(models.Model):
    """
    Represents a contract between a player and a team.

    Attributes:
    - player (ForeignKey): The player involved in the contract.
    - team (ForeignKey): The team involved in the contract.
    - contract_start_date (DateField): The start date of the contract.
    - contract_end_date (DateField): The end date of the contract.
    - salary (IntegerField): The salary amount of the player during the contract.
    - active (BooleanField): Indicates if the contract is currently active.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    salary = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):

        """
        
        Returns a string representation of the Contract.
        
        """
        
        return f"{self.player.name} - {self.team.name} (Contract)"
