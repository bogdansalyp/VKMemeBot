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
from PIL import Image, ImageFont, ImageDraw

FONT = 'fonts/arial.ttf'
RESULT_IMAGE_PATH = 'img/result.jpg'


def draw_watermark(image, watermark_text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, 50)
    draw.text((image.size[0] - font.getsize(watermark_text)[0], image.size[1] - font.getsize(watermark_text)[1]), watermark_text, (128,128,128), font=font)


def split_to_lines(message, symbols_to_fit):
    new_lines = []
    current_word = ''
    for ix, word in enumerate(message.replace('\n',' ').split(' ')):
        if len(current_word) + len(word) < symbols_to_fit:
            if ix != 0:
                current_word = current_word + ' ' + word
            else:
                current_word = word
        else:
            new_lines.append(current_word)
            current_word = word
    new_lines.append(current_word)
    return new_lines


def handle_ok(message):
    original_image_path = 'img/ok.jpg'
    original_img = Image.open(original_image_path)

    # Rescale the image
    whitespace_x = int(original_img.size[0] * 1.3)
    whitespace_y = int(original_img.size[0] * 0.9)
    whitespace_size = (whitespace_x, whitespace_y)
    new_image = Image.new('RGB', whitespace_size, (255,255,255))
    
    # Position new image
    new_position_x = -150
    new_position_y = int(whitespace_size[1] - original_img.size[1])
    new_position = (new_position_x, new_position_y)
    new_image.paste(original_img, new_position)
    
    # Add text
    FONT_SIZES = [220, 200, 180, 150, 130, 100]
    TEXT_MARGIN_RIGHT = 0.05
    TEXT_MARGIN_TOP = 200
    
    draw = ImageDraw.Draw(new_image)

    text_position_x = int(whitespace_size[0] * 0.5)
    text_position_y = TEXT_MARGIN_TOP

    margin = whitespace_x * TEXT_MARGIN_RIGHT
    
    # Try to write text in one line
    text_written = False
    for font_size in FONT_SIZES:
        font = ImageFont.truetype(FONT, font_size)
        font_width = font.getsize(message)[0]
        available_width = text_position_x - margin
        if ((font_width < available_width) and not (text_written)):
            draw.text((text_position_x, text_position_y), message, (0,0,0), font=font)
            text_written = True
            
    # Write text multiline
    if not text_written:
        font = ImageFont.truetype(FONT, 100)
        font_width = font.getsize(message)[0]
        text_position_x = int(whitespace_size[0] / 3)
        available_width = whitespace_x - (text_position_x + margin)
        symbols_to_fit = 100
        while(font.getsize('a'*symbols_to_fit)[0] > available_width):
            symbols_to_fit -= 1

        new_lines = split_to_lines(message, symbols_to_fit)

        # Resize image
        for line in new_lines:
            whitespace_y += font.getsize('A')[1]
            new_position_y += font.getsize('A')[1]
        whitespace_y -= font.getsize('A')[1] * 4
        new_position_y -= font.getsize('A')[1] * 4

        whitespace_size = (whitespace_x, whitespace_y)
        new_image = Image.new('RGB', whitespace_size, (255,255,255))
        new_position = (new_position_x, new_position_y)
        new_image.paste(original_img, new_position)
        draw = ImageDraw.Draw(new_image)

        # Write multiline
        for line in new_lines:
            draw.text((text_position_x, text_position_y), line, (0,0,0), font=font)
            text_position_y += font.getsize('A')[1]

    # Watermark
    draw_watermark(new_image, 'vk.com/postironic_bot')
    
    # Resize an image
    wert = new_image.resize((int(whitespace_size[0] / 4), int(whitespace_size[1] / 4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(RESULT_IMAGE_PATH)
    return RESULT_IMAGE_PATH


def handle_poker_face(message):
    original_image_path = 'img/poker_face.jpg'
    original_img = Image.open(original_image_path)

    # Rescale the image
    whitespace_x = int(original_img.size[0] * 1.6)
    whitespace_y = int(original_img.size[1] * 1.1)
    whitespace_size = (whitespace_x, whitespace_y)
    new_image = Image.new('RGB', whitespace_size, (255,255,255))
    
    # Position new image
    new_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    new_position_y = 350
    new_position = (new_position_x, new_position_y)
    new_image.paste(original_img, new_position)
    
    # Add text
    FONT_SIZES = [220, 200, 180, 150, 130, 100]
    TEXT_MARGIN_RIGHT = 0.05
    TEXT_MARGIN_TOP = 100

    draw = ImageDraw.Draw(new_image)

    text_position_x = int(whitespace_size[0] * 0.3)
    text_position_y = TEXT_MARGIN_TOP

    margin = whitespace_x * TEXT_MARGIN_RIGHT
    
    # Try to write text in one line
    text_written = False
    for font_size in FONT_SIZES:
        font = ImageFont.truetype(FONT, font_size)
        font_width = font.getsize(message)[0]
        available_width = text_position_x - margin
        if ((font_width < available_width) and not (text_written)):
            draw.text((text_position_x, text_position_y), message, (0,0,0), font=font)
            text_written = True
            
    # Write text multiline
    if not text_written:
        font = ImageFont.truetype(FONT, 100)
        font_width = font.getsize(message)[0]
        text_position_x = int(whitespace_size[0] * 0.05)
        available_width = whitespace_x - (text_position_x + margin)
        symbols_to_fit = 100
        while(font.getsize('a'*symbols_to_fit)[0] > available_width):
            symbols_to_fit -= 1

        new_lines = split_to_lines(message, symbols_to_fit)

        # Resize image
        for line in new_lines:
            whitespace_y += font.getsize('A')[1]
            new_position_y += font.getsize('A')[1]
        whitespace_y -= font.getsize('A')[1] * 5
        new_position_y -= font.getsize('A')[1] * 5

        whitespace_size = (whitespace_x, whitespace_y)
        new_image = Image.new('RGB', whitespace_size, (255,255,255))
        new_position = (new_position_x, new_position_y)
        new_image.paste(original_img, new_position)
        draw = ImageDraw.Draw(new_image)

        # Write multiline
        for line in new_lines:
            draw.text((text_position_x, text_position_y), line, (0,0,0), font=font)
            text_position_y += font.getsize('A')[1]

    # Watermark
    draw_watermark(new_image, 'vk.com/postironic_bot')

    # Resize an image
    wert = new_image.resize((int(whitespace_size[0] / 4), int(whitespace_size[1] / 4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(RESULT_IMAGE_PATH)
    return RESULT_IMAGE_PATH

def handle_poker_face_2(message):
    original_image_path = 'img/poker_face_2.jpg'
    original_img = Image.open(original_image_path)

    # Rescale the image
    whitespace_x = int(original_img.size[0] * 2.6)
    whitespace_y = int(original_img.size[1] * 1.3)
    whitespace_size = (whitespace_x, whitespace_y)
    new_image = Image.new('RGB', whitespace_size, (255,255,255))
    
    # Position new image
    new_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    new_position_y = int((whitespace_size[1] - original_img.size[1]) * 1.2)
    new_position = (new_position_x, new_position_y)
    new_image.paste(original_img, new_position)
    
    # Add text
    FONT_SIZES = [80]
    TEXT_MARGIN_RIGHT = 0.05
    TEXT_MARGIN_TOP = 100

    draw = ImageDraw.Draw(new_image)

    text_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    text_position_y = int(whitespace_size[0] / 7)

    margin = whitespace_x * TEXT_MARGIN_RIGHT
    
    # Try to write text in one line
    text_written = False
    for font_size in FONT_SIZES:
        font = ImageFont.truetype(FONT, font_size)
        font_width = font.getsize(message)[0]
        available_width = text_position_x - margin
        if ((font_width < available_width) and not (text_written)):
            draw.text((text_position_x, text_position_y), message, (0,0,0), font=font)
            text_written = True
            
    # Write text multiline
    if not text_written:
        font = ImageFont.truetype(FONT, 60)
        font_width = font.getsize(message)[0]
        text_position_x = int(whitespace_size[0] * 0.05)
        text_position_y = 100
        available_width = whitespace_x - (text_position_x + margin)
        symbols_to_fit = 100
        while(font.getsize('a'*symbols_to_fit)[0] > available_width):
            symbols_to_fit -= 1

        new_lines = split_to_lines(message, symbols_to_fit)

        # Resize image
        for line in new_lines:
            whitespace_y += font.getsize('A')[1]
            new_position_y += font.getsize('A')[1]
        whitespace_y -= font.getsize('A')[1] * 5
        new_position_y -= font.getsize('A')[1] * 5

        whitespace_size = (whitespace_x, whitespace_y)
        new_image = Image.new('RGB', whitespace_size, (255,255,255))
        new_position = (new_position_x, new_position_y)
        new_image.paste(original_img, new_position)
        draw = ImageDraw.Draw(new_image)

        # Write multiline
        for line in new_lines:
            draw.text((text_position_x, text_position_y), line, (0,0,0), font=font)
            text_position_y += font.getsize('A')[1]

    # Watermark
    draw_watermark(new_image, 'vk.com/postironic_bot')

    # Resize an image
    wert = new_image.resize((int(whitespace_size[0] / 4), int(whitespace_size[1] / 4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(RESULT_IMAGE_PATH)
    return RESULT_IMAGE_PATH


def handle_poker_face_3(message):
    original_image_path = 'img/poker_face_3.png'
    original_img = Image.open(original_image_path)

    # Rescale the image
    whitespace_x = int(original_img.size[0] * 2.6)
    whitespace_y = int(original_img.size[1] * 1.5)
    whitespace_size = (whitespace_x, whitespace_y)
    new_image = Image.new('RGB', whitespace_size, (255,255,255))
    
    # Position new image
    new_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    new_position_y = int((whitespace_size[1] - original_img.size[1]) * 1.2)
    new_position = (new_position_x, new_position_y)
    new_image.paste(original_img, new_position)
    
    # Add text
    FONT_SIZES = [80]
    TEXT_MARGIN_RIGHT = 0.05
    TEXT_MARGIN_TOP = 100

    draw = ImageDraw.Draw(new_image)

    text_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    text_position_y = int(whitespace_size[0] / 7)

    margin = whitespace_x * TEXT_MARGIN_RIGHT
    
    # Try to write text in one line
    text_written = False
    for font_size in FONT_SIZES:
        font = ImageFont.truetype(FONT, font_size)
        font_width = font.getsize(message)[0]
        available_width = text_position_x - margin
        if ((font_width < available_width) and not (text_written)):
            draw.text((text_position_x, text_position_y), message, (0,0,0), font=font)
            text_written = True
            
    # Write text multiline
    if not text_written:
        font = ImageFont.truetype(FONT, 60)
        font_width = font.getsize(message)[0]
        text_position_x = int(whitespace_size[0] * 0.05)
        text_position_y = 100
        available_width = whitespace_x - (text_position_x + margin)
        symbols_to_fit = 100
        while(font.getsize('a'*symbols_to_fit)[0] > available_width):
            symbols_to_fit -= 1

        new_lines = split_to_lines(message, symbols_to_fit)

        # Resize image
        for line in new_lines:
            whitespace_y += font.getsize('A')[1]
            new_position_y += font.getsize('A')[1]
        whitespace_y -= font.getsize('A')[1]
        new_position_y -= font.getsize('A')[1]

        whitespace_size = (whitespace_x, whitespace_y)
        new_image = Image.new('RGB', whitespace_size, (255,255,255))
        new_position = (new_position_x, new_position_y)
        new_image.paste(original_img, new_position)
        draw = ImageDraw.Draw(new_image)

        # Write multiline
        for line in new_lines:
            draw.text((text_position_x, text_position_y), line, (0,0,0), font=font)
            text_position_y += font.getsize('A')[1]

    # Watermark
    draw_watermark(new_image, 'vk.com/postironic_bot')

    # Resize an image
    wert = new_image.resize((int(whitespace_size[0] / 4), int(whitespace_size[1] / 4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(RESULT_IMAGE_PATH)
    return RESULT_IMAGE_PATH


def handle_me_only(message):
    original_image_path = 'img/me_only.jpg'
    original_img = Image.open(original_image_path)

    # Rescale the image
    whitespace_x = int(original_img.size[0] * 5)
    whitespace_y = int(original_img.size[1] * 1.5)
    whitespace_size = (whitespace_x, whitespace_y)
    new_image = Image.new('RGB', whitespace_size, (255,255,255))
    
    # Position new image
    new_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    new_position_y = int((whitespace_size[1] - original_img.size[1]) * 1.2)
    new_position = (new_position_x, new_position_y)
    new_image.paste(original_img, new_position)
    
    # Add text
    FONT_SIZES = [150, 120, 100, 80]
    TEXT_MARGIN_RIGHT = 0.05
    TEXT_MARGIN_TOP = 100

    draw = ImageDraw.Draw(new_image)

    text_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    text_position_y = int(whitespace_size[0] / 7)

    margin = whitespace_x * TEXT_MARGIN_RIGHT
    
    # Try to write text in one line
    text_written = False
    for font_size in FONT_SIZES:
        font = ImageFont.truetype(FONT, font_size)
        font_width = font.getsize(message)[0]
        available_width = whitespace_x - (text_position_x + margin)
        if ((font_width < available_width) and not (text_written)):
            draw.text((text_position_x, text_position_y), message, (0,0,0), font=font)
            text_written = True
            
    # Write text multiline
    if not text_written:
        font = ImageFont.truetype(FONT, 60)
        font_width = font.getsize(message)[0]
        text_position_x = int(whitespace_size[0] * 0.15)
        text_position_y = 300
        available_width = whitespace_x - (text_position_x + margin)
        symbols_to_fit = 100
        while(font.getsize('a'*symbols_to_fit)[0] > available_width):
            symbols_to_fit -= 1

        new_lines = split_to_lines(message, symbols_to_fit)

        # Resize image
        for line in new_lines:
            whitespace_y += font.getsize('A')[1]
            new_position_y += font.getsize('A')[1]
        whitespace_y -= font.getsize('A')[1] * 5
        new_position_y -= font.getsize('A')[1] * 5

        whitespace_size = (whitespace_x, whitespace_y)
        new_image = Image.new('RGB', whitespace_size, (255,255,255))
        new_position = (new_position_x, new_position_y)
        new_image.paste(original_img, new_position)
        draw = ImageDraw.Draw(new_image)

        # Write multiline
        for line in new_lines:
            draw.text((text_position_x, text_position_y), line, (0,0,0), font=font)
            text_position_y += font.getsize('A')[1]

    # Watermark
    draw_watermark(new_image, 'vk.com/postironic_bot')
    
    # Resize an image
    wert = new_image.resize((int(whitespace_size[0] / 4), int(whitespace_size[1] / 4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(RESULT_IMAGE_PATH)
    return RESULT_IMAGE_PATH


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
                    'label': '1'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': '2'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': '3'
                },
                'color': 'negative'
            }
        ],
        [
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': '4'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': '5'
                },
                'color': 'negative'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': '0'
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
    if number == 0:
        number = random.randint(1, 5)

    # Select a handler
    if number == 1:
        image_path = handle_ok(message)
    elif number == 2:
        image_path = handle_poker_face(message)
    elif number == 3:
        image_path = handle_poker_face_2(message)
    elif number == 4:
        image_path = handle_poker_face_3(message)
    elif number == 5:
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
                r.set(str(event.user_id) + 'number', int(event.text))
            elif user_status == b'writing a message':
                number = int(r.get(str(event.user_id) + 'number'))
                # Generate a text and image
                answer, image_path = handle_msg(event.text, number)
                r.delete(event.user_id)
                # Send a message back
                write_msg(event.user_id, answer, image_path)
            else:
                write_hello_msg(event.user_id)
                r.delete(event.user_id)

            print('Text: ', event.text)
