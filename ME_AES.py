import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

s_box = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
]
# AES Inverse S-box (Substitution box)
inverse_s_box = [
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
]

mix_columns_matrix =[   ['02', '03', '01', '01'],
                        ['01', '02', '03', '01'],
                        ['01', '01', '02', '03'],
                        ['03', '01', '01', '02'] ]
                        

inverse_mix_columns_matrix = [  ['0e', '0b', '0d', '09'],
                                ['09', '0e', '0b', '0d'],
                                ['0d', '09', '0e', '0b'],
                                ['0b', '0d', '09', '0e'] ]
        
rc =[   [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 1, 1],
        [0, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0]  ]

def binary_list_to_string(binary_list):
    # Convert binary list to a binary string
    binary_string = ''.join(map(str, binary_list))

    # Convert binary string to a string of characters
    char_string = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))

    return char_string

def string_to_binary_list(input_string):
    binary_list = []

    # Convert each character in the string to its binary representation
    for char in input_string:
        binary_representation = bin(ord(char))[2:]
        
        # Ensure each binary representation has 8 bits by padding with zeros if necessary
        padded_representation = '0' * (8 - len(binary_representation)) + binary_representation
        
        # Convert each bit to an integer and extend the list
        binary_list.extend([int(bit) for bit in padded_representation])

    return binary_list

def hex_to_binary_list(hex_number):
    # Convert hexadecimal to binary string
    binary_string = bin(int(hex_number, 16))[2:]

    # Convert binary string to a list of integers
    binary_list = [int(bit) for bit in binary_string]

    return binary_list

def hex_to_binary_list_from_sBox(hex_number):
    hex_number = str(hex_number)
    # Convert hexadecimal to integer
    decimal_number = int(hex_number, 16)

    # Convert integer to binary string and remove the '0b' prefix
    binary_string = bin(decimal_number)[2:]

    # Ensure the binary string is 8 bits long by padding with zeros if needed
    padded_binary_string = binary_string.zfill(8)

    # Convert the binary string to a list of integers
    binary_list = [int(bit) for bit in padded_binary_string]

    return binary_list

# take binary int list of size 8 (return one hexa num)
def binary_list_to_hex(binary_list):
    # Convert the binary list to a binary string
    binary_string = ''.join(map(str, binary_list))

    # Pad the binary string with zeros to ensure it's a multiple of 4
    padded_binary_string = '0' * (4 - len(binary_string) % 4) + binary_string

    # Convert the binary string to a hexadecimal string
    hex_string = hex(int(padded_binary_string, 2))[2:]

    return hex_string.upper()

def binary_list_to_hex_matrix(binary_list):
    # Ensure the binary list has a length that is a multiple of 32 (4 words of 8 bits each)
    binary_list = binary_list[:len(binary_list) - len(binary_list) % 32]

    # Convert binary list to a binary string
    binary_string = ''.join(map(str, binary_list))

    # Split the binary string into groups of 32 bits (4 words of 8 bits each)
    binary_chunks = [binary_string[i:i+32] for i in range(0, len(binary_string), 32)]

    # Convert each 32-bit binary chunk to hexadecimal and create a 2D matrix
    #hex_matrix = [['0x' + hex(int(chunk[i:i+8], 2))[2:].upper() for i in range(0, 32, 8)] for chunk in binary_chunks]
    hex_matrix = [[ hex(int(chunk[i:i+8], 2))[2:].upper() for i in range(0, 32, 8)] for chunk in binary_chunks]

    return hex_matrix

def make_xor_32bit(l1,l2):
    new_list = []
    for i in range(32):
        new_list.append((l1[i] ^ l2[i]))
    return new_list

def list_to_matrix(input_list, rows, cols):
    if rows * cols != len(input_list):
        raise ValueError("Number of rows and columns do not match the length of the input list.")
    
    matrix = [input_list[i:i+cols] for i in range(0, len(input_list), cols)]
    return matrix

def key_addition(data, key):
    # 128 bits
    for i in range(128):
        data[i] = data[i] ^ key[i]
    return data

def row_col(binary_list):
    print(" in row col ")
    print(binary_list)
    print(type(binary_list))
    print(len(binary_list))


    # Divide the list into two parts (4 digits each)
    first_part = binary_list[:4]
    second_part = binary_list[4:]

    # Convert each part to binary string and then to decimal
    first_decimal = int(''.join(map(str, first_part)), 2)
    second_decimal = int(''.join(map(str, second_part)), 2)

    return first_decimal, second_decimal

def matrix_multiply(matrix_a, matrix_b):
    
    final_list = []

    # convert hexa representation to it's number
    for i in range(4): 
        for j in range(4):
            matrix_a[i][j] = int(str(matrix_a[i][j]),16) 
            matrix_b[i][j] = int(str(matrix_b[i][j]),16) 

    # convert 2d list to matrix
    matrix_a = np.array(matrix_a)
    matrix_b = np.array(matrix_b)

    # multiply matrices
    result_matrix = np.dot(matrix_a, matrix_b)
    # result matrix now is decimal and have result of  multiplication

    # Convert each hex item to binary and remove the '0b' prefix
    # and put numbers in list col by col so j is the first index
    for i in range(4):
        for j in range(4):
            num = result_matrix[j][i]
            binary_string = bin(num)[2:].zfill(8)
            binary_list = [int(bit) for bit in binary_string]
            final_list.extend(binary_list)

    return final_list # 128  int binary digit
# the error bec binary list is empty
def g(binary_list, round):

    # shift left
    binary_list = binary_list[8:32]+binary_list[0:8]

    new_list = []
    for i in range(4):
        # get row and col of 8 bits and return new value hexa and store it as binary list again
        row, col = row_col(binary_list[i*8:(i*8)+8])
        new_list.extend(hex_to_binary_list_from_sBox(s_box[row][col]))

    # make RC[i] for first 8 bits
    for i in range(8):
        new_list[i] = new_list[i] ^ rc[round][i]

    return new_list

# take 2 binary int lists and make xors
def key_schedule(key):
    # convert hexa to binary list of integers  len = 128 
    #key = hex_to_binary_list(key) 
    
    keys = [] 
    for i in range(11):
        new_key = []
        w0 = key[0:32]
        w1 = key[32:64]
        w2 = key[64:96]
        w3 = g(key[96:], i)

        w0_next= make_xor_32bit(w0,w3)
        new_key.extend(w0_next)

        w1_next = make_xor_32bit(w0_next,w1)
        new_key.extend(w1_next)

        w2_next = make_xor_32bit(w1_next,w2)
        new_key.extend(w2_next)

        w3_next = make_xor_32bit(w2_next,w3)
        new_key.extend(w3_next)
        key = new_key
        keys.append(new_key)

    return keys

# data is list of binary
def byte_substitution(data):
    new_data = []
    i = 0
    while i < (len(data)):
        row, col = row_col(data[i:i+8])
        new_data.extend(hex_to_binary_list_from_sBox(s_box[row][col]))
        i += 8
    return new_data

def inverse_byte_substitution(data):
    new_data = []
    i = 0
    while i < (len(data)):
        row, col = row_col(data[i:i+8])
        new_data.extend(hex_to_binary_list_from_sBox(inverse_s_box[row][col]))
        i += 8
    return new_data

# take list of 128 binary int
def shift_row(data):
    # put the 128 bit as rows 
    row1 = data[0:8  ]+data[32:40]+data[64:72]+data[96:104 ]
    row2 = data[8:16 ]+data[40:48]+data[72:80]+data[104:112]
    row3 = data[16:24]+data[48:56]+data[80:88]+data[112:120]
    row4 = data[24:32]+data[56:64]+data[88:96]+data[120:128]

    # shift ledt each row 
    # row1 no shift
    row2 = row2[8:32] + row2[0:8] 
    row3 = row3[16:] + row3[0:16] 
    row4 = row4[24:] + row4[0:24] 

    # take data column by column to return it as we taks
    col1 = row1[0:8]+row2[0:8]+row3[0:8]+row4[0:8]
    col2 = row1[8:16]+row2[8:16]+row3[8:16]+row4[8:16]
    col3 = row1[16:24]+row3[16:24]+row3[16:24]+row4[16:24]
    col4 = row1[24:32]+row2[24:32]+row3[24:32]+row4[24:32]
    
    new_data = col1+col2+col3+col4
    return new_data

def inverse_shift_row(data):
    # put the 128 bit as rows 
    row1 = data[0:8  ]+data[32:40]+data[64:72]+data[96:104 ]
    row2 = data[8:16 ]+data[40:48]+data[72:80]+data[104:112]
    row3 = data[16:24]+data[48:56]+data[80:88]+data[112:120]
    row4 = data[24:32]+data[56:64]+data[88:96]+data[120:128]

    # shift ledt each row 
    # row1 no shift
    row2 = row2[96:] + row2[0:96] # right shift 1 = shift left 3
    row3 = row3[64:] + row3[0:64] 
    row4 = row4[32:] + row4[0:32] # # right shift 3 = shift left 1

    # take data column by column 
    col1 = row1[0:8]+row2[0:8]+row3[0:8]+row4[0:8]
    col2 = row1[8:16]+row2[8:16]+row3[8:16]+row4[8:16]
    col3 = row1[16:24]+row3[16:24]+row3[16:24]+row4[16:24]
    col4 = row1[24:32]+row2[24:32]+row3[24:32]+row4[24:32]

    new_data = col1+col2+col3+col4 
    return new_data

# take 128 int binary list then make it 4 cols and multiply each col by column_matrix
def mix_col(data):

    # convert 128 bit to 16 hexa values
    data_in_hexa = []
    for i in range(0, 128, 8):
        hex_value = hex(int("".join(map(str, data[i:i+8])), 2)) 
        # hex_value format is '0xA5' in string so we ignore 0x in next line 
        data_in_hexa.append(hex_value[2:])

    # convert hexa array to 2d matrix
    data_in_hexa = list_to_matrix(data_in_hexa,4,4) # each number is like 'A4'

    result =  matrix_multiply(data_in_hexa,mix_columns_matrix)
    return result

def inverse_mix_col(data):

    # convert 128 bit to 16 hexa values
    data_in_hexa = []
    for i in range(0, 128, 8):
        hex_value = hex(int("".join(map(str, data[i:i+8])), 2))
        data_in_hexa.append(hex_value)
    # convert hexa array to 2d matrix
    data_in_hexa = list_to_matrix(data_in_hexa,4,4) # each number is like 'A4'

    result =  matrix_multiply(data_in_hexa,inverse_mix_columns_matrix)
    return result

def encrypt(original_plain_text,key):
    all_cipher = []

    key = key.upper()
    # convert ti in tbunary list
    key = hex_to_binary_list(key)

    # 11 keys  // list of lists
    keys = key_schedule(key) 
    # note key converting is handled in key_schedule function
    # take 16 char by 16 char
    for i in range(0, len(original_plain_text)//16, 16):
        plain_text = original_plain_text[i:i+16]
        # convert  P to binary int list of 128
        plain_text = string_to_binary_list(plain_text)

        print(" in encryption ")
        print(key)
        print(plain_text)
        
        # key addition 
        cipher_text = key_addition(plain_text,keys[0])
        
        print("cipher size is ", len(cipher_text))
        print(cipher_text)
        # 10 rounds for encryption
        for i in range(10):
            cipher_text = byte_substitution(cipher_text)
            cipher_text = shift_row(cipher_text)
            cipher_text = mix_col(cipher_text)
            cipher_text = key_addition(cipher_text,keys[i+1])   # 1 -> 10

        all_cipher.extend(cipher_text)
    return all_cipher

def decrypt(original_cipher_text,key):
    string_plain_text =""

    key = key.upper()

    # convert key an C to binary int list
    key = hex_to_binary_list(key)

    keys = key_schedule(key) # 11 keys  // list of lists

    # get the last key then get keys agein
    decryption_key = keys[10]  
    keys = key_schedule(decryption_key) # 11 keys  // list of lists

    for i in range(0,len(original_cipher_text)//16,16):
        cipher_text = string_to_binary_list(original_cipher_text[i:i+16])
        # key addition
        plain_text = key_addition(cipher_text,keys[0])
        
        # 10 rounds for decryption
        for i in range(10):
            plain_text = inverse_byte_substitution(plain_text)
            plain_text = inverse_shift_row(plain_text)
            plain_text = inverse_mix_col(plain_text)
            plain_text = key_addition(plain_text,keys[i+1])   # 1 -> 10

        string_plain_text += binary_list_to_string(plain_text)
   
    return string_plain_text

def encryption(plaintext, key):
    cipher = AES.new(binascii.unhexlify(key), AES.MODE_ECB)
    padded_text = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def decryption(ciphertext, key):
    cipher = AES.new(binascii.unhexlify(key), AES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_text.decode()
# aaaaaaaaaaaaaaaa
####################################################################################################################################################
# main
# ... (existing code)

# main
key_size = 0
key = ""
count = 0
while key_size != 32:
    if count > 0:
        key = input("Wrong key! Please enter a 16-hex-digit key: ")
        key_size = len(key)
        if key_size == 32:
            break
    else:
        key = input("Enter your key with length 16 hexa digits: ")
        key_size = len(key)
        if key_size == 32:
            break
        count = 1

addition_char = 0
while True:
    x = input("Type 'encrypt (e)' for encryption or 'decrypt (d)' for decryption, or 'exit' to exit: ")
    if x.lower() == "exit":
        break
    elif x.lower() in ['e', 'encrypt']:
        plain_text = input("Enter plain text: ")
        count = 0
        if len(plain_text) % 16 != 0:
            while len(plain_text) % 16 != 0:
                count += 1
                plain_text += '#'
        addition_char = count

        # cipher_text = encrypt(plain_text.upper(), key)
        # print(cipher_text)
        print("plain text after padding is :" + plain_text)
        ciphertext = encryption(plain_text, key)
        print(ciphertext)
        print(f'Ciphertext: {binascii.hexlify(ciphertext).decode()}')
    elif x.lower() in ['d', 'decrypt']:
        C = input("Enter ciphertext (should be % 16 == 0): ")
        # plain_text = decrypt(C, key)
        # plain_text = plain_text[:len(plain_text) - addition_char]
        # print("Decrypted text as binary: \t", plain_text)
        decrypted_text = decryption(ciphertext, key)
        print(f'Decrypted Text: {decrypted_text[:len(decrypted_text)-addition_char]}')
    else:
        print("Invalid input. Please enter 'e' or 'd'.")

# key_size = 0
# key = ""
# count = 0
# while key_size != 16:
#     if count > 0:
#         key = input(" wrong key please enter 16 hixa digit key !!!!!!!!!! \n")
#         key_size = len(key)
#         if (key_size == 16): break
#     key = input(" enter your key with length 16 hexa digit  \n")
#     count = 1
#     key_size = len(key)
#     if key_size == 16 : break



# addition_char = 0 
# while(True):
#     x = (input( " type encrypt (e) for encryption or  dcrypt (d) for dycreption   or exit to exit "))
#     if x == "exit": break 
#     if(x == 'e' or x == 'encrypt'):
#         P = input(" enter plain text \n ")
#         count = 0 
#         if len(P) % 16 != 0:
#             while len(P) % 16 != 0:
#                 count += 1
#                 P += '#'
#         addition_char = count 

#         cipher_txt= encrypt(P.upper(), key)
#         print(cipher_txt)
#     else:
#         C = input(" enter cipher text (should be % 16 == 0 ) \n ")
#         plain_text = decrypt(C, key)
#         plain_text = plain_text[:len(plain_text)-addition_char]
#         print("dycrypted text as binary: \t" , plain_text)
