import abc
import math

from data_structures.referential_array import ArrayR

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass

class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp # Sets required attributes

    def get_attack(self):
        return self.attack 

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp # Returns defined attributes

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        """
        This method has a complexity of O(N), where N relates to the size of each respective array.
        """
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula
        pass

    def evaluate_expression(self, expression, level):
        """
        This method has a best case and worst case time complexity of both O(N).
        This is due to the fact of each token being processed exactly once no matter the order
        """
        stack = []
        operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            'power': lambda a, b: math.pow(a, b),
            'sqrt': lambda a: math.sqrt(a),
        } #Defines operators

        for token in expression:
            if token in operators:
                if token == 'sqrt':
                    a = stack.pop() # Utilizes the stack method
                    stack.append(operators[token](a))
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(int(operators[token](a, b)))
            elif token == 'level':
                stack.append(level)
            elif token == 'middle':
                c = stack.pop()
                b = stack.pop()
                a = stack.pop()
                stack.append(sorted([a, b, c])[1]) # Appends to stored array
            else:
                stack.append(float(token))

        return int(stack[0])

    def get_attack(self, level: int):
        return self.evaluate_expression(self.attack_formula, level) # Utilizes formulas derived from evaluate_expression function

    def get_defense(self, level: int):
        return self.evaluate_expression(self.defense_formula, level)

    def get_speed(self, level: int):
        return self.evaluate_expression(self.speed_formula, level)

    def get_max_hp(self, level: int):
        return self.evaluate_expression(self.max_hp_formula, level)
