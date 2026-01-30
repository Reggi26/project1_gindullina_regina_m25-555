from constants import ROOMS
import math

def get_input(prompt="> "):
    """Получает ввод от пользователя с обработкой ошибок"""
    try:
        user_input = input(prompt).strip().lower()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
def describe_current_room(game_state):
    """Выводит описание текущей комнаты"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    print(f"\n== {current_room_name.upper()} ==")
    
    print(room['description'])
    
    if room['items']:
        print("\nЗаметные предметы:")
        for item in room['items']:
            print(f"  - {item}")
    
    if room['exits']:
        print("\nВыходы:")
        for direction, target_room in room['exits'].items():
            print(f"  {direction}: {target_room}")
    
    if room['puzzle'] is not None:
        print("\nКажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Функция решения загадок"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return
    
    question, correct_answer = room['puzzle']
    
    print(f"\n{question}")
    user_answer = get_input("Ваш ответ: ")
    
    if user_answer.lower() == correct_answer.lower():
        print("Верно! Загадка решена!")
        room['puzzle'] = None
        
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
    
    if current_room_name != 'treasure_room' or 'treasure_chest' not in room['items']:
        print("Здесь нет сундука с сокровищами.")
        return False
    
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
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
def pseudo_random(seed: int, modulo: int):
    print("seed =", seed, "modulo =", modulo)
    if modulo < 0:
        print("modulo должно быть неотрицательным числом")
        return
        # raise ValueError("modulo должно быть неотрицательным числом")

    if modulo == 0:
        return 0

    sin_value = math.sin(seed * 12.9898)

    multiplied = sin_value * 43758.5453

    fractional_part = multiplied - math.floor(multiplied)

    scaled_value = fractional_part * modulo

    return math.floor(scaled_value)


def trigger_trap(game_state):
    """
    Функция имитирует срабатывание ловушки.
    """
    print("\n" + "=" * 50)
    print("Ловушка активирована! Пол стал дрожать...")
    print("=" * 50)

    inventory = game_state.get('player_inventory', [])

    if inventory:
        item_count = len(inventory)

        seed = game_state.get('steps_taken', 0)
        random_index = pseudo_random(seed, item_count)

        removed_item = inventory.pop(random_index)

        print(f"Вы потеряли предмет: '{removed_item}'!")

        game_state['player_inventory'] = inventory

    else:
        print("Ваш инвентарь пуст...")
        print("Ловушка наносит прямой урон!")

        seed = game_state.get('steps_taken', 0) + 100
        damage_roll = pseudo_random(seed, 10)

        if damage_roll < 3:
            print("Вы не смогли избежать ловушки... Поражение!")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться!")

    return game_state


def random_event(game_state):
    """
    Создает случайные события во время перемещения игрока.
    """
    seed = game_state.get('steps_taken', 0)
    event_chance = pseudo_random(seed, 10)

    if event_chance not in {0,1,2,3,7,9}:
        return game_state

    print("\n--- Случайное событие! ---")

    seed2 = seed + 100
    event_type = pseudo_random(seed2, 3)  # 0, 1 или 2

    if event_type == 0:
        # Сценарий 1: Находка
        print("Вы нашли на полу монетку!")

        current_room = game_state.get('current_room', 'unknown')
        room = ROOMS.get(current_room, {})

        if room:
            if 'coin' not in room['items']:
                room['items'].append('coin')
            else:
                print("Здесь уже есть монетка.")

    elif event_type == 1:
        # Сценарий 2: Испуг
        print("Вы слышите странный шорох...")

        inventory = game_state.get('player_inventory', [])
        if 'sword' in inventory:
            print("Вы достаете меч и отпугиваете существо!")
        else:
            print("Существо скрывается в темноте...")

    elif event_type == 2:
        # Сценарий 3: Срабатывание ловушки
        print("Вы чувствуете опасность...")

        current_room = game_state.get('current_room', '')
        inventory = game_state.get('player_inventory', [])

        if current_room == 'trap_room' and 'torch' not in inventory:
            print("Ловушка активирована!")
            game_state = trigger_trap(game_state)
        else:
            print("Опасность миновала.")
    return game_state