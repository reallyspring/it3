import random
import time
import sys

# Функция для постепенного вывода текста (эффект печатной машинки)
def slow_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

# Функция для постепенного вывода текста в запросе ввода
def slow_input(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    return input()

# Базовый класс для всех персонажей
class Character:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_mp = 50
        self.mp = self.max_mp
        self.strength = 10
        self.agility = 10
        self.intelligence = 10

    # Проверка, жив ли персонаж
    def is_alive(self):
        if self.hp > 0:
            return True
        else:
            return False

    # Получение урона
    def take_damage(self, damage):
        if damage < 0:
            damage = 0
        self.hp = self.hp - damage
        if self.hp < 0:
            self.hp = 0
        return damage

    # Лечение персонажа
    def heal(self, amount):
        self.hp = self.hp + amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return amount

    # Обычная атака
    def basic_attack(self, target):
        damage = self.strength + random.randint(1, 5)
        # Наносим урон цели
        target.take_damage(damage)
        slow_print(self.name + " ударил " + target.name + " на " + str(damage) + " урона!")

    # Использование предмета (артефакта)
    def use_item(self, item_name):
        if item_name == "Амулет Жизни":
            self.heal(20)
            slow_print(self.name + " использовал Амулет Жизни и восстановил 20 HP!")
            return True
        return False

# Класс Воина - много здоровья и силы
class Warrior(Character):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.max_hp = 150
        self.hp = self.max_hp
        self.strength = 15

    # Особый прием воина
    def special_move(self, target):
        damage = self.strength * 2
        target.take_damage(damage)
        slow_print(self.name + " применил Сокрушительный удар на " + target.name + " и нанес " + str(damage) + " урона!")

# Класс Мага - меньше здоровья, но сильная магия
class Mage(Character):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.max_hp = 80
        self.hp = self.max_hp
        self.intelligence = 20

    # Особый прием мага
    def special_move(self, target):
        damage = self.intelligence * 2
        target.take_damage(damage)
        slow_print(self.name + " пустил Файербол в " + target.name + " на " + str(damage) + " урона!")

# Класс Монстра
class Monster(Character):
    def __init__(self, name, hp, strength):
        super().__init__(name)
        self.max_hp = hp
        self.hp = hp
        self.strength = strength

# Функция для проведения боя между игроком и врагом
def start_simple_battle(player, enemy, artifacts=None):
    if artifacts is None:
        artifacts = []
    slow_print("--- Начался бой! ---")
    
    # Цикл боя, пока оба живы
    while player.is_alive() and enemy.is_alive():
        slow_print(player.name + ": " + str(player.hp) + " HP | " + enemy.name + ": " + str(enemy.hp) + " HP")
        slow_print("1. Обычная атака")
        slow_print("2. Особый прием")
        
        # Если есть амулет, даем возможность лечиться
        if "Амулет Жизни" in artifacts:
            slow_print("3. Использовать Амулет Жизни")
        
        choice = slow_input("Ваш ход: ")
        
        # Ход игрока
        if choice == "1":
            player.basic_attack(enemy)
        elif choice == "2":
            player.special_move(enemy)
        elif choice == "3" and "Амулет Жизни" in artifacts:
            player.use_item("Амулет Жизни")
        else:
            slow_print("Вы промахнулись кнопкой и пропустили ход!")

        # Ответный ход врага
        if enemy.is_alive():
            enemy.basic_attack(player)
            
    # Проверка результата боя
    if player.is_alive():
        slow_print("Вы победили " + enemy.name + "!")
        return True
    else:
        slow_print("Вы проиграли...")
        return False
