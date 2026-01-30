from player_actions import (
    # get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from utils import (
    get_input,
    attempt_open_treasure,
    describe_current_room,
    solve_puzzle,
    show_help
)
from constants import COMMANDS

# Состояние игры
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}
def process_command(game_state, command):
    """Обрабатывает команды пользователя"""
    parts = command.split()
    if not parts:
        return

    main_command = parts[0]
    argument = parts[1] if len(parts) > 1 else None

    match main_command:
        case 'show_help':
            show_help(COMMANDS)
            print('Что вы хотите сделать?')
            command = get_input()
            process_command(game_state, command)

        case 'look':
            describe_current_room(game_state)

        case 'go' | 'move' | 'north' | 'south' | 'east' | 'west':
            if main_command in ['go', 'move'] and argument:
                direction = argument
            else:
                direction = main_command

            if move_player(game_state, direction):
                describe_current_room(game_state)

        case 'take' | 'get':
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите предмет для взятия.")

        case 'use':
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите предмет для использования.")

        case 'solve':
            current_room = game_state['current_room']
            if current_room == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case 'open':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                print("Нечего открывать здесь.")

        case 'inventory' | 'inv':
            show_inventory(game_state)

        case 'quit' | 'exit':
            print("Спасибо за игру! До свидания!")
            game_state['game_over'] = True

        case _:
            print(
                "Неизвестная команда. Попробуйте: look, go [направление], "
                "take [предмет], use [предмет], solve, open, inventory, quit"
            )

def main():
    """Основная функция игры"""
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("=" * 40)

    describe_current_room(game_state)

    while not game_state['game_over']:
        print("\nЧто вы хотите сделать?")
        print(
            "Доступные команды: show_help, look, go [направление], take [предмет], "
            "use [предмет], solve, open, inventory, quit"
        )

        command = get_input()
        process_command(game_state, command)

    if game_state['steps_taken'] > 0:
        print(f"\nИгра завершена! Вы сделали {game_state['steps_taken']} шагов.")


if __name__ == "__main__":
    main()

    # # test pseudo_random
    # for i in range(5):
    #     print(f"{pseudo_random(i, 35)}")
    #     print("==============")