import numpy as np

#permutation table of the f function
pp = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

# ip = 64   data initial permutaiton 
ip = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32,
      24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47,
      39, 31, 23, 15, 7]
# ip-1 = 64    data fnal permutaion
ip_1 = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53,
        21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1,
        41, 9, 49, 17, 57, 25]
# pc-1 = 56  as permutatoin with parity check bit removing for key
pc_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63,
        55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
# pc-2 = 48 as output from 56 key
pc_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
# Expansion = 48 output from 32 bit
Expansion = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]
]

def binary_to_ascii(binary_list):
    s = []
    for i in range(0, len(binary_list), 8):
        # Convert the binary list to a string
        binary_string = ''.join(map(str, binary_list[i:i+8]))

        # Convert binary string to decimal integer
        decimal_integer = int(binary_string,2)

        # Convert decimal integer to ASCII character
        s.append(chr(decimal_integer))

    return ''.join(s)

def generate_key(key):  # key is 01010.. string

    dec_key = []  # special fo rfycryption
    
    # pc-1
    key_after_pc_1 = []  # list of binary numbers(integers) ( length = key (56))
    index = 0
    while index < 56:  # make pc-1 for key
        key_after_pc_1.append((int(key[pc_1[index] - 1])))  # - '0' # -'0' to be int not char (key is char)
        index += 1

    # key rounds 
    k = key_after_pc_1  # .copy() ,   key become 1-D list
    left = k[0:28]  # list of nums ( binary )
    right = k[28:56]
    sub_keys = []  # list of keys ( each key is list of binary numbers  )
    index = 0
    while index < 16:
        subkey = []
        if index == 0 or index == 1 or index == 8 or index == 15:  # shift left by 1
            left = left[1:] + left[0:1]
            right = right[1:] + right[0:1]
        else:  # shift left by 2
            left = left[2:] + left[0:2]
            right = right[2:] + right[0:2]
        subkey += left
        subkey += right
        sub_keys.append(subkey)  # subkey now is a list (56)
        index += 1

        # last key for dycryption i snedded before pc-2 (need it as 56 bits) 
        # add last key twice 
        if (index == 16):
            dec_key = subkey

    # pc-2 operation  to make subkey as 48  bit from 56 (left + right) 
    sub_keys_2 = [] # sub_keys.copy()
    for sub_key in sub_keys:  # for each list (for each subkey 56 bits) we take 48 bits from 56 
        temp_key = []
        x = 0
        while x < 48:
            temp_key.append(sub_key[pc_2[x] - 1])
            x += 1
        sub_keys_2.append(temp_key)  # temp_key(subkey) is 48 bit as list of 48 integer 
        # temp key is list , subkeys is list of list

    sub_keys_2.append(dec_key)  # addtional key for dycreption but not affect on our equations bec our loops is 0 --> 15
    return sub_keys_2  # list of subkeys (list of integer lists (48) )

def generate_key_for_decryption(key):  # same dycreption but shift right, also the key is the result from decryption
    # key = list(key)

    # pc-1
    key_after_pc_1 = []  # list of binary numbers(integers) ( length = key (56))
    index = 0
    while index < 56:  # make pc-1 for key
        key_after_pc_1.append(int(key[pc_1[index] - 1]))  # - '0' # -'0' to be int not char (key is char)
        # note : appending item is ok the list will add item 
        # but appending list will add all list as one item not concatinate it
        index += 1

    # key rounds
    k = key_after_pc_1  
    left = k[0:28]
    right = k[28:56]
    sub_keys = []
    index = 0
    while index < 16:
        subkey = []
        if index == 0 or index == 1 or index == 8 or index == 15:  # shift right by 1
            left = left[28 - ( 1):] + left[0: 28 - ( 1)]
            right = right[28 - (1):] + right[0:28 - ( 1)]
        else:  # shift right by 2
            left = left[28 - (2):] + left[0: 28 - ( 2)]
            right = right[28 - (2):] + right[0:28 - ( 2)]
        subkey += left
        subkey += right
        sub_keys.append(subkey)
        index += 1
    
    # pc-2 for all keys
    sub_keys_2 = []# sub_keys.copy()
    for sub_key in sub_keys:
        temp_key = []
        x = 0
        while x < 48:
            temp_key.append(sub_key[pc_2[x] - 1])
            x += 1
        sub_keys_2.append(temp_key)
    return sub_keys_2


def F(R, K):  # R, K is lists of integers R is 32 and k is 48   // note that F function take one subkey
    # expand R 
    extended_R = []
    for i in range(48):
        extended_R.append(int(R[Expansion[i] - 1]))

    # make xor between R and K    
    xor_result = []  # 48 bit
    for i in range(48):
        xor_result.append((extended_R[i] ^ K[i]))

    # make S box for every xor_result  to get 32 
    xor_result_and_s_box = []
    count = 0  # to define each s-box we work on
    loop_count = 0
    while loop_count < 48:
        temp = xor_result[loop_count:loop_count + 6]  # take each 6 bits seperately ( as list )
        row = temp[0:1] + temp[5:6] # concatinate 2 lists --> one list
        row = ''.join(map(str, row))  # convert list(row) to string (binary string "010101111")
        row = int(row, 2)  # convert binary string to it's decimal value ,
        # now row become decimal number the representation for 2 bits that represent row
        col = temp[1:5]
        col = ''.join(map(str, col))
        col = int(col, 2)  # now col become decimal number the representation for 4 bits that represent cloumn
        new_num = S_BOXES[count][row][col]  # return decimal number

        binary_new_num = bin(new_num)[2:]  # bin function return string as binary representation for nwe_num, we use slicing 2 because
        # bin return 0b(binary_representation) so we don't need 0b indication
        # push them in xor_result_and_s_box list as numbers 
        # example : 
        # x = 10 
        # binary_representation = bin(x)   -> binary representation = '0b1010'

        # adjust binary num to be sure that is 4 bits
        reversed_binary_new_num = binary_new_num[::-1]  # reversed is also string
        while (len(reversed_binary_new_num) < 4):
            reversed_binary_new_num += ('0')  
        # binary num become 4 chars
        # return binary num again to correct order
        binary_new_num = reversed_binary_new_num[::-1]  # string

        # convert binary num string

        for z in range(4): # for each digit in s-box output number
            xor_result_and_s_box.append(int(binary_new_num[z]))  # - '0')  # take binary bits and push it in result
        # update loop 
        count += 1
        loop_count += 6
    
    new_xor_result_and_s_box = []
    
    for j in range(32):  
        new_xor_result_and_s_box.append(int(xor_result_and_s_box[pp[j]- 1]))

    return new_xor_result_and_s_box   # 32 bit sequence 


#######################################################################################################################################
#######################################################################################################################################


def encryption(P, key):# P and key is binary string //  # return cipher blocks //  list of lists(binary string)
    
    # convert P from strings to binary string
    temp_blocks = []
    i = 0
    while i < (len(P)):
        temp = P[i:i + 8]
        temp_blocks.append(''.join(format(ord(char), '08b') for char in temp))  # blocks is list of binary strings
        i += 8
    temp_blocks = ''.join(temp_blocks) # one string
    P = []
    P = temp_blocks


    keys = generate_key(key)  # return  16 subkeys  (list)  "handle key conversion"
    # P blocks (data) list of strings each string is binary number but in string (string of '01011..' )
    # P i sbinary string

    # initial permutation 
    """    
    blocks = []
    if (len(P)>1):
        for block in P:  # for each block(binary string) , block is string of 010100..
            new_block = []  # permuted block ( list of integers)
            for i in range(len(block)):  # 64
                new_block.append(int(block[ip[i] - 1]))  # - '0')
            blocks.append(new_block)
    else:
        for i in range(len(P)):  # for each block(binary string) , block is string of 010100..
            new_block.append(int(block[ip[i] - 1]))  # - '0')
        blocks.append(new_block)
     """
    blocks = []
    i = 0 
    while i < (len(P)):  # for each block(binary string) , block is string of 010100..
        new_block = []  # permuted block ( list of integers)
        for j in range(64):  # 64
            new_block.append(int(P[ip[j] - 1]))  # - '0')
        blocks.append(new_block)
        i+= 64        
    
    print(" initial  permutation : \t",  blocks)
    # we make new block that is a permuted block and represented as integer list 
    # we have new blocks as permuted block and integer numbers

    # encryption for each block # each block now is list of nums not chars (not binary strings) 
    cipher_data = []
    for block in blocks:  # encrypt each block  // each block
        cipher_block = []
        # L and R is the current block data
        Li_1 = block[0:32]
        Ri_1 = block[32:]
        for j in range(16):  # 16 round for each block ( encrypt the block invidually)
            Ki = keys[j]
            Li = Ri_1
            f = F(Ri_1, Ki)  # list 32
            Ri = [] #Li_1  # just ti be size 32 but i will override on it
            for k in range(32):
                Ri.append(Li_1[k] ^ f[k])
            # update 
            Li_1 = Li
            Ri_1 = Ri
            print( "round ", j , "\t",  Li+Ri)
        cipher_block = Li + Ri # concatinating # the last L+R is the decryption result for the current block

        # do final permutation for cipher block
        new_cipher_block = []
        for i in range(len(cipher_block)):  # 64
            new_cipher_block.append(cipher_block[ip_1[i] - 1])
        
        print(" final permutation : \t",  new_cipher_block)
        # append the cipher block in all cipher list
        cipher_data += new_cipher_block # all data (all blocks)

    return cipher_data ,binary_to_ascii(cipher_data)   # list of binary int , the encrypted data as text


#######################################################################################################################################
#######################################################################################################################################
def decryption(C, key):

    # convert P from strings to binary string
    temp_blocks = []
    i = 0
    while i < (len(C)):
        temp = C[i:i + 8]
        temp_blocks.append(''.join(format(ord(char), '08b') for char in temp))  # blocks is list of binary strings
        i += 8
    temp_blocks = ''.join(temp_blocks)
    C = []
    C = temp_blocks

    # temp_keys = generate_key(key)  # tha same function in dycryption to get   k16
    # dec_key = ''.join(map(str, temp_keys[16])) # get the last key and convert it to its binary string to call function again
    # ( function should take binary string )
    # generate keys again for decryption ( the same as encryption but shift right and begin with k16) 
    # keys = generate_key_for_decryption(dec_key)
    keys = generate_key(key)
    # the same algorithm for encryption 
    
    # initial permutation     
    blocks = []
    i = 0 
    while i < (len(C)):  # for each block(binary string) , block is string of 010100..
        new_block = []  # permuted block ( list of integers)
        for j in range(64):  # 64
            new_block.append(int(C[ip[j] - 1]))  # - '0')
        blocks.append(new_block)
        i+= 64 
    print(" initial permutation : \t",  blocks)
    #blocks.append(new_block)
    # we make new block that is a permuted block and represented as integer list 
    # we have new blocks as permuted block and integer numbers

    # encryption for each block 
    cipher_data = []
    for block in blocks:  # encrypt each block  // each block
        cipher_block = []
        # L and R is the current block data
        Li_1 = block[0:32]
        Ri_1 = block[32:]
        for j in range(16):  # 16 round
            Ki = keys[j]
            Li = Ri_1
            f = F(Ri_1, Ki)  # list 32
            Ri = [] #Li_1  # just ti be size 32 but i will override on it
            for k in range(32):
                Ri.append(Li_1[k] ^ f[k])
            # update 
            Li_1 = Li
            Ri_1 = Ri
            print( "round ", j , "\t",  Li+Ri)
        cipher_block = Li + Ri
        # do final permutation for cipher block
        new_cipher_block = []
        for i in range(len(cipher_block)):  # 64
            new_cipher_block.append(cipher_block[ip_1[i] - 1])
        
        print(" final permutation : \t",  new_cipher_block)
        # append the cipher block in all cipher list
        cipher_data.append(new_cipher_block)
    
    # convert binary stream to string
    #plain_txt = ''.join(map(str, cipher_data))
    #cipher_data_txt = (''.join([chr(int(bin_char, 2)) for bin_char in [plain_txt[i:i + 8] for i in range(0, len(plain_txt), 8)]]))
    
    # temproray solve error 
    l = []
    for i in range(len(cipher_data[0])):
        l.append(int(cipher_data[0][i]))

    cipher_data_txt = binary_to_ascii(l)

    return cipher_data , cipher_data_txt  # list of binary strings lists, text


#######################################################################################################################################
#######################################################################################################################################


# main
key_size = 0
str_key = ""
count = 0
while key_size < 8:
    if count > 0:
        str_key = input(" wrong key please enter 8 characters key !!!!!!!!!! \n")
        key_size = len(str_key)
        if (key_size == 8): break
    str_key = input(" enter your key with length 8 char \n")
    count += 1
    key_size = len(str_key)
    if key_size == 8: break
key = ''.join(
    format(ord(char), '08b') for char in str_key)  # (key is binary string) binary_representation of key in string

x = int(input( " type 0 for encryption or 1 for dycreption  "))
if(x == 0):
    P = input(" enter plain text \n ")
    if len(P) % 8 != 0:
        while len(P) % 8 != 0:
            P += '#'
    
    
    #string_P = []
    #i = 0
    #while i < (len(P)):
    #    temp = P[i:i + 8]
    #    string_P.append(''.join(format(ord(char), '08b') for char in temp))  # blocks is list of binary strings
    #    i += 8
    #print("plain txt is :\t" + P)
    #print("plain text as binary representation is \t:"); print(string_P)
    cipher , cipher_txt= encryption(P, key)
    print("cipher bits :\n", cipher, "\n cipher text :\n", cipher_txt)
else:
    C = input(" enter cipher text (should be %8 == 0 ) \n ")
    string_C = []
    i = 0
    while i < (len(C)):
        temp = C[i:i + 8]
        string_C.append(''.join(format(ord(char), '08b') for char in temp))  # blocks is list of binary strings
        i += 8
    plain, plain_txt = decryption(C, key)
    print("dycrypted text as binary: \t" , plain)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # print("dycrepted text: \t", plain_txt)



