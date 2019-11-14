from io import BytesIO
from pprint import pprint
from collections import Counter

import requests
from PIL import Image


symbols = [' ', '░','▒', '▓', '█']


def img_to_ascii(url, max_width=100):
    """
    url: str
        the url to an image

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
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size

    aspect_ratio = max_width/width

    # resizing image based on compression factor. -2 because of new line characters
    img = img.resize((int(width*aspect_ratio-2), int(((height*aspect_ratio)-2)*.55)))
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
        row_values = [int((value/255)*len(symbols)-1) for value in row]
        ascii_img.append([symbols[v] for v in row_values])
        
    return ascii_img



if __name__ == "__main__":

    url = "https://www.python.org/static/opengraph-icon-200x200.png"

    ascii_img = img_to_ascii(url, max_width=100)
    
    # outputting the result into a file called output.txt
    with open('output.txt', "w", encoding='utf-8') as f:
        # joining all the symbols together to be printed to a file
        for row in ascii_img:
            line = ''.join(row)
            print(line, file=f)
