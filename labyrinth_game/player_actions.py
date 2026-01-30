from constants import ROOMS
from utils import random_event
def show_inventory(game_state):
    """Показывает инвентарь игрока"""
    inventory = game_state['player_inventory']

    if inventory:
        print("\nВаш инвентарь:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("\nВаш инвентарь пуст.")
def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]

    if direction in current_room['exits']:
        target_room = current_room['exits'][direction]

        if target_room == 'treasure_room':
            inventory = game_state['player_inventory']

            if 'rusty_key' in inventory:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False

        game_state['current_room'] = target_room
        game_state['steps_taken'] += 1

        print(f"\nВы пошли {direction}...")

        game_state = random_event(game_state)

        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False

def take_item(game_state, item_name):
    """Позволяет игроку подобрать предмет"""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return False

    if item_name in current_room['items']:
        game_state['player_inventory'].append(item_name)
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