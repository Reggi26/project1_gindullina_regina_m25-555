from constants import ROOMS
from player_actions import get_input


def describe_current_room(game_state):
    """Выводит описание текущей комнаты"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Название комнаты в верхнем регистре
    print(f"\n== {current_room_name.upper()} ==")
    
    # Описание комнаты
    print(room['description'])
    
    # Список предметов
    if room['items']:
        print("\nЗаметные предметы:")
        for item in room['items']:
            print(f"  - {item}")
    
    # Доступные выходы
    if room['exits']:
        print("\nВыходы:")
        for direction, target_room in room['exits'].items():
            print(f"  {direction}: {target_room}")
    
    # Сообщение о загадке
    if room['puzzle'] is not None:
        print("\nКажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Функция решения загадок"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Проверяем, есть ли загадка в комнате
    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return
    
    question, correct_answer = room['puzzle']
    
    # Выводим вопрос и получаем ответ
    print(f"\n{question}")
    user_answer = get_input("Ваш ответ: ")
    
    # Сравниваем ответы
    if user_answer.lower() == correct_answer.lower():
        print("Верно! Загадка решена!")
        # Убираем загадку из комнаты
        room['puzzle'] = None
        
        # Добавляем награду в зависимости от комнаты
        if current_room_name == 'treasure_room':
            print("Вы получаете доступ к сокровищу!")
        elif current_room_name == 'hall':
            print("Пьедестал опускается, открывая потайной отсек!")
            if 'treasure_key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('treasure_key')
                print("Вы нашли treasure_key!")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """Логика открытия сундука с сокровищами"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Проверяем, что мы в комнате с сокровищами и сундук еще есть
    if current_room_name != 'treasure_room' or 'treasure_chest' not in room['items']:
        print("Здесь нет сундука с сокровищами.")
        return False
    
    # Проверка наличия ключа
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. У вас нет подходящего ключа.")
    choice = get_input("Попробовать ввести код? (да/нет): ")
    
    if choice.lower() in ['да', 'yes', 'y']:
        if room['puzzle'] is not None:
            question, correct_answer = room['puzzle']
            print(f"\n{question}")
            user_code = get_input("Введите код: ")
            
            if user_code == correct_answer:
                print("Код принят! Сундук открывается!")
                room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return True
            else:
                print("Неверный код. Сундук остается запертым.")
                return False
        else:
            print("Загадка уже решена, но без ключа сундук не открыть.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False

# labyrinth_game/utils.py
def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")