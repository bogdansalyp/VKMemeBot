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

import keyboards
import handle_images
from config import *


def write_msg(user_id, message, image_path):

    # Upload the photo
    upload_url = vk.method('photos.getMessagesUploadServer', {'peer_id': 0})['upload_url']
    response = requests.post(upload_url, files = {'photo': open('img/result.jpg', 'rb')})
    json_data = json.loads(response.text)

    # Send a message with photo
    result = vk.method('photos.saveMessagesPhoto', {'server': json_data['server'], 'photo': json_data['photo'], 'hash': json_data['hash']})
    
    buttons = keyboards.initial_keyboard

    button_json = json.dumps(buttons)

    vk.method('messages.send', {
        'user_id': user_id, 
        'message': '', 
        'attachment': 'photo{}_{}'.format(result[0]['owner_id'], result[0]['id']), 
        'keyboard': button_json,
        'random_id': random.randint(1, 9999)
    })


def write_hello_msg(user_id):
    buttons = keyboards.initial_keyboard

    button_json = json.dumps(buttons)

    vk.method('messages.send', {
        'user_id': user_id, 
        'message': 'Привет',
        'keyboard': button_json,
        'random_id': random.randint(1, 9999)
    })


def show_numbers(user_id):
    buttons = keyboards.templates_keyboard;

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
        image_path = handle_images.handle_ok(message)
    elif number == b"poker face":
        image_path = handle_images.handle_poker_face(message)
    elif number == b"poker face 2":
        image_path = handle_images.handle_poker_face_2(message)
    elif number == b"really":
        image_path = handle_images.handle_poker_face_3(message)
    elif number == b"hmmmm":
        image_path = handle_images.handle_me_only(message)
    elif number == b"sladko":
        image_path = handle_images.handle_sladko(message)
    elif number == b"gorko":
        image_path = handle_images.handle_gorko(message)
    elif number == b"a pochemu":
        image_path = handle_images.handle_pochemu(message)
    elif message.lower() =='анекдот' or message.lower() == 'анек':
        data = pd.read_csv('data/anekdot_ru.csv')
        message = np.random.choice(data['text'])
        image_path = handle_images.handle_ok(message)
    else:
        image_path = handle_images.handle_ok("начни сообщение с цифры до 5")
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

            # User just opened chat
            if user_status == None:
                if event.text == 'Создать картинку':
                    # Show first message
                    show_numbers(event.user_id)
                    r.set(event.user_id, 'choosing numbers')
                    print('Create a picture branch')
                elif event.text == 'Анекдот':
                    answer, image_path = handle_msg(event.text)
                    write_msg(event.user_id, answer, image_path)
                    r.delete(event.user_id)
                else:
                    write_hello_msg(event.user_id)
                    r.delete(event.user_id)
            
            # User decided to choose a meme template
            elif user_status == b'choosing numbers':
                if event.text in AVAILABLE_TEMPLATES:
                    print('Choosing numbers branch')
                    write_prompt_select_text(event.user_id)
                    r.set(event.user_id, 'writing a message')
                    r.set(str(event.user_id) + 'number', event.text)
                else:
                    write_hello_msg(event.user_id)
                    r.delete(event.user_id)
            
            # User has chosen a meme template; now writes a phrase
            elif user_status == b'writing a message':
                number = r.get(str(event.user_id) + 'number')
                print(number)
                # Generate a text and image
                answer, image_path = handle_msg(event.text, number)
                r.delete(event.user_id)
                # Send a message back
                write_msg(event.user_id, answer, image_path)

            # Unknown user status
            else:
                write_hello_msg(event.user_id)
                r.delete(event.user_id)

            print('Text: ', event.text)
