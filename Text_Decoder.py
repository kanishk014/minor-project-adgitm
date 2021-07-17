
# importing the required packages
import cv2
import numpy as np
import argparse


# Function to convert the the content into it's relevant binary form
def to_binary(msg):
    msg_type = type(msg)
    if msg_type == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif msg_type == bytes or msg_type == np.ndarray:
        return [format(i, "08b") for i in msg]
    elif msg_type == int or msg_type == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Input Type is not supported")


# Getting the hidden data from the image
def getData(img):
    b_data = ''
    for values in img:
        for pixel in values:

            # convert RGB values to binary format
            r, g, b = to_binary(pixel)
            # extracting the data from the LSB of red pixel
            b_data += r[-1]
            # extracting the data from the LSB of green pixel
            b_data += g[-1]
            # extracting the data from the LSB of blue pixel
            b_data += b[-1]

    # split by 8-bits
    bytes_data = [b_data[i:i + 8] for i in range(0, len(b_data), 8)]
    # convert the bits into characters
    decoded_data = ""
    for byte in bytes_data:
        decoded_data += chr(int(byte, 2))
        # check if we have reached the delimiter string
        if decoded_data[-3:] == '###':
            break
    # remove the delimiter string from the final decoded message
    return decoded_data[:-3]


# Decode the data from the image
def decode(filename):
    img = cv2.imread(filename)
    text = getData(img)
    # Print the decoded text into a text file in the same directory as the code file
    file = open('Extracted_msg.txt', 'w')
    file.write(text)
    file.close()


if __name__ == '__main__':

    # Building a command line argument
    parser = argparse.ArgumentParser(
        description='Decode text inside an image generated with encoded data by the Encoder.')

    # Collecting the filename of the image which is to be decoded
    parser.add_argument('image', type=str,
                        help='Enter the filename of the image which contains the encoded text.')

    args = parser.parse_args()
    filename = args.image
    
    decode(filename)
