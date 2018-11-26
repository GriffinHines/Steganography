from PIL import Image
import binascii

#turn rgb color values into hex color values 
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

#turn hex color values into rgb color values
def hex2rgb(hexcode):
    # return tuple(map(ord, hexcode[1:].decode('hex')))
    return (int(hexcode[1:3], 16), int(hexcode[3:5], 16), int(hexcode[5:7], 16))

#converts message string to binary
def str2bin(message):
    binary = bin(int(binascii.hexlify(bytes(message, 'UTF-8')), 16))
    return binary[2:]

#converts binary message to string
def bin2str(binary):
    message = binascii.unhexlify('%x' % (int('0b'+binary, 2)))
    return message

#changes hexcode of a pixel for encoding purposes
def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None

#changes hexcode of a pixel for decoding purposes
def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None

#hide message in image file
def embed(filename, message):
    img = Image.open(filename)
    binary = str2bin(message) + '1111111111111110'

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        newData = []
        digit = 0

        for item in datas:
            if digit < len(binary):
                newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[digit])
                # print(newpix)
                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1
            else:
                newData.append(item) 

        img.putdata(newData)
        img.save(filename, "PNG")

        return newData # completed
    return False # incorrect image mode, couldn't hide

#read hidden message from image file
def extract(filename):
    img = Image.open(filename)
    binary = ""

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = decode(rgb2hex(item[0], item[1], item[2]))

            if digit == None:
                pass
            else:
                binary += digit
                if binary[-16:] == '1111111111111110':
                    return bin2str(binary[:-16]) # success
        return bin2str(binary)
    return False # incorrect image mode, couldn't retrieve

def Main():
    while(True):
        targetFile = input('Enter a target file')
        mode = input('Enter e for encode, d for decode')
        if(mode == 'e'):
            text = input('Enter a message to hide')
            embed(targetFile, text)
        elif(mode == 'd'):
            print(extract(targetFile))
    
if __name__ == '__main__':
    Main()