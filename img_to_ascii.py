import os
from collections import Counter
from io import BytesIO
from pprint import pprint

import requests
from PIL import Image

# symbols = [' ', '░','▒', '▓', '█']
symbols = [ ' ', '.', ':', '-', '=', '+', '*', '#', '%', '@' ]
# symbols.reverse()


def img_to_ascii(location, max_width=100):
    """
    location: str
        filepath or url to image

    max_width: int
        an int that decides how many characters are allowed 
        in the width and shrinks the image accordingly

    returns a list of rows of characters like this:

    [
        [' ', '░','▒', '▓', '█'],
        [' ', '░','▒', '▓', '█'],
        [' ', '░','▒', '▓', '█'],
    ]
    """

    # reading image
    # if the location exists on the system, use it. else, try to find it online.
    if os.path.exists(location):
        img = Image.open(location)
    else:
        response = requests.get(location)
        img = Image.open(BytesIO(response.content))

    width, height = img.size

    aspect_ratio = max_width/width

    # resizing image based on compression factor. -2 because of new line characters
    img = img.resize((int(width*aspect_ratio-2), int(((height*aspect_ratio)-2)*.45)))
    width, height = img.size

    # converting to black and white
    img_bw = img.convert('L')
    # img_bw.show()

    # sorting the image into rows of pixels
    pixels = list(img_bw.getdata())
    rows = [pixels[h*width:(h+1)*width] for h in range(height)]

    ascii_img = []

    for row in rows:
        # getting the symbol for the light value from symbols dict
        row_values = [int((value/255)*(len(symbols)-1)) for value in row]
        ascii_img.append([symbols[v] for v in row_values])
        
    return ascii_img



if __name__ == "__main__":

    import argparse
    from time import sleep

    parser = argparse.ArgumentParser()
    parser.add_argument('location', help="filepath or url to an image")
    parser.add_argument('-w', '--width', help="How many characters wide the output will be. (including new line characters)")

    args = parser.parse_args()

    if args.width:
        max_width = int(args.width)
    else:
        max_width = 100

    ascii_img = img_to_ascii(args.location, max_width=max_width)
    
    # joining all the symbols together to be printed
    for row in ascii_img:
        line = ''.join(row)
        # print(line, file=f)
        print(line)
        sleep(0.01)
