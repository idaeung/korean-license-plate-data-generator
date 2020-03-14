from PIL import Image, ImageFont, ImageDraw

text = '58로 6324'
font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 50)
width, height = font.getsize(text)

image2 = Image.new('RGBA', (width, height), (0, 0, 128, 0))
draw2 = ImageDraw.Draw(image2)
draw2.text((0, 0), text=text, font=font, fill=(0, 255, 128))
image2 = image2.rotate(30, expand=1)
print('image2.size: ', image2.size)

w, h = image2.size
image1 = Image.new('RGBA', (w, h), (0, 128, 0, 0))
image1.show()
image2.show()

px, py = 0, 0
sx, sy = image2.size
image1.paste(image2, (px, py, px + sx, py + sy), image2)
image1.show()

