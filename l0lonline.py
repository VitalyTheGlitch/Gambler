import socket
import threading
import hashlib
import base64
import sys
import json


class Client:
    def __init__(self, token=None, debug=False, language='ru', tag=''):
        self.token = None
        self.client_socket = None
        self.debug = debug
        self.tag = tag
        self.language = language
        self.uid = None
        self.receive = []
        self.create_connection()
        self.sign(self.get_session_key())

        if token:
            self.signin_by_access_token(token)

    def create_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5000)
        self.client_socket.connect(('49.12.2.202', 10001))
        self.client_socket.settimeout(None)

        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            buffer = bytes()

            while True:
                r = self.client_socket.recv(4096)

                buffer += r

                read = len(r)

                if read != -1:
                    try:
                        d = buffer.decode()
                    except:
                        continue

                    if d.endswith('\n'):
                        buffer = bytes()

                        for s in d.strip().split('\n'):
                            s = s[0:-1]
                            pos = s.find('{')
                            command = s[:pos]

                            try:
                                message = json.loads(s[pos:] + '}')
                            except:
                                continue

                            if command != 'uu' and command != 'free':
                                message['command'] = command
                                self.receive.append(message)

                    else:
                        buffer = buffer + r

                else:
                    return

    def send_server(self, data: dir):
        self.client_socket.send((data.pop('command') + json.dumps(data, separators=(',', ':')).replace('{}', '') + '\n').encode())

    def get_session_key(self):
        data = {
            'command': 'c',
            'd': 'Blackview BV4900Pro',
            'v': '1.3.0',
            'tz': '+04:00',
            'and': 29,
            'pl': 'android',
            'l': self.language,
            'n': '101.android',
            'p': 10
        }

        self.send_server(data)

        return self.listen()['key']

    def sign(self, key):
        sign_hash = base64.b64encode(hashlib.md5((key + 'oc3q7ingf978mx457fgk4587fg847').encode()).digest()).decode()

        self.send_server({
            'command': 'sign',
            'hash': sign_hash
        })

        return self.listen()

    def signin_by_access_token(self, token):
        self.token = token
        self.send_server({
            'command': 'auth',
            'token': self.token
        })

        authorized = self.listen()

        if authorized['command'] == 'err':
            try:
                print('\nError: {}'.format(authorized['code']))
            except:
                print('\nUnknown error occured')

        self.uid = authorized['id']

        return self.uid

    def google_auth(self, id_token):
        self.send_server({
            'command': '101_google_auth',
            'id_token': id_token
        })

    def get_captcha(self):
        self.send_server({
            'command': 'get_captcha'
        })

    def register(self, name, captcha=''):
        self.send_server({
            'command': 'register',
            'name': name,
            'captcha': captcha
        })

        data = self.listen()

        if data['command'] == 'err':
            try:
                print('\nError: {}'.format(data['code']))
            except:
                print('\nUnknown error occured')
        else:
            return data['token']

    def get_user_info(self, user_id):
        self.send_server({
            'command': 'get_user_info',
            'id': user_id
        })

    def friend_accept(self, friend_id):
        self.send_server({
            'command': 'friend_accept',
            'id': friend_id
        })

    def friend_delete(self, friend_id):
        self.send_server({
            'command': 'friend_delete',
            'id': friend_id
        })

    def send_friend_request(self, user_id):
        self.send_server({
            'command': 'friend_request',
            'id': user_id
        })

        return self.listen()

    def verify_purchase(self, signature, purchase_data):
        self.send_server({
            'command': 'verify_purchase',
            'signature': signature,
            'purchase_data': purchase_data
        })

    def get_purchase_ids(self):
        self.send_server({
            'command': 'get_android_purchase_ids'
        })

    def get_prem_price(self):
        self.send_server({
            'command': 'get_prem_price'
        })

    def get_points_price(self):
        self.send_server({
            'command': 'get_points_price'
        })

    def buy_prem(self, item_id=0):
        self.send_server({
            'command': 'buy_prem',
            'id': f'com.rstgames.101.prem.{item_id}'
        })

    def buy_points(self, item_id=0):
        self.send_server({
            'command': 'buy_points',
            'id': f'com.rstgames.101.points.{item_id}'
        })

        return self.listen()

    def buy_asset(self, asset_id):
        self.send_server({
            'command': 'buy_asset',
            'id': asset_id
        })

    def get_friend_list(self):
        self.send_server({
            'command': 'friend_list'
        })

        friends = []

        data = self.listen()

        while data['command'] != 'img_msg_price':
            friends.append(data)
            data = self.listen()

        return friends

    def join_to_game(self, game_id, password=''):
        if password:
            self.send_server({
                'command': 'join',
                'password': password,
                'id': game_id
            })

        else:
            self.send_server({
                'command': 'join',
                'id': game_id
            })

    def rejoin_to_game(self, position, game_id):
        self.send_server({
            'command': 'rejoin',
            'p': position,
            'id': game_id
        })

    def leave(self, game_id):
        self.send_server({
            'command': 'leave',
            'id': game_id
        })

    def game_publish(self):
        self.send_server({
            'command': 'game_publish'
        })

    def get_assets(self):
        self.send_server({
            'command': 'get_assets'
        })

    def asset_select(self, asset_id):
        self.send_server({
            'command': 'asset_select',
            'id': asset_id
        })

    def achieve_select(self, achieve_id):
        self.send_server({
            'command': 'achieve_select',
            'id': achieve_id
        })

    def send_smile_game(self, smile_id=1):
        self.send_server({
            'command': 'smile',
            'id': smile_id
        })

    def ready(self):
        self.send_server({
            'command': 'ready'
        })

    def surrender(self):
        self.send_server({
            'command': 'surrender'
        })

    def complaint(self, user_id):
        self.send_server({
            'command': 'complaint',
            'id': user_id
        })

    def player_swap(self, position):
        self.send_server({
            'command': 'player_swap',
            'id': position
        })

    def send_message_friend(self, content, to):
        self.send_server({
            'command': 'send_user_msg',
            'msg': content,
            'to': to
        })

    def send_user_message_code(self, code, content):
        self.send_server({
            'command': 'send_user_msg_code',
            'code': code,
            'msg': content
        })

    def delete_message(self, message_id):
        self.send_server({
            'command': 'delete_msg',
            'msg_id': message_id
        })

    def gift_coll_item(self, item_id, coll_id, to):
        self.send_server({
            'command': 'gift_coll_item',
            'item_id': item_id,
            'coll_id': coll_id,
            'to_id': to
        })

    def get_bets(self):
        self.send_server({
            'command': 'gb'
        })

    def create_game(self, bet=100, password='', fast=True, players=3, deck=36, hand=4):
        if password:
            self.send_server({
                'command': 'create',
                'bet': bet,
                'password': password,
                'fast': fast,
                'players': players,
                'deck': deck,
                'hand': hand
            })

        else:
            self.send_server({
                'command': 'create',
                'bet': bet,
                'fast': fast,
                'players': players,
                'deck': deck,
                'hand': hand
            })

    def invite_to_game(self, user_id):
        self.send_server({
            'command': 'invite_to_game',
            'user_id': user_id
        })

    def lookup_start(self, betMin=100, pr=False, betMax=1000, fast=None, players=None, deck=None, hand=None):
        if hand is None:
            hand = [4, 5, 6]

        if fast is None:
            fast = [False, True]

        if deck is None:
            deck = [36]

        if players is None:
            players = [3, 4]

        if not pr:
            self.send_server({
                'command': 'lookup_start',
                'betMin': betMin,
                'betMax': betMax,
                'pr': [False],
                'fast': fast,
                'players': players,
                'deck': deck,
                'hand': hand
            })

        else:
            self.send_server({
                'command': 'lookup_start',
                'pr': [True]
            })

    def lookup_stop(self):
        self.send_server({
            'command': 'lookup_stop'
        })

    def get_server(self):
        self.send_server({
            'command': 'get_server'
        })

    def update_name(self, nickname=None):
        self.send_server({
            'command': 'update_name',
            'value': nickname
        })

    def save_note(self, note, user_id, color=0):
        self.send_server({
            'command': 'save_note',
            'note': note,
            'color': color,
            'id': user_id
        })

    def leaderboard_get_by_user(self, user_id, info_type='score', season=False):
        s = '' if not season else 's_'

        self.send_server({
            'command': s + 'lb_get_by_user',
            'user_id': user_id,
            'type': info_type
        })

    def leaderboard_get_top(self, info_type='score'):
        self.send_server({
            'command': 'lb_get_top',
            'type': info_type
        })

    def leaderboard_get_by_place_down(self, place=20, info_type='score'):
        self.send_server({
            'command': 'lb_get_by_place_down',
            'place': place,
            'type': info_type
        })

    def turn(self, card):
        self.send_server({
            'command': 't',
            'c': card
        })

    def take(self):
        self.send_server({
            'command': 'take'
        })

    def tpass(self):
        self.send_server({
            'command': 'pass'
        })

    def suit(self, suit):
        self.send_server({
            'command': 's',
            's': suit
        })

    def show_discard(self):
        self.send_server({
            'command': 'show_discard'
        })

    def listen(self):
        while not self.receive:
            pass

        r = self.receive[0]

        self.receive.pop(0)

        return r
