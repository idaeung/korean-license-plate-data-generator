import os
import random as rnd
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageOps
import sys

import data_augmentation

def get_opt_dict(license_plate_type):
    opt = dict()

    if license_plate_type == 0:
        opt['text_color'] = 'black'
        opt['background'] = 'white'
        opt['text_len'] = 8
        opt['hangul_index'] = 2

    return opt

def text_generator(hangul, num, text_len, hangul_index):
    # Create license plate strings by picking random word in hangul and num list
    hangul_len = len(hangul)
    num_len = len(num)

    string = ""
    for i in range(text_len - 1):
        if i == hangul_index:
            string += hangul[rnd.randrange(hangul_len)]
            string += " "
        else:
            string += num[rnd.randrange(num_len)]
    return string

def image_generator(text, font, text_color, font_size, font_ratio, space_width, character_spacing):
    number_font = ImageFont.truetype(font=font, size=font_size)
    hangul_font = ImageFont.truetype(font=font, size=int(font_size * font_ratio))

    space_width = int(number_font.getsize(" ")[0] * space_width)
    char_widths = [number_font.getsize(c)[0] if c != " " else space_width for c in text]

    text_width = sum(char_widths) + character_spacing * (len(text) - 1)
    text_height = max([number_font.getsize(c)[1] for c in text])

    fill = ImageColor.getrgb(text_color)
    background = (0, 0, 0, 0) if fill[0] else (255, 255, 255, 0)

    # white image
    txt_img = Image.new("RGBA", (text_width, text_height), background)
    txt_img_draw = ImageDraw.Draw(txt_img)

    for i, c in enumerate(text):
        if c.isdigit() or ord(c) == ord(' '):
            txt_img_draw.text(
                (sum(char_widths[0:i]) + i * character_spacing, 0),
                c,
                fill=fill,
                font=number_font,
            )
        else:
            txt_img_draw.text(
                (sum(char_widths[0: i]) + i * character_spacing, int(text_height * (1 - font_ratio))),
                c,
                fill=fill,
                font=hangul_font,
            )

    return txt_img

def get_round_corner(radius, fill):
    corner = Image.new('RGB', (radius, radius), (255, 255, 255))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill, outline='black')
    return corner

def background_generator(size, radius, fill):
    rect = Image.new('RGBA', size, color=fill)
    border_rect = ImageOps.expand(rect, border=1, fill='black')
    width, height = border_rect.size

    corner = get_round_corner(radius, fill)

    border_rect.paste(corner, (0, 0))
    border_rect.paste(corner.rotate(90), (0, height - radius))
    border_rect.paste(corner.rotate(180), (width - radius, height - radius))
    border_rect.paste(corner.rotate(270), (width - radius, 0))

    return border_rect

def augmentation_generator(img, augmentation_type):
    # 1: skewing, 2: distortion, 3: blurring, 4: shadow, 5: all of them
    aug_img = None
    if augmentation_type == 1:
        aug_img = data_augmentation.skewing(img)
    elif augmentation_type == 2:
        aug_img = data_augmentation.distortion(img)
    elif augmentation_type == 3:
        aug_img = data_augmentation.blurring(img)
    elif augmentation_type == 4:
        aug_img = data_augmentation.add_shadow(img)
    elif augmentation_type == 5:
        aug_img = data_augmentation.add_shadow(img)
        aug_img = data_augmentation.skewing(aug_img)
        # aug_img = data_augmentation.distortion(img)
        aug_img = data_augmentation.blurring(aug_img)
    else:
        print('ERROR')

    return aug_img

def data_generator(
    index,
    hangul_list,
    num_list,
    font,
    out_dir,
    augmentation_type,
    size,
    ratio,
    license_plate_type,
    extension,
    space_width,
    character_spacing,
    radius,
    margins
):

    margin_top, margin_left, margin_bottom, margin_right = margins
    horizontal_margin = margin_left + margin_right
    vertical_margin = margin_top + margin_bottom

    opt = get_opt_dict(license_plate_type)

    # Creating synthetic license plate
    text = text_generator(hangul_list, num_list, opt['text_len'], opt['hangul_index'])
    print('text: ', text)
    print('font: ', font)

    # Create image of text
    original_img = image_generator(text, font, opt['text_color'], size, ratio, space_width, character_spacing)
    print('original_img size: ', original_img.size)

    original_width, original_height = original_img.size
    background_width = original_width + horizontal_margin
    background_height = original_height + vertical_margin

    # Generate background image
    background_img = background_generator((background_width, background_height), radius=radius, fill=opt['background'])
    background_img.paste(original_img, (margin_left, margin_top), original_img)
    print('background_img size: ', background_img.size)

    import cv2, imutils, numpy
    cv2.imshow('numpy', imutils.resize(numpy.array(background_img), height=200))
    cv2.imshow('gauss', imutils.resize(data_augmentation.noisy(background_img, 0), height=200))
    cv2.imshow('poisson', imutils.resize(data_augmentation.noisy(background_img, 2), height=200))
    cv2.imshow('speckle', imutils.resize(data_augmentation.noisy(background_img, 3), height=200))
    cv2.waitKey()
    # cv2.imshow('4', data_augmentation.noisy(background_img, 1))
    # for i in range(4):
    #     data_augmentation.noisy(background_img, i)
    sys.exit(1)

    final_img = background_img
    if augmentation_type:
        final_img = augmentation_generator(background_img, augmentation_type)
        # final_img.show()
    print('final_image size: ', final_img.size)

    # Generate name for resulting image
    image_name = "{}_{}.{}".format(text, str(index), extension)

    # Save the image
    final_img.convert("RGB").save(os.path.join(out_dir, image_name))


