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

    return 10


def start(l0l, p, position, players):
    cards = []
    cards_n = []
    table = []
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

    print(f'{Fore.GREEN}Game started\n')
    print(f'{Fore.GREEN}YOU', 'are marked in', f'{Fore.GREEN}GREEN\n')
    print(f'{Fore.CYAN}(To surrender, press CTRL+C)\n')

    while True:
        data = l0l.listen()

        if data['command'] == 'err':
            print(f'\n{Back.RED}Error:', data['code'])

            data = l0l.listen()

            choice = 'y'

            break

        elif data['command'] == 'order' and turn == -1:
            turn = data['ids'][0]

        elif data['command'] == 'hand':
            cards = []
            cards_n = []

            print(f'\n{Back.CYAN}Your cards:', end=' ')

            for card in range(len(data['cards'])):
                if get_card(data['cards'][card]) not in cards:
                    cards.append(get_card(data['cards'][card]))

                if data['cards'][card] not in cards_n:
                    cards_n.append(data['cards'][card])

                print(get_card(data['cards'][card]), end=' ')

        elif data['command'] == 'turn':
            table = []

            print(f'\n{Back.CYAN}Cards on the table:', end=' ')

            for card in range(len(data['table'])):
                table.append(get_card(data['table'][card]))

                print(get_card(data['table'][card]), end=' ')

            print(f'\n{Back.CYAN}Cards in the deck:', data['deck'])

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

            print(f'\n{Back.CYAN}Your score:', data['s'])

        elif data['command'] == 't':
            if data['id'] == position:
                print(f'\n{Fore.GREEN}Player {data["id"]}({players[data["id"]]}) played the {get_card(data["c"])}')

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
                print(f'\nPlayer {data["id"]}({players[data["id"]]}) played the {get_card(data["c"])}')

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

        elif data['command'] == 'surrender':
            surrender = data['id']

        elif data['command'] == 'shuffle':
            print(f'\n{Back.CYAN}Deck shuffled')

        elif data['command'] == 'p_off':
            print(f'\nPlayer {data["id"]} went offline')

        elif data['command'] == 'p_on':
            print(f'\nPlayer {data["id"]} is back')

        elif data['command'] == 'game_over':
            over = []
            winner = -1
            you = -1

            for player in range(len(data['win'])):
                if not data['win'][str(player)]['c']:
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
                print(f'\n{Back.GREEN}Victory')

            elif winner > -1:
                print(f'\n{Back.RED}Game over. The winner is {winner}')

                if data['win'][str(position)]['s101']:
                    print(f'\n{Back.GREEN}You took {you} place, finishing the game with 101 points')

                else:
                    if p == 2 or (p == 3 and you == 3) or (p == 4 and you > 2) or (p == 5 and you > 2) or (p == 6 and you > 3):
                        print(f'\n{Back.RED}You took {you} place')

                    else:
                        print(f'\n{Back.GREEN}You took {you} place')

            elif surrender:
                print(f'\n{Back.GREEN}Victory\n\nPlayer {surrender} surrendered')

            else:
                print(f'\n{Back.RED}The game is over as a result of an unknown outcome')

            choice = input(f'\n{Fore.CYAN}Continue? (Y/n): ')

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

                    if all_available_eights:
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

                    if best_eight is not None:
                        for i in range(len(available)):
                            if available == best_eight:
                                available_p[i] = 100

            if available:
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

                print(f'\n{Fore.GREEN}Player {position}({players[position]}) played the {get_card(available[z])}')

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

                        print(f'\n{Fore.GREEN}Player {position}({players[position]}) missed a turn')

                        takes = 0

                    else:
                        l0l.take()

                        print(f'\n{Fore.GREEN}Player {position}({players[position]}) took')

                elif six_or_seven:
                    l0l.take()

                    print(f'\n{Fore.GREEN}Player {position}({players[position]}) took')

                    takes = 0

                else:
                    if takes == 2:
                        l0l.tpass()

                        print(f'\n{Fore.GREEN}Player {position}({players[position]}) missed a turn')

                        takes = 0

                    else:
                        l0l.take()

                        print(f'\n{Fore.GREEN}Player {position}({players[position]}) took')

            me = False

    try:
        return choice.lower() == 'y'
    except:
        return False


def wait(l0l, game, pr, position=None, players={}):
    banner()

    print(f'{Back.CYAN}Name:', game['name'])
    print(f'{Back.CYAN}Players:', game['p'])
    print(f'{Back.CYAN}Bet:', game['bet'])
    print(f'\n\n{Back.GREEN}Successful entry into the game')
    print(f'\n{Fore.GREEN}YOU', 'are marked in', f'{Fore.GREEN}GREEN')
    print(f'\n{Fore.CYAN}Waiting for players... (To leave the room before it starts, press CTRL+C)')

    for i in range(len(players)):
        if i == position:
            print(f'\n{Fore.GREEN}Player {i}({players[i]}) joined the game')

        else:
            print(f'\nPlayer {i}({players[i]}) joined the game')

    players_ready = 0
    x = 3

    try:
        if pr:
            l0l.game_publish()

        while players_ready != game['p'] - 1:
            data = l0l.listen()

            if data['command'] == 'cp':
                position = data['id']

                print(f'\n{Fore.GREEN}Player {data["id"]}({data["user"]["name"]}) joined the game')

                players[data['id']] = data['user']['name']

            if data['command'] == 'ready_on':
                if data['id'] == position:
                    print(f'\n{Fore.GREEN}Player {data["id"]} is ready')

                else:
                    print(f'\nPlayer {data["id"]} is ready')

                players_ready += 1

            elif data['command'] == 'p' and len(data) == 3 and data['user'] is None:
                print(f'\nPlayer {data["id"]} left the game')

                players_ready = 0

            elif data['command'] == 'p':
                try:
                    print(f'\nPlayer {data["id"]}({data["user"]["name"]}) joined the game')

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
        print(f'\n{Fore.CYAN}You left the room')

        time.sleep(2)

    elif x == 1:
        print(f'\n{Back.RED}Timeout error')

        time.sleep(2)

    else:
        l0l.ready()

        try:
            r = start(l0l, game['p'], position, players)
        except KeyboardInterrupt:
            l0l.surrender()

            data = l0l.listen()
            data = l0l.listen()

            print(f'\n{Back.RED}You surrendered')

            r = input(f'\n{Fore.CYAN}Continue? (Y/n): ')

        if r:
            wait(l0l, game, pr, position, players)


def get_games(l0l, min_bet, max_bet, pr):
    banner()

    print(f'\n{Fore.CYAN}Games:')

    if not pr:
        l0l.lookup_start(min_bet=min_bet, max_bet=max_bet)

    else:
        l0l.lookup_start(pr=True)

    data = l0l.listen()

    l0l.lookup_stop()

    for i in range(len(data['g'])):
        if data['g'][i]['p'] - data['g'][i]['cp'] > 0:
            print(f'\n{Back.CYAN}{i}.', 'Name:', data['g'][i]['name'])
            print(f'{Back.GREEN}ID:', data['g'][i]['id'])
            print(f'{Back.GREEN}Playes:', data['g'][i]['cp'], '/', data['g'][i]['p'])
            print(f'{Back.GREEN}Bet:', data['g'][i]['bet'])

        else:
            data['g'].pop(i)

            i -= 2

    return data['g']


def main(l0l, min_bet, max_bet, pr):
    banner()

    while True:
        try:
            if not pr:
                games = get_games(l0l, min_bet, max_bet, 0)

            else:
                games = get_games(l0l, 1, 1, pr)
        except KeyError:
            continue

        if not games:
            print(f'\n{Back.CYAN}No games found. Re-check after 5s...')

            time.sleep(5)

            continue

        try:
            choice = int(input(f'\n{Fore.CYAN}Game number (100 to refresh): '))
        except ValueError:
            continue

        if choice < 0 or choice >= len(games):
            continue

        if pr:
            password = int(input(f'\n{Fore.CYAN}Password (100 to cancel): '))

            l0l.join_to_game(games[choice]['id'], password)

        else:
            l0l.join_to_game(games[choice]['id'])

        data = l0l.listen()

        if data['command'] in ['g', 'gd', 'gl']:
            if pr:
                print(f'\n{Back.RED}Error: Incorrect password')

                time.sleep(2)

                continue

            while data['command'] in ['g', 'gd', 'gl']:
                data = l0l.listen()

        if data['command'] == 'err':
            print(f'\n{Back.RED}Error:', data['code'])

            time.sleep(2)

        else:
            wait(l0l, games[choice], pr)

            break


def choose_bets(l0l):
    banner()

    try:
        min_bet = int(input(f'\n{Fore.CYAN}Minimum bet [100]: '))

        print(f'\n{Back.GREEN}Minimum bet:', min_bet)
    except ValueError:
        min_bet = 100

        print(f'\n{Back.GREEN}Minimum bet:', min_bet)

    try:
        max_bet = int(input(f'\n{Fore.CYAN}Maximum bet [1000]: '))

        print(f'\n{Back.GREEN}Maximum bet:', max_bet)
    except ValueError:
        max_bet = 1000

        print(f'\n{Back.GREEN}Maximum bet:', max_bet)

    time.sleep(1)
    main(l0l, min_bet, max_bet, 0)


def choose_game(l0l):
    banner()

    print(f'\n{Back.CYAN}0.', 'Search for public games')
    print(f'{Back.CYAN}1.', 'Search for public games')

    try:
        pr = int(input(f'\n{Fore.CYAN}Choice [0]: '))

        if pr < 0 or pr > 1:
            pr = 0
    except ValueError:
        pr = 0

    print(f'\n{Back.GREEN}Choice:', pr)

    time.sleep(1)

    if not pr:
        choose_bets(l0l)

    else:
        main(l0l, 1, 1, pr)

    choose_game(l0l)


l0l = l0lonline.Client('$2a$06$6fy8UJ1/5qDA1JY4pmbWnu')

choose_game(l0l)
