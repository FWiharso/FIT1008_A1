from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        """
        O(1): Simply assigns the value
        """
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """
        """
        Every single function in this method has a best case and worst case complexity of O(1).
        All the calculations perform require a single step and involve simple arthimetic based on relevant variables.
        """
        # Determine the actions for each team
        action1 = self.out1.choose_action(self.out1, self.out2)
        action2 = self.out2.choose_action(self.out2, self.out1)

        # Process actions for both teams
        if action1 == Battle.Action.ATTACK:
            damage1 = self.out1.get_attack() - self.out2.get_defense()
            self.out2.reduce_hp(damage1)

        if action2 == Battle.Action.ATTACK:
            damage2 = self.out2.get_attack() - self.out1.get_defense()
            self.out1.reduce_hp(damage2)

        # Handle fainted monsters
        if self.out1.is_fainted():
            if self.team1.has_remaining_monsters():
                self.out1 = self.team1.retrieve_from_team()
            else:
                return Battle.Result.TEAM2

        if self.out2.is_fainted():
            if self.team2.has_remaining_monsters():
                self.out2 = self.team2.retrieve_from_team()
            else:
                return Battle.Result.TEAM1

        # Handle level ups and evolutions
        self.out1.check_for_level_up_or_evolution()
        self.out2.check_for_level_up_or_evolution()

        # Subtract 1 from HP if both monsters survive
        if not self.out1.is_fainted() and not self.out2.is_fainted():
            self.out1.reduce_hp(1)
            self.out2.reduce_hp(1)

        # Checks for the battle result
        if self.team1.is_defeated():
            return Battle.Result.TEAM2
        elif self.team2.is_defeated():
            return Battle.Result.TEAM1
        else:
            return None

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        """
        Best case: O(1) - When one team has no monsters, ending the battle immediately.
        Worst case: O(n) - Dependent on the number of turns (n) during the battle.
        """
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        
        # Check if either team has no available monsters
        if len(team1) == 0:
            print("Team 1 has no monsters. Add monsters to the team.")
            return Battle.Result.TEAM2
        elif len(team2) == 0:
            print("Team 2 has no monsters. Add monsters to the team.")
            return Battle.Result.TEAM1

        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
