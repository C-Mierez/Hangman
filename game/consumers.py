from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import hangedman


class GameConsumer(AsyncWebsocketConsumer):
    games = {}

    async def connect(self):
        # Obtener el room_name a partir de la url
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Definir nombre del Group
        self.room_group_name = 'game_%s' % self.room_name

        # Crear el Group
        await self.channel_layer.group_add(
            self.room_group_name,
            # Puntero al channel_layer que va a llegar al consumer
            self.channel_name
        )

        if self.room_group_name not in self.games:
            game = hangedman.HangedMan()
            self.games[self.room_group_name] = game

        # TODO: Quirar print
        print(self.games)

        await self.accept()

    async def disconnect(self, code):
        game = self.games[self.room_group_name]
        game.removeUsername(
            self.scope['user'].username
        )
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'state': "disconnect",
                    'message': {
                        'username': self.scope['user'].username,
                        'cUser': game.currentUser()
                    }
                }
            )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        return super().disconnect(code)

    async def receive(self, text_data):
        data_json = json.loads(text_data)

        event = data_json['event']
        message = data_json['message']
        inpt = message.pop('input', None)
        cword = None
        guessResult = None
        username = self.scope['user'].username
        # Uso del Modelo
        game = self.games[self.room_group_name]
        if event == "start":
            game.addUsername(username)
            state = "init"
            message = {
                'cword' : game.cword(),
                'cUser' : game.currentUser(),
                'username': username,
            }
        else:
            canPlay = game.canPlay(username)

            if canPlay:
                if event == "letter":
                    guessResult = game.guessLetter(inpt)
                    cword = game.cword()
                    if len(inpt) != 0:
                        inpt = inpt[0]
                    else:
                        inpt = '🤐'
                elif event == "word":
                    guessResult = game.guessWord(inpt)
                    cword = game.cword()
                    if len(inpt) == 0:
                        inpt = '🤐'
                # TODO: Evento para ganar
                cUser = game.currentUser()
                gameSolved = game.checkIfSolved()
                if gameSolved:
                    state = "solved"
                else:
                    state = "unsolved"
                
                message = {
                    'cword': cword,
                    'cUser': cUser,
                    'input': inpt,
                    'guessResult': guessResult,
                    'username': username,
                }
            else:
                state = "invalidTurn"
                message = {
                    'username': username,
                }
        print(game.usernames())
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'state': state,
                    'message': message
                }
            )

    async def send_message(self, event):
        state = event['state']
        message = event['message']

        await self.send(
            text_data=json.dumps({
                'state': state,
                'message': message,
            })
        )

    
