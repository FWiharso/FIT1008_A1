from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        """
        Best case: O(n)
        Worst case: O(n) - Dependent of the size of monsters in the team created
        """
        self.team_mode = team_mode
        self.team = ArrayR[Optional[MonsterBase]](self.TEAM_LIMIT)
        self.team_size = 0
        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

    def add_to_team(self, monster: MonsterBase):
        """
        Best case: O(1) - When the monster is inserted without any shifting.
        Worst case: O(n) - When shifting is involved in insertion.
        """
        if self.team_size < self.TEAM_LIMIT:
            if self.team_mode == self.TeamMode.FRONT:
                self.team.insert_first(monster)
            elif self.team_mode == self.TeamMode.BACK:
                self.team.insert_last(monster)
            elif self.team_mode == self.TeamMode.OPTIMISE:
                stat_value = monster.get_stat(self.sort_key)
                index = self.team_size
                while index > 0 and self.team[index - 1].get_stat(self.sort_key) < stat_value:
                    self.team[index] = self.team[index - 1]
                    index -= 1
                self.team[index] = monster
            self.team_size += 1
        else:
            raise ValueError("Team is already full.")

    def retrieve_from_team(self) -> MonsterBase:
        """
        Best case: O(1)
        Worst case: O(1) - Since there is a set of instructions based on every possible scenario
        It directly accesses an element from the given array.
        """
        if self.team_size > 0:
            if self.team_mode == self.TeamMode.FRONT:
                monster = self.team.get_first()
            elif self.team_mode == self.TeamMode.BACK:
                monster = self.team.get_last()
            elif self.team_mode == self.TeamMode.OPTIMISE:
                monster = self.team[self.team_size - 1]
            self.team_size -= 1
            return monster
        else:
            raise ValueError("Team is empty.")

    def special(self) -> None:
        """
        Best case: O(n)
        Worst case: O(n) - Where n is dependent on the team's size
        O(n) is required due to the nature of operations performed and permuations involved.
        """
        if self.team_mode == self.TeamMode.FRONT:
            self.team.reverse_first_n(3)
        elif self.team_mode == self.TeamMode.BACK:
            middle = self.team_size // 2
            self.team.swap_first_half_with_second_half(middle)
            self.team.reverse_last_n(middle)
        elif self.team_mode == self.TeamMode.OPTIMISE:
            self.team.reverse()
        else:
            raise ValueError("Invalid team mode.")

    def regenerate_team(self) -> None:
        """
        Best case: O(1)
        Worst case: O(1) - Simply creates a new empty team
        """
        self.team = ArrayR[Optional[MonsterBase]](self.TEAM_LIMIT)
        self.team_size = 0

    def select_randomly(self):
        """
        Best case: O(n)
        Worst case: O(n)
        In this case, it is not possible for the best case complexity to be O(1).
        It is required for the algorithm to iterate through every element in the list.
        This is in order to count the amount of spawnable monsters, resulting in O(n) complexity.
        """
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Best case: O(n * k)
        Worst case: O(n * k)
        In this case, n is the team size, and k is the number of available monsters.
        It is not possible to reduce time complexity due to iterating over all the possible monsters.
        """
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """
        team_size = int(input("How many monsters are there? "))
        monsters = get_all_monsters()
        spawnable_monsters = [monster for monster in monsters if monster.can_be_spawned()]

        print("MONSTERS Are:")
        for index, monster in enumerate(spawnable_monsters, start=1):
            status = "✔️" if monster in spawnable_monsters else "❌"
            print(f"{index}: {monster.get_name()} [{status}]")

        for _ in range(team_size):
            valid_selection = False
            while not valid_selection:
                try:
                    monster_index = int(input("Which monster are you spawning? ")) - 1
                    if 0 <= monster_index < len(spawnable_monsters):
                        selected_monster = spawnable_monsters[monster_index]
                        self.add_to_team(selected_monster())
                        valid_selection = True
                    else:
                        print("Invalid selection. Please choose a valid monster.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Best case: O(n)
        Worst case: O(n) - Where n is the amount of monsters in the team
        """
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        if provided_monsters is None:
            raise ValueError("Provided monsters list is required.")
        
        for monster_class in provided_monsters:
            self.add_to_team(monster_class())

    def __len__(self) -> int:
        """
        O(1): Simplty returns the length of team size
        """
        return self.team_size

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        """
        O(1): Only requires a singular calculation, comparing the values of the current monster against the enemy.
        """
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
