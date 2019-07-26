import vk_api
import key
import random
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import json
from PIL import Image, ImageFont, ImageDraw


def handle_ok_sign(message):
    image_path = 'img/result.jpg'

    img = Image.open('img/ok.jpg')
    size = (int(max(img.size)*1.3), int(max(img.size)))
    print(type(size[0]))
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
    wert.save(image_path)
    return image_path


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
    return {'text': message}

print("Server started")
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print('New message:')
            print(f'For me by: {event.user_id}')

            # Create a text answer
            answer = handle_msg(event.text)

            # Create an answer and an image
            image_path = handle_ok_sign(event.text)

            # Send a message back
            write_msg(event.user_id, answer, image_path)

            print('Text: ', event.text)
