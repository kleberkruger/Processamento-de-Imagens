import numpy as np
import cv2

# Funciona em escalas de cinza

# Retorna um range que define a forma como uma linha da matriz será percorrida
#   - Flag -> determina se a imagem está sendo percorrida em zigzag ou da esquerda para direita
#   - i    -> indíce da linha atual para determinar a direção em caso de zigzag (flag = True)
#   - comp -> qt de linhas da img (com padding 0 de largura 1)
def zigZagRange(flag, i, comp):
    if (flag == False):
        return [1, comp - 2, 1]
    else:
        if (i % 2 != 0):
            return [1, comp - 2, 1]
        else:
            return [comp - 2, 1, -1]


# Aplicação do potilhado por difusão de erro de Floyd-Steinberg
#   - caminho: caminho para a img
#   - zigzag: se True então percorrer a img em zigzag, caso contrário da esquerda para a direita
#   - name: nome para salvar a img resultante
def pontilhadoPorDifusaoDeErro(caminho, zigzag, name):
    aux = cv2.imread(caminho, 0)  # 0 determina que a img é lida em tons de cinza
    # cv2.imshow('barcelona', aux)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img = cv2.copyMakeBorder(aux, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)  # aplicação de padding zero com largura 1

    alt = np.size(img, 0)  # qt de linhas
    comp = np.size(img, 1)  # qt de colunas

    img2 = np.zeros((alt, comp), dtype=np.uint8)  # resultado

    for i in range(1, alt - 1):

        a, b, incr = zigZagRange(zigzag, i, comp)

        for j in range(a, b, incr):
            pixel = img[i][j]

            if pixel < 128:
                pixel = 0
            else:
                pixel = 255

            erro = img[i][j] - pixel

            # propagação do erro
            img[i][j + 1] = img[i][j + 1] + (7 / 16) * erro
            img[i + 1][j - 1] = img[i + 1][j - 1] + (3 / 16) * erro
            img[i + 1][j] = img[i + 1][j + 1] + (5 / 16) * erro
            img[i + 1][j + 1] = img[i + 1][j + 1] + (1 / 16) * erro

            img2[i][j] = pixel

    cv2.imwrite('imgRes/error_difusion_dithering/' + name + '.pbm', img2)
    cv2.imshow('barcelona', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


pontilhadoPorDifusaoDeErro('./../in/baboon.png', True, './../out/barcelona-zigzag')  # percorrendo em zig zag
pontilhadoPorDifusaoDeErro('./../in/baboon.png', False, './../out/barcelona-notzigzag')  # percorrendo da esquerda para a direita
