import os
import random

# Файлы для хранения данных
USERS_FILE = "users.txt"
ARTIFACTS_FILE = "artifacts.txt"

# Полный список всех возможных артефактов в игре
ALL_POSSIBLE_ARTIFACTS = ["Меч Грифона", "Щит Черепахи", "Кольцо Силы", "Плащ Тени", "Амулет Жизни"]

# Сохранение игры пользователя
def save_game(username, password, level, class_name, artifacts):
    # Сначала загружаем всех существующих пользователей
    users = []
    if os.path.exists(USERS_FILE):
        f = open(USERS_FILE, "r", encoding="utf-8")
        users = f.readlines()
        f.close()
    
    # Ищем текущего пользователя, чтобы обновить его данные
    new_users = []
    found = False
    for u in users:
        data = u.strip().split("|")
        if data[0] == username:
            # Формируем новую строку с данными пользователя
            new_line = username + "|" + password + "|" + str(level) + "|" + class_name + "|" + ",".join(artifacts) + "\n"
            new_users.append(new_line)
            found = True
        else:
            new_users.append(u)
    
    # Если пользователя не было в списке, добавляем его
    if not found:
        new_line = username + "|" + password + "|" + str(level) + "|" + class_name + "|" + ",".join(artifacts) + "\n"
        new_users.append(new_line)
    
    # Записываем обновленный список всех пользователей обратно в файл
    f = open(USERS_FILE, "w", encoding="utf-8")
    for u in new_users:
        f.write(u)
    f.close()
    print("Игра сохранена для пользователя " + username + "!")

# Загрузка данных пользователя по его логину
def load_game(username):
    if not os.path.exists(USERS_FILE):
        return None
    
    f = open(USERS_FILE, "r", encoding="utf-8")
    users = f.readlines()
    f.close()
    
    # Ищем строку с нужным логином
    for u in users:
        data = u.strip().split("|")
        if data[0] == username:
            # Возвращаем словарь с данными
            return {
                "username": data[0],
                "password": data[1],
                "level": int(data[2]),
                "class_name": data[3],
                "artifacts": data[4].split(",") if data[4] else []
            }
    return None

# Загрузка списка доступных артефактов из "копилки"
def load_artifacts_pool():
    if not os.path.exists(ARTIFACTS_FILE):
        # Если файла нет, создаем его и наполняем всеми артефактами
        save_artifacts_pool(ALL_POSSIBLE_ARTIFACTS)
        return ALL_POSSIBLE_ARTIFACTS
    
    f = open(ARTIFACTS_FILE, "r", encoding="utf-8")
    content = f.read().strip()
    f.close()
    if not content:
        return []
    return content.split(",")

# Сохранение списка артефактов в файл "копилки"
def save_artifacts_pool(artifacts_list):
    f = open(ARTIFACTS_FILE, "w", encoding="utf-8")
    f.write(",".join(artifacts_list))
    f.close()

# Генерация новых артефактов, когда старые закончились
def generate_new_artifacts():
    print("Все артефакты собраны! Генерируем новые...")
    save_artifacts_pool(ALL_POSSIBLE_ARTIFACTS)
    return ALL_POSSIBLE_ARTIFACTS

# Получение случайного артефакта из копилки
def get_random_artifact():
    pool = load_artifacts_pool()
    if not pool:
        # Если копилка пуста, генерируем заново
        pool = generate_new_artifacts()
    
    # Выбираем случайный
    art = random.choice(pool)
    # Удаляем его из копилки, так как он теперь у игрока
    pool.remove(art)
    save_artifacts_pool(pool)
    return art

# Возврат артефактов в копилку (если игрок не сохранился)
def return_artifacts_to_pool(player_artifacts):
    pool = load_artifacts_pool()
    for art in player_artifacts:
        # Если такого артефакта еще нет в копилке, добавляем его
        if art and art not in pool:
            pool.append(art)
    save_artifacts_pool(pool)
    print("Артефакты вернулись в копилку.")
