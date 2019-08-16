from PIL import Image, ImageFont, ImageDraw
from image_tools import draw_watermark

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