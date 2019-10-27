import argparse
import cv2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_img', type=str, help="image output file")
    parser.add_argument('bit_plain', type=int, nargs='?', default=0, help="bit plain")
    parser.add_argument('out_txt', type=str, nargs='?', help="output file with the decrypted message")
    args = parser.parse_args()
    return args.out_img, args.bit_plain, args.out_txt


def decode_msg(bin_msg):
    msg = str()
    for i in range(0, len(bin_msg), 8):
        msg += str(chr(int(bin_msg[i:i + 8], base=2)))
    return msg


def extract_bin_msg(img, bit_plain):
    msg = str()
    start = 7 - bit_plain + 2
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            msg += format(img[y][x][0], '#010b')[start:][::-1]
            msg += format(img[y][x][1], '#010b')[start:][::-1]
            msg += format(img[y][x][2], '#010b')[start:][::-1]

            # TODO: Esta parte pode ser melhorada.
            tokens = [(msg[i:i + 8]) for i in range(0, len(msg), 8)]
            if tokens.count('00000000') > 0:
                stop = tokens.index('00000000')
                msg = msg[0:stop * 8]
                return msg
    return None


def decode(img, bit_plain=0):
    return decode_msg(extract_bin_msg(img, bit_plain))


def main():
    out_img, bit_plan, out_txt = parse_args()
    f = open(out_txt, 'w')
    f.write(decode(cv2.imread(out_img), bit_plan))
    f.close()


if __name__ == '__main__':
    main()
