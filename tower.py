from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        """
        O(1) - Time complexity is constant, only involves creating battle instance.
        """
        self.battle = battle or Battle(verbosity=0)
        self.player_team = None
        self.tower_teams = []

    def set_my_team(self, team: MonsterTeam) -> None:
        """
        O(1) - Involves assigning a value based on the generated number of lives
        It will always be O(1) regardless of the value.
        """
        self.player_team = team
        self.player_team.lives = RandomGen.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES + 1)

    def generate_teams(self, n: int) -> None:
        """
        O(n), since it is dependent on the number of different teams generated.
        """
        for _ in range(n):
            team = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
            team.lives = RandomGen.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES + 1)
            self.tower_teams.append(team)

    def battles_remaining(self) -> bool:
        """
        O(n), since it considers the teams assigned from the generate_teams method, analyzing the amount of lives.
        """
        return self.player_team.lives > 0 and any(team.lives > 0 for team in self.tower_teams)

    def __iter__(self):
        """
        O(1)
        """
        return self

    def __next__(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        """
        O(1), since it simply creates commands to execute the battle and modifies the values in the amount of lives remaining.
        """
        if not self.battles_remaining():
            raise StopIteration

        tower_team = self.tower_teams.pop(0)
        result = self.battle.battle(self.player_team, tower_team)
        player_lives = self.player_team.lives
        tower_lives = tower_team.lives

        if result == Battle.Result.TEAM1:
            tower_team.lives -= 1
        elif result == Battle.Result.TEAM2:
            self.player_team.lives -= 1
        else:  # Draw
            self.player_team.lives -= 1
            tower_team.lives -= 1

        return result, self.player_team, tower_team, player_lives, tower_lives

    def out_of_meta(self) -> ArrayR[Element]:
        """"""
        elements_present = set()
        for team in self.tower_teams:
            elements_present.update(monster.element for monster in team.monsters)
        return ArrayR([element for element in Element if element not in elements_present])

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)
