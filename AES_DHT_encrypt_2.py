from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import RPi.GPIO as gpio
import dht11



def generate_encryption_key(password, salt):
    #actaual encryption key generation
    key = PBKDF2(password, static_salt, dkLen=32)
    #print(key)
    return key

#sensor setting
gpio.setmode(gpio.BOARD)
gpio.setup(40,gpio.OUT)
dht=dht11.DHT11(pin=40)

def read_data():
    #message to be encrypted
    #message = b"Hello!!!"
    result = dht.read()
    #Temp = result.temperature
    #Hum = result.humidity
    #print(str(temp))
    if result.is_valid():
        return str(result.temperature)+"C, " + str(result.humidity)+"%"
    else:
        return "Invalid Data"
    
def encrypt_and_save_data(data, key, output_filename):
    iv = get_random_bytes(16)
    # using the key to cipher message
    cipher = AES.new(key,AES.MODE_CBC)
    ciphered_data= cipher.encrypt(pad(data.encode(), AES.block_size))
    #print(ciphered_data)
    #export it in a binary file
    with open(output_filename,'wb') as f:
        f.write(iv)
        f.write(ciphered_data)
        
if __name__=="__main__":
    # Generate key for encyption and decryption
    #basic key
    #simple_key = get_random_bytes(32)
    #print(simple_key)
    static_salt = b"r@y2M\xfc\xf6\xe6\n\x82\xb9\xce0Y)\x17Nd\xe3_\xc2\xfd^\n&sRdx'\xb8\xfc"
    password = "brdbrn@93"
    
    key = generate_encryption_key(password, static_salt)
    sensor_data = read_data()
    
    if sensor_data != "Invalid Data":
        encrypt_and_save_data(sensor_data, key, 'encrypt.bin')
        print("data encrypted and save")
    else:
        print("Error: Invalid Data")





