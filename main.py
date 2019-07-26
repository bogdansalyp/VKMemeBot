import vk_api
import key
import random
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import json
from PIL import Image, ImageFont, ImageDraw


def handle_ok(message):
    original_image_path = 'img/ok.jpg'
    result_image_path = 'img/result.jpg'

    img = Image.open(original_image_path)
    size = (int(max(img.size)*1.3), int(max(img.size)))
    layer = Image.new('RGB', size, (255,255,255))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype("fonts/times.ttf", 140)

    text_x = int(size[0]/4)
    text_y = 200
    draw.text((text_x, text_y), message, (0,0,0), font=font)

    size_int = tuple((int((size[0] - img.size[0])/4), int(size[1] - img.size[1])))
    layer.paste(img, size_int)
    wert = layer.resize((int(size[0]/4), int(size[1]/4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(result_image_path)
    return result_image_path


def handle_poker_face(message):
    original_image_path = 'img/poker_face.jpg'
    result_image_path = 'img/result.jpg'

    img = Image.open(original_image_path)
    size = (int(img.size[0]*1.6), int(img.size[1] * 1.3))
    layer = Image.new('RGB', size, (255,255,255))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype("fonts/times.ttf", 140)

    text_x = int(size[0]/4)
    text_y = int(size[1]/7)
    draw.text((text_x, text_y), message, (0,0,0), font=font)

    size_int = tuple((int((size[0] - img.size[0])/2.5), int((size[1] - img.size[1]) * 1.2)))
    layer.paste(img, size_int)
    wert = layer.resize((int(size[0]/4), int(size[1]/4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(result_image_path)
    return result_image_path

def handle_poker_face_2(message):
    original_image_path = 'img/poker_face_2.jpg'
    result_image_path = 'img/result.jpg'

    img = Image.open(original_image_path)
    size = (int(img.size[0] * 2.6), int(img.size[1] * 1.3))
    layer = Image.new('RGB', size, (255,255,255))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype("fonts/times.ttf", 80)

    text_x = int(size[0]/4)
    text_y = int(size[1]/7)
    draw.text((text_x, text_y), message, (0,0,0), font=font)

    size_int = tuple((int((size[0] - img.size[0])/2.5), int((size[1] - img.size[1]) * 1.2)))
    layer.paste(img, size_int)
    wert = layer.resize((int(size[0]/4), int(size[1]/4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(result_image_path)
    return result_image_path


def handle_poker_face_3(message):
    original_image_path = 'img/poker_face_3.png'
    result_image_path = 'img/result.jpg'

    img = Image.open(original_image_path)
    size = (int(img.size[0] * 2.6), int(img.size[1] * 1.5))
    layer = Image.new('RGB', size, (255,255,255))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype("fonts/times.ttf", 80)

    text_x = int(size[0]/4)
    text_y = int(size[1]/7)
    draw.text((text_x, text_y), message, (0,0,0), font=font)

    size_int = tuple((int((size[0] - img.size[0])/2.5), int((size[1] - img.size[1]) * 1.2)))
    layer.paste(img, size_int)
    wert = layer.resize((int(size[0]/4), int(size[1]/4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(result_image_path)
    return result_image_path


def handle_me_only(message):
    original_image_path = 'img/me_only.jpg'
    result_image_path = 'img/result.jpg'

    img = Image.open(original_image_path)
    size = (int(img.size[0] * 5), int(img.size[1] * 1.5))
    layer = Image.new('RGB', size, (255,255,255))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype("fonts/times.ttf", 80)

    text_x = int(size[0]/4)
    text_y = int(size[1]/7)
    draw.text((text_x, text_y), message, (0,0,0), font=font)

    size_int = tuple((int((size[0] - img.size[0])/2.5), int((size[1] - img.size[1]) * 1.2)))
    layer.paste(img, size_int)
    wert = layer.resize((int(size[0]/4), int(size[1]/4)), Image.ANTIALIAS)
    wert.resize((100, 100), Image.ANTIALIAS)
    wert.save(result_image_path)
    return result_image_path


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
    if message.startswith("1"):
        image_path = handle_ok(event.text.split(' ', 1)[1])
    elif message.startswith("2"):
        image_path = handle_poker_face(event.text.split(' ', 1)[1])
    elif message.startswith("3"):
        image_path = handle_poker_face_2(event.text.split(' ', 1)[1])
    elif message.startswith("4"):
        image_path = handle_poker_face_3(event.text.split(' ', 1)[1])
    elif message.startswith("5"):
        image_path = handle_me_only(event.text.split(' ', 1)[1])
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
