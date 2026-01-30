from constants import ROOMS


def show_inventory(game_state):
    """Показывает инвентарь игрока"""
    inventory = game_state['player_inventory']

    if inventory:
        print("\nВаш инвентарь:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("\nВаш инвентарь пуст.")


def get_input(prompt="> "):
    """Получает ввод от пользователя с обработкой ошибок"""
    try:
        user_input = input(prompt).strip().lower()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]

    if direction in current_room['exits']:
        # Обновляем текущую комнату
        game_state['current_room'] = current_room['exits'][direction]
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1

        print(f"\nВы пошли {direction}...")
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """Позволяет игроку подобрать предмет"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]
    
    # Проверяем, не пытается ли игрок взять сундук
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return False
    
    if item_name in current_room['items']:
        # Добавляем предмет в инвентарь
        game_state['player_inventory'].append(item_name)
        # Удаляем предмет из комнаты
        current_room['items'].remove(item_name)
        
        print(f"Вы подняли: {item_name}")
        return True
    else:
        print("Такого предмета здесь нет.")
        return False


def use_item(game_state, item_name):
    """Использование предмета из инвентаря"""
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return False

    # Уникальные действия для каждого предмета
    if item_name == 'torch':
        print("Вы зажгли факел. Стало светлее!")

    elif item_name == 'sword':
        print("Вы почувствовали уверенность, держа меч в руках.")

    elif item_name == 'bronze_box':
        print("Вы открыли бронзовую шкатулку.")
        if 'rusty_key' not in inventory:
            game_state['player_inventory'].append('rusty_key')
            print("Внутри вы нашли rusty_key!")
        else:
            print("Шкатулка пуста.")

    else:
        print(f"Вы не знаете, как использовать {item_name}.")

    return True
