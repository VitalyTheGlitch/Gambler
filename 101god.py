import os
import random
import time
from colorama import Fore, Back, init
import l0lonline

init(autoreset=True)


def clear():
    os.system('cls')


def banner():
    clear()

    print(f'{Fore.GREEN}101GOD\n')


def get_card(card_id):
    card = ''
    suit = card_id

    while suit >= 0:
        suit -= 4
    suit += 4

    if suit == 0:
        card += '♣'
    elif suit == 1:
        card += '♦'
    elif suit == 2:
        card += '♥'
    elif suit == 3:
        card += '♠'

    value = card_id // 4 + 2

    if value < 11:
        card += str(value)
    elif value == 11:
        card += 'J'
    elif value == 12:
        card += 'Q'
    elif value == 13:
        card += 'K'
    elif value == 14:
        card += 'A'

    return card


def get_points(card):
    if card[1] == 'Q' and card[0] == '♠':
        return 40

    elif card[1] == 'Q':
        return 20

    elif card[1] == 'K' and card[0] == '♠':
        return 40

    elif card[1] == 'K':
        return 4

    elif card[1] == 'A':
        return 11

    elif card[1] == 'J':
        return 2

    elif card[1] == '9':
        return 0

    elif int(card[1]) <= 8:
        return int(card[1])

    else:
        return 10


def start(l0l, p, position, players):
    cards = []
    cards_n = []
    table = []
    smiles = []
    takes = 0
    points = 0
    eight = False
    eight_suit = None
    six_or_seven = False
    queen = False
    suit = -1
    turn = -1
    me = False
    start = True
    surrender = False
    last_mode = None

    banner()

    print(f'{Fore.GREEN}Игра началась!\n')
    print(f'{Fore.GREEN}ВЫ', 'обозначаетесь', f'{Fore.GREEN}ЗЕЛЕНЫМ', 'цветом\n')
    print(f'{Fore.CYAN}(Чтобы сдаться, нажмите CTRL+C)\n')

    while True:
        data = l0l.listen()

        if data['command'] == 'err':
            print(f'\n{Back.RED}Ошибка:', data['code'])
            data = l0l.listen()
            choose = 'y'
            break

        elif data['command'] == 'order' and turn == -1:
            turn = data['ids'][0]

        elif data['command'] == 'hand':
            cards = []
            cards_n = []

            print(f'\n{Back.CYAN}Ваши карты:', end=' ')

            for card in range(len(data['cards'])):
                if get_card(data['cards'][card]) not in cards:
                    cards.append(get_card(data['cards'][card]))

                if data['cards'][card] not in cards_n:
                    cards_n.append(data['cards'][card])

                print(get_card(data['cards'][card]), end=' ')

        elif data['command'] == 'turn':
            table = []

            print(f'\n{Back.CYAN}Карты на столе:', end=' ')

            for card in range(len(data['table'])):
                table.append(get_card(data['table'][card]))

                print(get_card(data['table'][card]), end=' ')

            print(f'\n{Back.CYAN}Карт в стопке:', data['deck'])

        elif data['command'] == 'mode':
            if data[str(position)] >= 6:
                if not start:
                    me = True
                    if queen:
                        l0l.suit(random.randint(0, 3))
                        queen = False
                        me = False
            last_mode = data[str(position)]
        elif data['command'] == 'hs':
            points = data['s']
            print(f'\n{Back.CYAN}Ваши очки:', data['s'])
        elif data['command'] == 't':
            if data['id'] == position:
                print(f'\n{Fore.GREEN}Игрок {data["id"]}({players[data["id"]]}) сходил картой {get_card(data["c"])}')
                if start:
                    if data['c'] in [40, 41, 42, 43]:
                        queen = True
                        me = False
                try:
                    cards.remove(get_card(data['c']))
                    cards_n.remove(data['c'])
                except:
                    pass
            else:
                print(f'\nИгрок {data["id"]}({players[data["id"]]}) сходил картой {get_card(data["c"])}')

            start = False

            if get_card(data['c']) not in table:
                table.append(get_card(data['c']))

            suit = -1
        elif data['command'] == 'h':
            try:
                six_or_seven = data['sv']
            except:
                six_or_seven = False

            try:
                if last_mode >= 6:
                    eight = data['a']
                else:
                    eight = False
            except:
                eight = False

            try:
                if len(data) == 3 and data['t'] == 1 and data['s'] >= 0:
                    suit = data['s']
            except:
                pass

        elif data['command'] == 'smile':
            print(data)
            smiles.append(data['id'])
        elif data['command'] == 'surrender':
            surrender = data['id']
        elif data['command'] == 'shuffle':
            print(f'\n{Back.CYAN}Колода перетасована!')
        elif data['command'] == 'p_off':
            print(f'\nИгрок {data["id"]} вышел из сети!')
        elif data['command'] == 'p_on':
            print(f'\nИгрок {data["id"]} вернулся!')
        elif data['command'] == 'game_over':
            over = []
            winner = -1
            you = -1

            for player in range(len(data['win'])):
                if len(data['win'][str(player)]['c']) == 0:
                    winner = player
                try:
                    over.append(data['win'][str(player)]['s'])
                except KeyError:
                    over.append(0)
            over = sorted(over)
            for i in range(len(over)):
                if over[i] == points:
                    you = i + 1
            if winner == position:
                print(f'\n{Back.GREEN}Победа!')
            elif winner > -1:
                print(f'\n{Back.RED}Игра окончена! Выиграл игрок {winner}!')
                if data['win'][str(position)]['s101']:
                    print(f'\n{Back.GREEN}Вы заняли {you} место, закончив игру с 101 очками!')
                else:
                    if p == 2 or (p == 3 and you == 3) or (p == 4 and you > 2) or (p == 5 and you > 2) or (
                            p == 6 and you > 3):
                        print(f'\n{Back.RED}Вы заняли {you} место!')
                    else:
                        print(f'\n{Back.GREEN}Вы заняли {you} место!')
            elif surrender:
                print(f'\n{Back.GREEN}Победа! Игрок {surrender} сдался!')
            else:
                print(f'\n{Back.RED}Игра окончена в результате неизвестного исхода!')

            choose = input(f'\n{Fore.CYAN}Продолжить?(Y/n): ')
            break

        if me:
            available = []
            available_p = []
            last_card = table[-1]

            if six_or_seven:
                if last_card[1] == '6':
                    for i in range(len(cards)):
                        if cards[i][1] == '6':
                            available.append(cards_n[i])
                            available_p.append(get_points(cards[i]))
                elif last_card[1] == '7':
                    for i in range(len(cards)):
                        if cards[i][1] == '7':
                            available.append(cards_n[i])
                            available_p.append(get_points(cards[i]))
            elif eight:
                for i in range(len(cards)):
                    if cards[i][1] == '8' or cards[i][0] == eight_suit or cards[i][1] == 'Q':
                        available.append(cards_n[i])
                        available_p.append(get_points(cards[i]))
            else:
                if suit > -1:
                    for i in range(len(cards)):
                        if get_card(suit)[0] == cards[i][0] or cards[i][1] == 'Q':
                            available.append(cards_n[i])
                            available_p.append(get_points(cards[i]))
                else:
                    all_available_eights = []
                    best_eight = None
                    for i in range(len(cards)):
                        if last_card[0] == cards[i][0] or last_card[1:] == cards[i][1:] or cards[i][1] == 'Q':
                            if cards[i][1] == '8':
                                all_available_eights.append(cards[i][0])
                            available.append(cards_n[i])
                            available_p.append(get_points(cards[i]))
                    if len(all_available_eights) > 0:
                        found = False
                        for i in range(len(all_available_eights)):
                            if found:
                                break
                            for j in range(len(cards)):
                                if cards[j][0] == all_available_eights[i]:
                                    if cards[j][0] == '♣':
                                        best_eight = 24
                                    elif cards[j][0] == '♦':
                                        best_eight = 25
                                    elif cards[j][0] == '♥':
                                        best_eight = 26
                                    elif cards[j][0] == '♠':
                                        best_eight = 27
                                    found = True
                                    break
                    if best_eight != None:
                        for i in range(len(available)):
                            if available == best_eight:
                                available_p[i] = 100

            if len(available) > 0:
                z = 0

                for i in range(len(available_p)):
                    if available_p[i] == max(available_p):
                        z = i
                        break

                l0l.turn(available[z])

                if available[z] in [40, 41, 42, 43]:
                    queen = True
                elif available[z] in [24, 25, 26, 27]:
                    eight_suit = get_card(available[z])[0]

                print(f'\n{Fore.GREEN}Игрок {position}({players[position]}) сходил картой {get_card(available[z])}')

                try:
                    cards.remove(get_card(available[z]))
                    cards_n.remove(available[z])
                except:
                    pass

                takes = 0
            else:
                takes += 1

                if eight:
                    if takes == 4:
                        l0l.tpass()
                        print(f'\n{Fore.GREEN}Игрок {position}({players[position]}) пропустил ход')
                        takes = 0
                    else:
                        l0l.take()
                        print(f'\n{Fore.GREEN}Игрок {position}({players[position]}) взял')
                elif six_or_seven:
                    l0l.take()
                    print(f'\n{Fore.GREEN}Игрок {position}({players[position]}) взял')
                    takes = 0
                else:
                    if takes == 2:
                        l0l.tpass()
                        print(f'\n{Fore.GREEN}Игрок {position}({players[position]}) пропустил ход')
                        takes = 0
                    else:
                        l0l.take()
                        print(f'\n{Fore.GREEN}Игрок {position}({players[position]}) взял')
            me = False

    try:
        if choose.lower() == 'y':
            return True
        else:
            return False
    except:
        return False


def wait(l0l, game, pr, position=None, players={}):
    banner()

    print(f'{Back.CYAN}Название:', game['name'])
    print(f'{Back.CYAN}Игроков:', game['p'])
    print(f'{Back.CYAN}Ставка:', game['bet'])
    print(f'\n\n{Back.GREEN}Успешный вход в игру!')
    print(f'\n{Fore.GREEN}ВЫ', 'обозначаетесь', f'{Fore.GREEN}ЗЕЛЕНЫМ', 'цветом')
    print(f'\n{Fore.CYAN}Ожидание игроков... (Чтобы выйти из комнаты до начала, нажмите CTRL+C)')

    for i in range(len(players)):
        if i == position:
            print(f'\n{Fore.GREEN}Игрок {i}({players[i]}) зашел в игру')
        else:
            print(f'\nИгрок {i}({players[i]}) зашел в игру')

    players_ready = 0
    x = 3

    try:
        if pr:
            l0l.game_publish()
        while players_ready != game['p'] - 1:
            data = l0l.listen()

            if data['command'] == 'cp':
                position = data['id']
                print(f'\n{Fore.GREEN}Игрок {data["id"]}({data["user"]["name"]}) зашел в игру')
                players[data['id']] = data['user']['name']
            if data['command'] == 'ready_on':
                if data['id'] == position:
                    print(f'\n{Fore.GREEN}Игрок {data["id"]} готов')
                else:
                    print(f'\nИгрок {data["id"]} готов')
                players_ready += 1
            elif data['command'] == 'p' and len(data) == 3 and data['user'] == None:
                print(f'\nИгрок {data["id"]} вышел')
                players_ready = 0
            elif data['command'] == 'p':
                try:
                    print(f'\nИгрок {data["id"]}({data["user"]["name"]}) зашел в игру')
                    players[data['id']] = data['user']['name']
                except:
                    pass
            elif data['command'] == 'ready_timeout':
                x = 1
                break
    except KeyboardInterrupt:
        l0l.leave(game['id'])
        x = 0

    if x == 0:
        print(f'\n{Fore.CYAN}Вы вышли из комнаты!')
        time.sleep(2)
    elif x == 1:
        print(f'\n{Back.RED}Ошибка: ready_timeout!')
        time.sleep(2)
    else:
        l0l.ready()
        try:
            r = start(l0l, game['p'], position, players)
        except KeyboardInterrupt:
            l0l.surrender()
            data = l0l.listen()
            data = l0l.listen()
            print(f'\n{Back.RED}Вы сдались!')
            r = input(f'\n{Fore.CYAN}Продолжить?(Y/n): ')
        if r:
            wait(l0l, game, pr, position, players)


def get_games(l0l, betMin, betMax, pr):
    banner()
    print(f'\n{Fore.CYAN}Игры:')

    if not pr:
        l0l.lookup_start(betMin=betMin, betMax=betMax)
    else:
        l0l.lookup_start(pr=True)

    data = l0l.listen()
    l0l.lookup_stop()

    for i in range(len(data['g'])):
        if data['g'][i]['p'] - data['g'][i]['cp'] > 0:
            print('\n' + Back.CYAN + str(i) + '.', 'Название:', data['g'][i]['name'])
            print(f'{Back.GREEN}ID:', data['g'][i]['id'])
            print(f'{Back.GREEN}Игроков:', data['g'][i]['cp'], '/', data['g'][i]['p'])
            print(f'{Back.GREEN}Ставка:', data['g'][i]['bet'])
        else:
            data['g'].pop(i)
            i -= 2

    return data['g']


def main(l0l, betMin, betMax, pr):
    banner()

    while True:
        try:
            if not pr:
                games = get_games(l0l, betMin, betMax, 0)
            else:
                games = get_games(l0l, 1, 1, pr)
        except KeyError:
            continue
        if len(games) == 0:
            print(f'\n{Back.CYAN}Игр не найдено! Повторная проверка через 5с...')
            time.sleep(5)
            continue
        try:
            choose = int(input(f'\n{Fore.CYAN}Номер игры(100 для обновления): '))
        except ValueError:
            continue
        if choose < 0 or choose >= len(games):
            continue

        if pr:
            password = int(input(f'\n{Fore.CYAN}Введите пароль(100 для отмены): '))
            l0l.join_to_game(games[choose]['id'], password)
        else:
            l0l.join_to_game(games[choose]['id'])
        data = l0l.listen()

        if data['command'] == 'gd' or data['command'] == 'gl' or data['command'] == 'g':
            if pr:
                print(f'\n{Back.RED}Ошибка: Неверный пароль!')
                time.sleep(2)
                continue
            while data['command'] == 'gd' or data['command'] == 'gl' or data['command'] == 'g':
                data = l0l.listen()
        if data['command'] == 'err':
            print(f'\n{Back.RED}Ошибка:', data['code'])
            time.sleep(2)
        else:
            wait(l0l, games[choose], pr)
            break


def choose_bets(l0l):
    banner()

    try:
        betMin = int(input(f'\n{Fore.CYAN}Минимальная ставка(по умолчанию 100): '))
        print(f'\n{Back.GREEN}Минимальная ставка:', betMin)
    except ValueError:
        betMin = 100
        print(f'\n{Back.GREEN}Минимальная ставка:', betMin)
    try:
        betMax = int(input(f'\n{Fore.CYAN}Максимальная ставка(по умолчанию 1000): '))
        print(f'\n{Back.GREEN}Максимальная ставка:', betMax)
    except ValueError:
        betMax = 1000
        print(f'\n{Back.GREEN}Максимальная ставка:', betMax)

    time.sleep(1)
    main(l0l, betMin, betMax, 0)


def choose_game(l0l):
    banner()

    print(f'\n{Back.CYAN}0.', 'Поиск публичных игр')
    print(f'{Back.CYAN}1.', 'Поиск приватных игр')

    try:
        pr = int(input(f'\n{Fore.CYAN}Выбор(по умолчанию 0): '))

        if pr < 0 or pr > 1:
            pr = 0
    except ValueError:
        pr = 0

    print(f'\n{Back.GREEN}Выбор:', pr)

    time.sleep(1)

    if not pr:
        choose_bets(l0l)
    else:
        main(l0l, 1, 1, pr)

    choose_game(l0l)


l0l = l0lonline.Client('$2a$06$6fy8UJ1/5qDA1JY4pmbWnu')

choose_game(l0l)
