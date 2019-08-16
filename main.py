import vk_api
import key
import random
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import json
import random
import numpy as np
import pandas as pd
import redis

from handle_images import handle_ok, handle_poker_face, handle_poker_face_2, handle_poker_face_3, handle_me_only

FONT = 'fonts/arial.ttf'
RESULT_IMAGE_PATH = 'img/result.jpg'


def write_msg(user_id, message, image_path):

    # Upload the photo
    upload_url = vk.method('photos.getMessagesUploadServer', {'peer_id': 0})['upload_url']
    response = requests.post(upload_url, files = {'photo': open('img/result.jpg', 'rb')})
    json_data = json.loads(response.text)

    # Send a message with photo
    result = vk.method('photos.saveMessagesPhoto', {'server': json_data['server'], 'photo': json_data['photo'], 'hash': json_data['hash']})
    
    buttons = {}
    buttons['one_time'] = True
    buttons['buttons'] = []
    buttons['buttons'].append([])
    buttons['buttons'][0].append({})
    buttons['buttons'][0][0]['action'] = {}
    buttons['buttons'][0][0]['action']['type'] = 'text'
    buttons['buttons'][0][0]['action']['payload'] = "{\"button\": \"1\"}"
    buttons['buttons'][0][0]['action']['label'] = 'Создать картинку'
    buttons['buttons'][0][0]['color'] = 'negative'
    buttons['buttons'].append([])
    buttons['buttons'][1].append({})
    buttons['buttons'][1][0]['action'] = {}
    buttons['buttons'][1][0]['action']['type'] = 'text'
    buttons['buttons'][1][0]['action']['payload'] = "{\"button\": \"1\"}"
    buttons['buttons'][1][0]['action']['label'] = 'Анекдот'

    button_json = json.dumps(buttons)

    button_json = json.dumps(buttons)
    vk.method('messages.send', {
        'user_id': user_id, 
        'message': '', 
        'attachment': 'photo{}_{}'.format(result[0]['owner_id'], result[0]['id']), 
        'keyboard': button_json,
        'random_id': random.randint(1, 9999)
    })


def write_hello_msg(user_id):
    buttons = {}
    buttons['one_time'] = True
    buttons['buttons'] = []
    buttons['buttons'].append([])
    buttons['buttons'][0].append({})
    buttons['buttons'][0][0]['action'] = {}
    buttons['buttons'][0][0]['action']['type'] = 'text'
    buttons['buttons'][0][0]['action']['payload'] = "{\"button\": \"1\"}"
    buttons['buttons'][0][0]['action']['label'] = 'Создать картинку'
    buttons['buttons'][0][0]['color'] = 'negative'
    buttons['buttons'].append([])
    buttons['buttons'][1].append({})
    buttons['buttons'][1][0]['action'] = {}
    buttons['buttons'][1][0]['action']['type'] = 'text'
    buttons['buttons'][1][0]['action']['payload'] = "{\"button\": \"1\"}"
    buttons['buttons'][1][0]['action']['label'] = 'Анекдот'

    button_json = json.dumps(buttons)

    vk.method('messages.send', {
        'user_id': user_id, 
        'message': 'Привет',
        'keyboard': button_json,
        'random_id': random.randint(1, 9999)
    })


def show_numbers(user_id):
    buttons = {}
    buttons['one_time'] = True
    buttons['buttons'] = [
        [
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': 'cool ok'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': 'poker face'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': 'poker face 2'
                },
                'color': 'negative'
            }
        ],
        [
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': 'really'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': 'hmmmm'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': 'random'
                }
            }
        ]
    ]

    button_json = json.dumps(buttons)

    vk.method('messages.send', {
        'user_id': user_id, 
        'message': 'Выбери номер картинки',
        'keyboard': button_json,
        'random_id': random.randint(1, 9999)
    })


def write_prompt_select_text(user_id):
    vk.method('messages.send', {
        'user_id': user_id, 
        'message': 'Теперь пиши свою фразу:',
        'keyboard': json.dumps({}),
        'random_id': random.randint(1, 9999)
    })


# API-ключ созданный ранее
token = key.key

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

def handle_msg(message, number=None):
    if number == b"random":
        number = np.random.choice([b"cool ok", b"poker face", b"poker face 2", b"really", b"hmmmm"])

    # Select a handler
    if number == b"cool ok":
        image_path = handle_ok(message)
    elif number == b"poker face":
        image_path = handle_poker_face(message)
    elif number == b"poker face 2":
        image_path = handle_poker_face_2(message)
    elif number == b"really":
        image_path = handle_poker_face_3(message)
    elif number == b"hmmmm":
        image_path = handle_me_only(message)
    elif message.lower() =='анекдот' or message.lower() == 'анек':
        data = pd.read_csv('data/anekdot_ru.csv')
        message = np.random.choice(data['text'])
        image_path = handle_ok(message)
    else:
        image_path = handle_ok("начни сообщение с цифры до 5")
    return message, image_path

print("Server started")

# Set up database
r = redis.Redis(host='localhost', port=6379, db=0)

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print('New message:')
            print(f'For me by: {event.user_id}')

            user_status = r.get(event.user_id)
            print(user_status)

            if user_status == None and event.text == 'Создать картинку':
                # Show first message
                show_numbers(event.user_id)
                r.set(event.user_id, 'choosing numbers')
                print('Create a picture branch')
            elif user_status == None and event.text == 'Анекдот':
                answer, image_path = handle_msg(event.text)
                write_msg(event.user_id, answer, image_path)
                r.delete(event.user_id)
            elif user_status == b'choosing numbers':
                print('Choosing numbers branch')
                write_prompt_select_text(event.user_id)
                r.set(event.user_id, 'writing a message')
                r.set(str(event.user_id) + 'number', event.text)
            elif user_status == b'writing a message':
                number = r.get(str(event.user_id) + 'number')
                print("TRIED TO CREATE AN IMAGEs")
                print(number)
                # Generate a text and image
                answer, image_path = handle_msg(event.text, number)
                r.delete(event.user_id)
                # Send a message back
                write_msg(event.user_id, answer, image_path)
            else:
                write_hello_msg(event.user_id)
                r.delete(event.user_id)

            print('Text: ', event.text)
