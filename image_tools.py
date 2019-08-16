from PIL import Image, ImageFont, ImageDraw

FONT = 'fonts/arial.ttf'

def draw_watermark(image, watermark_text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, 50)
    draw.text((image.size[0] - font.getsize(watermark_text)[0], image.size[1] - font.getsize(watermark_text)[1]), watermark_text, (128,128,128), font=font)