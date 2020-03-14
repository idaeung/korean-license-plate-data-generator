import random as rnd
from PIL import Image
import cv2
import numpy as np
import imutils

def skewing(img):
    random_angle = rnd.randint(-45, 45)
    skewed_img = img.rotate(random_angle, expand=1)

    w, h = skewed_img.size
    background = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    background.paste(skewed_img, (0, 0, w, h), skewed_img)
    return background

def distortion(img):
    pass

def blurring(img):
    img = np.array(img.convert('RGB'))

    if rnd.randrange(0, 2):
        kernel = (5, 5) if rnd.randrange(0, 2) else (7, 7)
        print('blur kernel: ', kernel)
        blur = cv2.blur(img, ksize=kernel)
    else:
        kernel_list = [(3, 3), (5, 5), (7, 7), (9, 9), (11, 11)]
        kernel = kernel_list[rnd.randrange(0, len(kernel_list))]
        print('gaussian kernel: ', kernel)
        blur = cv2.GaussianBlur(img, kernel, 0)

    return Image.fromarray(blur).convert("RGBA")

def brightness(img):
    img = np.array(img.convert('RGB'))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = np.array(img, dtype=np.float64)
    random_bright = np.random.uniform(0, 1)
    print('random_bright: ', random_bright)
    img[:, :, 2] = img[:, :, 2] * (1-random_bright)
    img[:, :, 2][img[:, :, 2] > 255] = 255
    img[:, :, 2][img[:, :, 2] < 0] = 0
    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

    return Image.fromarray(img).convert("RGBA")

def add_brightness(img):
    img = np.array(img.convert('RGB'))
    image_HLS = cv2.cvtColor(img,cv2.COLOR_RGB2HLS)
    # Conversion to HLS
    image_HLS = np.array(image_HLS, dtype = np.float64)
    random_brightness_coefficient = np.random.uniform()+0.5
    ## generates value between 0.5 and 1.5
    image_HLS[:,:,1] = image_HLS[:,:,1]*random_brightness_coefficient
    ## scale pixel values up or down for channel 1(Lightness)
    image_HLS[:,:,1][image_HLS[:,:,1]>255]  = 255
    ##Sets all values above 255 to 255
    image_HLS = np.array(image_HLS, dtype = np.uint8)
    image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB)
    ## Conversion to RGB
    return Image.fromarray(image_RGB).convert("RGBA")

def generate_shadow_coordinates(imshape, no_of_shadows=1):
    vertices_list=[]
    for index in range(no_of_shadows):
        vertex=[]
        for dimensions in range(np.random.randint(3,15)):
            # Dimensionality of the shadow polygon
            vertex.append(( imshape[1]*np.random.uniform(),imshape[0]//3+imshape[0]*np.random.uniform()))
            vertices = np.array([vertex], dtype=np.int32)
            # single shadow vertices
        vertices_list.append(vertices)
    return vertices_list
    ## List of shadow vertices

def add_shadow(img, no_of_shadows=1):
    img = np.array(img.convert('RGB'))
    image_HLS = cv2.cvtColor(img,cv2.COLOR_RGB2HLS)
    # Conversion to HLS
    mask = np.zeros_like(img)
    imshape = img.shape
    vertices_list= generate_shadow_coordinates(imshape, no_of_shadows)
    # 3 getting list of shadow vertices
    for vertices in vertices_list:
        cv2.fillPoly(mask, vertices, 255)
    # adding all shadow polygons on empty mask, single 255 denotes only red channel
    image_HLS[:,:,1][mask[:,:,0]==255] = image_HLS[:,:,1][mask[:,:,0]==255]*0.5
    # if red channel is hot, image's "Lightness" channel's brightness is lowered
    image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB)
    # Conversion to RGB
    return Image.fromarray(image_RGB).convert("RGBA")

def noisy(img, noise_type):
    img = np.array(img.convert('RGB'))
    w, h, ch = img.shape

    if noise_type == 0:
        mean = 0
        var = 0.1
        sigma = var**0.5

        gauss = np.random.normal(mean, sigma, (w, h, ch))
        gauss = gauss.reshape(w, h, ch)
        noisy = img + gauss

    elif noise_type == 1:
        s_vs_p = 0.5
        amount = 0.004
        noisy = np.copy(img)

        num_salt = np.ceil(amount * img.size * s_vs_p)
        coords = [np.random.randint(0, i-1, int(num_salt)) for i in img.shape]
        print('coords: ', coords)
        noisy[coords] = 1

        num_pepper = np.ceil(amount * img.size * (1.-s_vs_p))
        coords = [np.random.randint(0, i-1, int(num_pepper)) for i in img.shape]
        noisy[coords] = 0

    elif noise_type == 2:
        vals = len(np.unique(img))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(img * vals) / float(vals)

    elif noise_type == 3:
        gauss = np.random.randn(w, h, ch)
        gauss = gauss.reshape(w, h, ch)
        noisy = img + img * gauss

    # return Image.fromarray(noisy).convert("RGBA")
    return noisy


