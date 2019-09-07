import cv2
import numpy as np

img = cv2.imread('./../in/baboon.png', 0)


def mostrar_img(nome, imagem):
    cv2.imshow(nome, imagem)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()


def imagem_negativa():
    # neg_img = (255 - img)
    neg_img = cv2.bitwise_not(img, 0)
    mostrar_img('neg_img', neg_img)


def cem_tons_de_cinza():
    normalized_img = cv2.normalize(img, None, 100, 200, cv2.NORM_MINMAX)
    mostrar_img('normalized_image', normalized_img)


def imprimir_img(image):
    for y in range(0, len(image)):
        for x in range(0, len(image[0])):
            if image[y][x] < 0 or image[y][x] > 255:
                print("valor errado: " + image[x][y])
                break
            else:
                print(image[x][y])


def ajustar_brilho(image, valor):
    image = image / 255
    img_b = image ** (1 / valor)
    image = img_b * 255

    # imprimir_img(image)
    mostrar_img('ajuste_de_brilho', img_b)


def ajustes_de_brilho():
    ajustar_brilho(img, 1.5)
    ajustar_brilho(img, 2.5)
    ajustar_brilho(img, 3.5)


def criar_mosaico():
    p01 = img[0:128, 0:128]
    p02 = img[0:128, 128:256]
    p03 = img[0:128, 256:384]
    p04 = img[0:128, 384:512]
    p05 = img[128:256, 0:128]
    p06 = img[128:256, 128:256]
    p07 = img[128:256, 256:384]
    p08 = img[128:256, 384:512]
    p09 = img[256:384, 0:128]
    p10 = img[256:384, 128:256]
    p11 = img[256:384, 256:384]
    p12 = img[256:384, 384:512]
    p13 = img[384:512, 0:128]
    p14 = img[384:512, 128:256]
    p15 = img[384:512, 256:384]
    p16 = img[384:512, 384:512]

    mosaico = img

    img[0:128, 0:128] = p06
    img[0:128, 128:256] = p11
    img[0:128, 256:384] = p13
    img[0:128, 384:512] = p03
    img[128:256, 0:128] = p08
    img[128:256, 128:256] = p16
    img[128:256, 256:384] = p01
    img[128:256, 384:512] = p09
    img[256:384, 0:128] = p12
    img[256:384, 128:256] = p14
    img[256:384, 256:384] = p02
    img[256:384, 384:512] = p07
    img[384:512, 0:128] = p04
    img[384:512, 128:256] = p15
    img[384:512, 256:384] = p10
    img[384:512, 384:512] = p05

    mostrar_img('mosaico', mosaico)


def multiplicar(matriz, valor):
    for i in range(0, len(matriz)):
        for j in range(0, len(matriz[0])):
            matriz[i][j] = round(matriz[i][j] * valor)
    return matriz


def combinar_imagens(val1, val2):
    img1 = cv2.imread('./../in/baboon.png', 0)
    img2 = cv2.imread('./../in/butterfly.png', 0)

    # combinada = multiplicar(img1, val1) + multiplicar(img2, val2)
    combinada = cv2.addWeighted(img1, val1, img2, val2, 0)

    mostrar_img('imagem_combinada', combinada)


combinar_imagens(0.2, 0.8)
combinar_imagens(0.5, 0.5)
combinar_imagens(0.8, 0.2)

# # Iterate over each pixel and change pixel value to binary using np.binary_repr() and store it in a list.
# lst = []
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         lst.append(np.binary_repr(img[i][j], width=8))  # width = no. of bits
#
# # We have a list of strings where each string represents binary pixel value. To extract bit planes we need to iterate
# # over the strings and store the characters corresponding to bit planes into lists.
# # Multiply with 2^(n-1) and reshape to reconstruct the bit image.
# eight_bit_img = (np.array([int(i[0]) for i in lst], dtype=np.uint8) * 128).reshape(img.shape[0], img.shape[1])
# seven_bit_img = (np.array([int(i[1]) for i in lst], dtype=np.uint8) * 64).reshape(img.shape[0], img.shape[1])
# six_bit_img = (np.array([int(i[2]) for i in lst], dtype=np.uint8) * 32).reshape(img.shape[0], img.shape[1])
# five_bit_img = (np.array([int(i[3]) for i in lst], dtype=np.uint8) * 16).reshape(img.shape[0], img.shape[1])
# four_bit_img = (np.array([int(i[4]) for i in lst], dtype=np.uint8) * 8).reshape(img.shape[0], img.shape[1])
# three_bit_img = (np.array([int(i[5]) for i in lst], dtype=np.uint8) * 4).reshape(img.shape[0], img.shape[1])
# two_bit_img = (np.array([int(i[6]) for i in lst], dtype=np.uint8) * 2).reshape(img.shape[0], img.shape[1])
# one_bit_img = (np.array([int(i[7]) for i in lst], dtype=np.uint8) * 1).reshape(img.shape[0], img.shape[1])
#
# # Concatenate these images for ease of display using cv2.hconcat()
# finalr = cv2.hconcat([eight_bit_img, seven_bit_img, six_bit_img, five_bit_img])
# # finalv = cv2.hconcat([four_bit_img, three_bit_img, two_bit_img, one_bit_img])
#
# # Vertically concatenate
# # final = cv2.vconcat([finalr, finalv])
# final = cv2.vconcat([finalr])
#
# # Display the images
# cv2.imshow('a', final)
# cv2.waitKey(0)

quit()
