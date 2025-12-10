from pathlib import Path
from re import ASCII
import sys
from PIL import Image
import numpy as np
import math 

ASCII_CHAR = " .:-=+*%@"

def calculateSharpness(Gx, Gy , z , convoluted_array):
    to_send_arr = []
    for i in range(0,z):
        x_mul = Gx * convoluted_array[i]
        x_val = int(x_mul.sum())
        y_mul = Gy * convoluted_array[i]
        y_val = int(y_mul.sum())

        gradient = math.sqrt(x_val**2 + y_val ** 2)
        to_send_arr.append(int(gradient))
    return to_send_arr

def edge_detection(img):
    width , height = img.size
    img = list(img.getdata())
    normal_arr  = np.array(img) 
    normal_arr = normal_arr.reshape((height,width))
    z = (width-2)*(height-2) 
    convoluted_array = np.full((z,3,3), 0)
    index = 0
    for j in range(0, height-2):
        for k in range(0,width-2):
            convoluted_array[index, : , : ] = normal_arr[j:j+3, k:k+3]
            index += 1
    Gx = np.array([
        [-1, 0 ,1],
        [-2 , 0 , 2],
        [-1 , 0 , 1]
    ])
    Gy = np.transpose(Gx)

    gradient_list = calculateSharpness(Gx, Gy , z , convoluted_array)

    gradient_list = np.array(gradient_list)

    gradient_list = gradient_list.reshape((height-2 , width-2))
    
    for i in range(height-2):
        for j in range(width-2):
            if gradient_list[i , j] < 100:
                gradient_list[i,j] =0
    
    flattened_list = list(gradient_list.flatten())
    scale = (len(ASCII_CHAR) -1) / 1443
    char =[]
    for p in flattened_list:
        idx = int(int(p) * scale)
        char.append(ASCII_CHAR[idx])
    full_string = "".join(char)

    lines = [full_string[i:i+width] for i in range(0, len(full_string),width-2 )]

    return "\n".join(lines)

def scale_image(img , new_width):
    width , height = img.size
    aspect_ratio = height/width
    new_height = max(1, int(aspect_ratio * new_width  *0.55))
    return img.resize((new_width , new_height))
    
def to_grayscale(img):
    return img.convert('L')

def map_pixels_to_ascii(img):
    pixels = list(img.getdata())
    chars = []
    scale = (len(ASCII_CHAR)-1) / 255
    for p in pixels:
        idx = int(p * scale)
        chars.append(ASCII_CHAR[idx])
    return "".join(chars)
        
def convert_image_to_ascii(path , width):
    img = Image.open(path)
    img = scale_image(img, new_width=width)
    img = to_grayscale(img)
    edge_lines = edge_detection(img)
    ascii_str = map_pixels_to_ascii(img)

    w = img.size[0]
    lines = [ascii_str[i:i+w] for i in range(0, len(ascii_str), w)]
    return '\n'.join(lines) , edge_lines

def main():
    img_path = Path(sys.argv[1])
    if not (img_path.exists()):
        print('Image not found')
        sys.exit(1)

    width = int(sys.argv[2]) if len(sys.argv) >= 3 else 1080
    
    ascii_art , edge_lines = convert_image_to_ascii(img_path , width=width)
    

    print(ascii_art)
        
    print(edge_lines)


if __name__ == '__main__':
    main()

