from enum import auto
from pathlib import Path
import sys
from PIL import Image
from colorama import init , Fore , Style

red= " .:-=+*#%@"
green= " .:-=+*#%@"
blue = " .:-=+*#%@"

init(autoreset=True)

def scale_image(img , new_width):
    width , height = img.size
    aspect_ratio = height/width
    new_height = max(1, int(aspect_ratio * new_width  * 0.8))
    return img.resize((new_width , new_height))
    
def map_pixels(img):
    pixels = list(img.getdata())
    chars = []
    for p in pixels:
        red_val , green_val , blue_val , transparency= 0,0,0,0
        try:
            red_val, green_val , blue_val ,transparency = p
            red_val = int((red_val/ 255) * (len(red)-1) )
            chars.append(red[red_val])
            green_val = int((green_val/ 255) * (len(green)-1) )
            chars.append(green[green_val])
            blue_val = int((blue_val/ 255) * (len(blue)-1) )
            chars.append(blue[blue_val])
        except Exception as ex:
            print(ex)
            print(red_val , green_val , blue_val)
            sys.exit(1)
    return "".join(chars)
        
def convert_image_to_simpler(path , width):
    img = Image.open(path)
    img = scale_image(img, new_width=width)
    img_str = map_pixels(img)

    w = img.size[0]
    lines = [img_str[i:i+(w*3)] for i in range(0, len(img_str), w*3)]
    return '\n\t\t\t\t\t\t\t'.join(lines)

def main():
    images =['1.png' , '2.png' ,'3.png' , '4.png','5.png']
    
    for idx , image in enumerate(images):
        img_path = Path(image)
        if not (img_path.exists()):
            print('Image not found')
            sys.exit(1)

        width = int(sys.argv[2]) if len(sys.argv) >= 3 else 200
        output_file = sys.argv[3] if len(sys.argv) >=4 else None
        
        simpler_art = convert_image_to_simpler(img_path , width=width)
        print('\n') 
        for value , char in enumerate(simpler_art):
            if value%3 ==0:
                print(f"{Fore.RED}{char}",end='')
            elif value%3 ==1:
                print(f"{Fore.GREEN}{char}",end='')
            elif value%3 ==2:
                print(f"{Fore.BLUE}{char}",end='')


if __name__ == '__main__':
    main()

