import argparse
import cv2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_img', type=str, help="image input file")
    parser.add_argument('in_txt', type=str, help="input file with a message")
    parser.add_argument('bit_plain', type=int, nargs='?', default=0, help="bit plain")
    parser.add_argument('out_img', type=str, nargs='?', help="image output file with a encrypted message")
    args = parser.parse_args()
    return args.in_img, args.in_txt, args.bit_plain, args.out_img


def encode_msg(msg):
    numbers = [ord(c) for c in msg]
    encoded = str()
    for n in numbers:
        encoded += format(n, '#010b')[2:]
    # return encoded
    return encoded + '00000000'


def set_bit(src, y, x, band, pos, value):
    # print(value, end="")
    # print("({}, {}, {}:{}) = {}".format(y, x, band, pos, value))
    # old_value = format(src[y][x][band], '#010b')[2:]
    if value == '1':
        src[y][x][band] |= 1 << pos
    else:
        src[y][x][band] &= ~(1 << pos)
    # print('{}\n{}\n'.format(old_value, format(src[y][x][band], '#010b')[2:]))


def encode(src, msg, bit_plain=1):
    encoded = encode_msg(msg)
    word_sz = bit_plain + 1
    block_sz = (3 * word_sz)
    for i, b in enumerate(encoded):
        pos, offset = int(i / block_sz), i % block_sz
        y, x = int(pos / src.shape[1]), pos % src.shape[1]
        band, bit = int(offset / word_sz), offset % word_sz
        set_bit(src, y, x, band, bit, b)
        # print("{} value = {}, pos = {} ({}, {}), {}:{}".format(
        #     i, b, pos, y, x, 'r' if band == 0 else 'g' if band == 1 else 'b', bit))
    return src


def main():
    in_img, in_txt, bit_plan, out_img = parse_args()
    f = open(in_txt, 'r')
    cv2.imwrite(out_img, encode(cv2.imread(in_img), f.read(), bit_plan))
    f.close()


if __name__ == '__main__':
    main()
