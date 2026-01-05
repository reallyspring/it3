from modules.game_logic import Warrior, Mage, Monster, start_simple_battle, slow_print, slow_input
from modules.storage import save_game, load_game, get_random_artifact, return_artifacts_to_pool
import sys
import random

def main():
    slow_print("=== Добро пожаловать в RPG Мини-игру! ===\n")
    
    # Сначала просим пользователя войти
    username = slow_input("Введите ваш логин: ")
    player_data = load_game(username)
    
    # Если пользователь найден, пытаемся загрузить данные
    if player_data:
        slow_print("Найден файл сохранения для: " + player_data["username"])
        ans = slow_input("Загрузить игру? (д/н): ")
        if ans.lower() == 'д':
            password = slow_input("Введите пароль: ")
            if password == player_data["password"]:
                # Если пароль верный, берем данные из сохранения
                password = player_data["password"]
                level = player_data["level"]
                class_name = player_data["class_name"]
                player_artifacts = player_data["artifacts"]
                slow_print("Загрузка успешна!")
            else:
                slow_print("Неверный пароль! Начинаем заново с новым персонажем.\n")
                player_data = None
        else:
            player_data = None

    # Если сохранения нет или пароль не подошел, создаем нового героя
    if not player_data:
        slow_print("Создание нового персонажа для " + username + '\n')
        password = slow_input("Придумайте пароль: ")
        slow_print("\nВыберите класс:")
        slow_print("1. Воин")
        slow_print("2. Маг")
        c_choice = slow_input("\nВаш выбор: ")
        if c_choice == "1":
            class_name = "Warrior"
        else:
            class_name = "Mage"
        level = 1
        player_artifacts = []

    # Создаем объект игрока нужного класса
    if class_name == "Warrior":
        player = Warrior(username, level)
    else:
        player = Mage(username, level)

    # Применяем бонусы от уже имеющихся артефактов
    for art in player_artifacts:
        if art == "Меч Грифона": player.strength += 5
        if art == "Щит Черепахи": player.max_hp += 20; player.hp += 20
        if art == "Амулет Жизни": player.max_hp += 30; player.hp += 30

    # Список для хранения уже пройденных веток
    visited_locations = []
    
    # Главный цикл выбора приключений (максимум 3 ветки)
    while len(visited_locations) < 3:
        slow_print("\n--- Выбор пути ---\n")
        if "лес" not in visited_locations:
            slow_print("1. Пойти в Темный Лес (Линия Боя)")
        if "замок" not in visited_locations:
            slow_print("2. Пойти в Заброшенный Замок (Линия Тайн)")
        if "деревня" not in visited_locations:
            slow_print("3. Пойти в Деревню (Линия Мира)")
        slow_print("0. Закончить приключение и подвести итоги")
        
        choice1 = slow_input("\nВаш выбор: ")

        # Если игрок хочет выйти раньше
        if choice1 == "0":
            break

        # Переменные для отслеживания прогресса внутри ветки
        story_done = False
        won_artifact = None
        outcome = "" # Для текста концовки

        # Ветка 1: Темный Лес
        if choice1 == "1" and "лес" not in visited_locations:
            visited_locations.append("лес")
            slow_print("Вы вошли в Темный Лес. Здесь пахнет сыростью и опасностью.")
            slow_print("На тропинке вы видите раненого разбойника.\n")
            slow_print("1. Помочь ему")
            slow_print("2. Добить и забрать вещи")
            slow_print("3. Пройти мимо")
            choice_forest_1 = slow_input("\nВаш выбор: ")

            if choice_forest_1 == "1":
                slow_print("\nВы перевязали раны разбойнику. В благодарность он дает вам карту сокровищ.")
                slow_print("Вы идете по карте и находите пещеру.")
                slow_print("В пещере спит Медведь-оборотень!\n")
                bear = Monster("Медведь-оборотень", 60, 10)
                if start_simple_battle(player, bear, player_artifacts):
                    slow_print("\nВы победили медведя!")
                    slow_print("\nМедведь лежит перед вами и тяжело дышит. Похоже, он был заколдован.")
                    slow_print("1. Добить зверя")
                    slow_print("2. Оставить в покое и забрать сокровища")
                    if "Амулет Жизни" in player_artifacts:
                        slow_print("3. Использовать Амулет Жизни, чтобы исцелить его")
                    
                    choice_bear = slow_input("\nВаш выбор: ")
                    if choice_bear == "3" and "Амулет Жизни" in player_artifacts:
                        slow_print("Магия амулета снимает проклятие! Медведь превращается в принца.")
                        slow_print("Принц благодарит вас и ведет в тайный город эльфов.")
                        outcome = "forest_prince"
                        won_artifact = get_random_artifact()
                        player_artifacts.append(won_artifact)
                    elif choice_bear == "1":
                        slow_print("Вы закончили мучения зверя и нашли в его берлоге золото.")
                        outcome = "standard_win"
                    else:
                        slow_print("Вы забираете сундук и уходите. Медведь со временем уходит в глубь леса.")
                        won_artifact = get_random_artifact()
                        slow_print("Вы нашли: " + won_artifact)
                        player_artifacts.append(won_artifact)
                        outcome = "hero_of_forest"
                    story_done = True
                else:
                    slow_print("Медведь оказался сильнее...")

            elif choice_forest_1 == "2":
                slow_print("\nВы забрали золото у разбойника, но его банда выскочила из кустов!\n")
                bandit = Monster("Главарь бандитов", 55, 12)
                if start_simple_battle(player, bandit, player_artifacts):
                    slow_print("\nВы перебили бандитов. Теперь вы новый лидер банды или просто богач?")
                    slow_print("1. Стать их главарем")
                    slow_print("2. Просто забрать золото и уйти")
                    choice_forest_2 = slow_input("\nВаш выбор: ")
                    if choice_forest_2 == "1":
                        outcome = "bandit_king"
                    else:
                        outcome = "rich_wanderer"
                    story_done = True
                else:
                    slow_print("\nБандиты отомстили за своего товарища...")

            else:
                slow_print("\nВы пошли дальше и наткнулись на Орка!")
                orc = Monster("Орк", 50, 8)
                if start_simple_battle(player, orc, player_artifacts):
                    slow_print("\nПосле победы вы нашли странный сундук.")
                    won_artifact = get_random_artifact()
                    slow_print("\nВы нашли артефакт: " + won_artifact)
                    player_artifacts.append(won_artifact)
                    outcome = "standard_win"
                    story_done = True
                else:
                    slow_print("\nОрк победил вас.")

        # Ветка 2: Заброшенный Замок
        elif choice1 == "2" and "замок" not in visited_locations:
            visited_locations.append("замок")
            slow_print("Вы входите в Заброшенный Замок. Стены покрыты пылью.")
            slow_print("Вы видите две двери: Золотую и Серебряную.")
            slow_print("1. Золотая дверь")
            slow_print("2. Серебряная дверь")
            choice_castle_1 = slow_input("\nВаш выбор: ")
            if choice_castle_1 == "1":
                slow_print("\nЗа золотой дверью огромный зал с короной на троне.")
                slow_print("1. Надеть корону")
                slow_print("2. Искать выход")
                choice_castle_2 = slow_input("\nВаш выбор: ")
                if choice_castle_2 == "1":
                    slow_print("Корона проклята! Появляется Призрак Короля!")
                    ghost = Monster("Призрак Короля", 100, 15)
                    if start_simple_battle(player, ghost, player_artifacts):
                        slow_print("Вы победили призрака и сняли проклятие!")
                        slow_print("Призрак указывает на стену, за которой скрыт механизм.")
                        slow_print("1. Просто забрать корону")
                        if "Меч Грифона" in player_artifacts:
                            slow_print("2. Вставить Меч Грифона в прорезь в стене")
                        
                        choice_ghost = slow_input("Ваш выбор: ")
                        if choice_ghost == "2" and "Меч Грифона" in player_artifacts:
                            slow_print("Стена отъезжает, открывая сокровищницу древних богов!")
                            outcome = "god_king"
                            won_artifact = get_random_artifact()
                            player_artifacts.append(won_artifact)
                        else:
                            slow_print("Вы стали королем этого замка.")
                            outcome = "true_king"
                        story_done = True
                    else:
                        slow_print("Ваша душа теперь принадлежит замку...")
                else:
                    slow_print("Вы пытались выйти, но наткнулись на Дракона!")
                    dragon = Monster("Маленький Дракон", 80, 12)
                    if start_simple_battle(player, dragon, player_artifacts):
                        outcome = "dragon_slayer"
                        won_artifact = get_random_artifact()
                        player_artifacts.append(won_artifact)
                        story_done = True
                    else:
                        slow_print("Дракон поджарил вас.")

            else:
                slow_print("За серебряной дверью вы нашли библиотеку.")
                slow_print("Там сидит старый Маг и читает книгу.")
                slow_print("1. Попросить обучить магии")
                slow_print("2. Ограбить мага")
                choice_castle_3 = slow_input("Ваш выбор: ")
                if choice_castle_3 == "1":
                    slow_print("Маг увидел в вас потенциал.")
                    player.level += 2
                    outcome = "sage_apprentice"
                    story_done = True
                else:
                    slow_print("Маг оказался разгневан!")
                    battle_mag = Monster("Разгневанный Маг", 70, 20)
                    if start_simple_battle(player, battle_mag, player_artifacts):
                        slow_print("Вы одолели мага и забрали его посох (артефакт).")
                        won_artifact = get_random_artifact()
                        player_artifacts.append(won_artifact)
                        outcome = "dark_mage"
                        story_done = True
                    else:
                        slow_print("Маг превратил вас в лягушку.")

        # Ветка 3: Деревня
        elif choice1 == "3" and "деревня" not in visited_locations:
            visited_locations.append("деревня")
            slow_print("Вы пришли в тихую Деревню. Все напуганы.")
            slow_print("Староста говорит, что в колодце живет монстр.")
            slow_print("1. Спуститься в колодец")
            slow_print("2. Сжечь деревню (стать злым)")
            slow_print("3. Просто отдохнуть в таверне")
            choice_village_1 = slow_input("Ваш выбор: ")

            if choice_village_1 == "1":
                slow_print("В колодце сыро. На вас нападает Слизень!")
                slime = Monster("Болотный Слизень", 40, 5)
                if start_simple_battle(player, slime, player_artifacts):
                    slow_print("Вы победили слизня!")
                    slow_print("На дне колодца вы видите странный светящийся камень.")
                    slow_print("1. Забрать камень")
                    if "Щит Черепахи" in player_artifacts:
                        slow_print("2. Использовать Щит Черепахи, чтобы закрыть источник заразы")
                    
                    choice_slime = slow_input("Ваш выбор: ")
                    if choice_slime == "2" and "Щит Черепахи" in player_artifacts:
                        slow_print("Вы запечатали колодец щитом. Вода стала целебной.")
                        outcome = "village_saint"
                    else:
                        slow_print("Вы нашли на дне древний артефакт!")
                        won_artifact = get_random_artifact()
                        player_artifacts.append(won_artifact)
                        outcome = "village_hero"
                    story_done = True
                else:
                    slow_print("Вы утонули в слизи.")

            elif choice_village_1 == "2":
                slow_print("Вы решили, что деревня вам не нравится. Но жители взялись за вилы!")
                mobs = Monster("Разгневанные крестьяне", 90, 7)
                if start_simple_battle(player, mobs, player_artifacts):
                    slow_print("Вы сожгли всё и ушли в закат с награбленным.")
                    outcome = "villain"
                    story_done = True
                else:
                    slow_print("Крестьяне оказались сильнее, чем вы думали.")

            else:
                slow_print("В таверне вы услышали сплетни.")
                slow_print("Трактирщик предлагает игру в кости на артефакт.")
                slow_print("1. Играть")
                slow_print("2. Просто спать")
                choice_village_2 = slow_input("Ваш выбор: ")
                if choice_village_2 == "1":
                    # Шанс 50 на 50
                    if random.randint(1, 2) == 1:
                        slow_print("Вы выиграли!")
                        won_artifact = get_random_artifact()
                        player_artifacts.append(won_artifact)
                        outcome = "lucky_gambler"
                    else:
                        slow_print("Вы проиграли всё золото и ушли ни с чем.")
                        outcome = "loser"
                    story_done = True
                else:
                    slow_print("Вы выспались. HP полностью восстановлено.")
                    player.hp = player.max_hp
                    outcome = "peaceful_traveler"
                    story_done = True
        else:
            slow_print("Неверный выбор или вы там уже были!")

        # Показываем промежуточный итог после прохождения ветки
        if story_done:
            slow_print("\n--- ИТОГИ ТЕКУЩЕГО ЭТАПА ---")
            if outcome == "hero_of_forest":
                slow_print("Вы защитили лес!")
            elif outcome == "forest_prince":
                slow_print("Вы спасли принца!")
            elif outcome == "bandit_king":
                slow_print("Вы стали главарем банды!")
            elif outcome == "god_king":
                slow_print("Вы нашли божественные сокровища!")
            elif outcome == "village_saint":
                slow_print("Вы спасли деревню!")
            else:
                slow_print("Вы успешно завершили эту часть пути.")
            slow_print("Теперь вы можете выбрать другой путь или закончить игру.")

    # Финальные итоги всего прохождения
    slow_print("\n--- ФИНАЛЬНЫЕ ИТОГИ ВАШЕГО ПУТЕШЕСТВИЯ ---")
    slow_print("Вы посетили локаций: " + str(len(visited_locations)))
    slow_print("У вас в руках артефакты: " + (", ".join(player_artifacts) if player_artifacts else "У вас нет артефактов."))
    
    # Предлагаем сохраниться
    slow_print("\nХотите сохранить прогресс? (Если нет, артефакты вернутся в копилку)")
    s_choice = slow_input("Сохранить? (д/н): ")
    if s_choice.lower() == 'д':
        save_game(username, password, player.level, class_name, player_artifacts)
    else:
        # Если не сохраняемся, артефакты улетают обратно в общий пул
        slow_print("Прогресс не сохранен.")
        return_artifacts_to_pool(player_artifacts)

    slow_print("До встречи!")

if __name__ == "__main__":
    main()
