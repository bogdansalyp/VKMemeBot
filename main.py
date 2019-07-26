import vk_api
import key
import random
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import json
import random
from PIL import Image, ImageFont, ImageDraw

FONT = 'fonts/arial.ttf'
RESULT_IMAGE_PATH = 'img/result.jpg'


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
    draw = ImageDraw.Draw(new_image)

    text_position_x = int(whitespace_size[0] / 2)
    text_position_y = 200

    margin = whitespace_x / 20
    
    
    text_written = False
    for font_size in [220, 200, 180, 150, 130, 100]:
        font = ImageFont.truetype(FONT, font_size)
        font_width = font.getsize(message)[0]
        available_width = text_position_x - margin
        if ((font_width < available_width) and not (text_written)):
            draw.text((text_position_x, text_position_y), message, (0,0,0), font=font)
            text_written = True
            
    if not text_written:
        text_position_y = 200
        font = ImageFont.truetype(FONT, 100)

        font = ImageFont.truetype(FONT, font_size)
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
    whitespace_y = int(original_img.size[1] * 1.3)
    whitespace_size = (whitespace_x, whitespace_y)
    new_image = Image.new('RGB', whitespace_size, (255,255,255))
    
    # Position new image
    new_position_x = int((whitespace_size[0] - original_img.size[0]) / 2.5)
    new_position_y = int((whitespace_size[1] - original_img.size[1]) * 1.2)
    new_position = (new_position_x, new_position_y)
    new_image.paste(original_img, new_position)
    
    # Add text
    font = ImageFont.truetype(FONT, 140)
    text_position_x = int(whitespace_size[0] / 4)
    text_position_y = int(whitespace_size[0] / 7)
    text_position = (text_position_x, text_position_y)
    draw = ImageDraw.Draw(new_image)
    draw.text(text_position, message, (0,0,0), font=font)

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
    font = ImageFont.truetype(FONT, 80)
    text_position_x = int(whitespace_size[0] / 4)
    text_position_y = int(whitespace_size[0] / 7)
    text_position = (text_position_x, text_position_y)
    draw = ImageDraw.Draw(new_image)
    draw.text(text_position, message, (0,0,0), font=font)

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
    font = ImageFont.truetype(FONT, 80)
    text_position_x = int(whitespace_size[0] / 4)
    text_position_y = int(whitespace_size[1] / 7)
    text_position = (text_position_x, text_position_y)
    draw = ImageDraw.Draw(new_image)
    draw.text(text_position, message, (0,0,0), font=font)

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
    font = ImageFont.truetype(FONT, 80)
    text_position_x = int(whitespace_size[0] / 4)
    text_position_y = int(whitespace_size[1] / 7)
    text_position = (text_position_x, text_position_y)
    draw = ImageDraw.Draw(new_image)
    draw.text(text_position, message, (0,0,0), font=font)

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
    vk.method('messages.send', {'user_id': user_id, 'message': '', 'attachment': 'photo{}_{}'.format(result[0]['owner_id'], result[0]['id']), 'random_id': random.randint(1, 9999)})


# API-ключ созданный ранее
token = key.key

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

def handle_msg(message):
    if message.startswith('1'):
        image_path = handle_ok(event.text.split(' ', 1)[1])
    elif message.startswith('2'):
        image_path = handle_poker_face(event.text.split(' ', 1)[1])
    elif message.startswith('3'):
        image_path = handle_poker_face_2(event.text.split(' ', 1)[1])
    elif message.startswith('4'):
        image_path = handle_poker_face_3(event.text.split(' ', 1)[1])
    elif message.startswith('5'):
        image_path = handle_me_only(event.text.split(' ', 1)[1])
    elif message.startswith('0'):
        message = str(random.randint(1, 5)) + message[1:]
        message, image_path = handle_msg(message)
    else:
        image_path = handle_ok("начни сообщение с цифры до 5")
    return message, image_path

print("Server started")
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print('New message:')
            print(f'For me by: {event.user_id}')

            # Generate a text and image
            answer, image_path = handle_msg(event.text)

            # Send a message back
            write_msg(event.user_id, answer, image_path)

            print('Text: ', event.text)
