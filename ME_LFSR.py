from numpy import random

def encryption(vector, function, binary_strem): #vector and function are int list , binary_strem is string
    encrypted_stream = []
    LSFR_all_sequene = []
    print("\n encryption ")
    # for neglect the first occurance of LFSR we should out the len(vector) bits and insert next_bits as a new vector
    # but we need the output for the initial vector

    for i in range(len(vector)):
        LSFR_all_sequene.append(vector[len(vector)-1]) # the last rigth bit of vector
        next_bit = 0
        j = 0
        while j < len(vector):
            if function[j]:
                next_bit ^= vector[j] 
            j = j+1
        print(" next bits number ", i+1 , ": ", next_bit)
        j = len(vector)-1  # the right most bit in vector
        while j > 0:
            vector[j] = vector[j-1]
            j = j-1
        vector[0] = next_bit 
    #for table priinting out of while loop 
    print("the first neglected bits from vector  ( initial vector ): ", LSFR_all_sequene[0:len(vector)])
    print("\n new initial vector is new next bits:  ", vector)

    # encrypt the stream 
    for i in range(len(binary_strem)): # bit by bit on stream
        out_stream = binary_strem[i] #binary_strem[len(binary_strem)-i-1]  # 1 bit of binary stream 
        #binary_strem = binary_strem[:len(binary_strem)-1] # ubdate our string to remove the last char
        out_LFSR = vector[len(vector)-1] # the first output (on right) of LFSR
        LSFR_all_sequene.append(out_LFSR)
        encrypted_bit = (out_LFSR ^ out_stream)
        encrypted_stream.append(encrypted_bit)
        next_bit = 0
        j = 0
        # LFSR function for next bit ( current_vector * function + next bit)
        while j < len(vector):
            if function[j]:
                next_bit ^= vector[j] 
            j = j+1
        #for inserting new  bit ( updating vector )
        j = len(vector)-1  # the right most bit in vector
        while j > 0:
            vector[j] = vector[j-1]
            j = j-1
        vector[0] = next_bit 

    print(" \n LFSR sequence    plain text Sequence    cipherd text sequence \n")
    #LSFR_all_sequene.reverse()
    for i in range(len(binary_strem)): #LSFR_all_sequene[i+len(vector)-1]
        print("\t", LSFR_all_sequene[i+len(vector)], "\t\t", binary_strem[i], "\t\t\t", encrypted_stream[i], "\n")

    return encrypted_stream # list of bits 


def decryption(vector, function, encrypted_stream):
    decrypted_stream = []
    LSFR_all_sequene = []
    
    print(" decryption ")
    # for neglect the first occurance of LFSR we should out the len(vector) bits and insert next_bits as a new vector
    # but we need the output for the initial vector
    for i in range(len(vector)):
        LSFR_all_sequene.append(vector[len(vector)-1])
        # find next bit
        next_bit = 0
        j = 0
        while j < len(vector):
            if function[j]:
                next_bit ^= vector[j] 
            j = j+1
        # update vector
        j = len(vector)-1  # the right most bit in vector
        while j > 0:
            vector[j] = vector[j-1]
            j = j-1
        vector[0] = next_bit 

    print("the first neglected bits from vector  ( initial vector )")
    print(LSFR_all_sequene[0:len(vector)])
    print("\n new initial vector is new next bits:  ", vector)
        
    for i in range(len(encrypted_stream)): # bit by bit on stream
        out_stream = encrypted_stream[i]  # 1 bit of binary stream 
        #encrypted_stream = encrypted_stream[:len(encrypted_stream)-1]
        out_LFSR = vector[len(vector)-1] # the first output (on right) of LFSR
        decrypted_bit = out_LFSR ^ out_stream
        decrypted_stream.append(decrypted_bit)
        LSFR_all_sequene.append(out_LFSR)
        #for  inserting new  bit ( updating vector )
        next_bit = 0
        j = 0
        # LFSR function for next bit ( current_vector * function + next bit)
        while j < len(vector):
            if function[j]:
                next_bit ^= vector[j] 
            j = j+1
        j = len(vector)-1  # the right most bit in vector
        while j > 0:
            vector[j] = vector[j-1]
            j = j-1
        vector[0] = next_bit 

    #for table priinting out of while loop 
    print(" \n LFSR sequence    encrypted strem \t  decrypted text sequence \n")
    for i in range(len(decrypted_stream)):
        print("\t", LSFR_all_sequene[i+len(vector)], "\t\t ", encrypted_stream[i] , "\t\t ", decrypted_stream[i] , "\n")

    # return dycrepted stream bits as string
    # take 8 bu 8 bits and convert them to corresponding char 
    string_stream = "" 
    for i in range (0,len(decrypted_stream),8):
        binary_list = decrypted_stream[i:i+8] # Example list of 8 binary integers
        binary_string = ''.join(map(str, binary_list))  # Convert the list to a binary string
        decimal_value = int(binary_string, 2)  # Convert the binary string to a decimal value
        character = chr(decimal_value)  # Convert the decimal value to a character
        string_stream +=  character
    return decrypted_stream , string_stream # list of bits

def check_primitive_inner(vector, function): # return LSFR stream from given function and vector
    LSFR_all_sequence = []
    
    # to  neglect innitial vector
    for i in range(len(vector)):
        next_bit = 0
        #LSFR_all_sequene.append(vector[len(vector)-1]) we don't nedd initial sequence
        j = 0
        while j < len(vector):
            if function[j]:
                next_bit ^= vector[j] 
            j = j+1
        j = len(vector)-1  # the right most bit in vector
        while j > 0:
            vector[j] = vector[j-1]
            j = j-1
        vector[0] = next_bit 
        
    tries = (2**len(vector)-1)*3
    for i in range(tries):
        out_LFSR = vector[len(vector)-1] # the first output (on right) of LFSR
        LSFR_all_sequence.append(out_LFSR)
        next_bit = 0 
        j = 0
        while j < len(vector):
            if function[j]:
                next_bit ^= vector[j] 
            j = j+1
        j = len(vector)-1  # the right most bit in vector
        while j > 0:
            vector[j] = vector[j-1]
            j = j-1
        vector[0] = next_bit 
    return LSFR_all_sequence
    
    
def check_primitive(vector , function):
    sequence = check_primitive_inner(vector, function)
    size_ = (2**len(vector)-1)
    prim = 1
    indexes = []
    print(" indexes at first as empty: ", indexes)
    for i in range(size_):
        if(sequence[i]!=sequence[i+size_]):
            prim = 0 
            indexes.append(i)
            break 
    if(prim):return "primitives"
    
    # if it isn't prime it is reducible or irreducible
    # if changing the initial vector don't affect it is Irreducible
    # if it depend on initial vector it is reducible
    for k in range(len(vector)):
        new_vector = [int(random.choice([0, 1])) for _ in range(len(vector))]
        print("new vector: " , new_vector)
        print("type new vector: " , type(new_vector))
        new_sequence = check_primitive_inner(new_vector, function)
        for i in range(size_):
            if(new_sequence[i]!=new_sequence[i+size_]):
                indexes.append(i)
                break
    indexes = sorted(indexes)
    print(" ----------------------------- ")
    print(indexes)
    print("type indexes : ",type(indexes) )
    print("size indexes:  ",   len(indexes))
    if indexes and indexes[0] == indexes[-1] and indexes[0] and indexes[-1]:
        return "irreducible"
    else:
        return "reducible"
    
    
    
    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////    main 

# P = input("enter plain text\n")
# binary_P = ''.join(format(ord(i), '08b') for i in P) # convert string to binary (binary_P is string type consist of 01011..)
# binary_P = [int(char) for char in binary_P] # binary P as list
# print(" text as binary:", binary_P)

m = int(input("enter degree of linear function \n"))
temp_p_of_x = input("enter p(x)\n")  # "x5+x4+x+1" function as a string
LFSR_function = [0] * m #int

i = 0
while i < len(temp_p_of_x):
    if temp_p_of_x[i] == 'x' and i > 0 and i + 1 < len(temp_p_of_x) and temp_p_of_x[i+1] != '+':
        place = int(temp_p_of_x[i + 1])
        LFSR_function[place]=1 
    elif temp_p_of_x[i] == 'x' and (temp_p_of_x[i + 1] == '+' or i + 1 == len(temp_p_of_x)): # last x in equation 
        LFSR_function[1] = 1 # second right bit
    elif temp_p_of_x[i] == '1': # 1 in equation 
        LFSR_function[0] = 1 # last right bit
    i += 1
LFSR_function.reverse()

temp_vector = (input("enter vector\n")) # one number ( string )
vector = [int(char) for char in temp_vector] # int
vector2 = vector.copy()
vector3 = vector.copy()
print("input vector: ", vector)

# encrypted_stream = []
check = "ali"
while check != "end":
    check = input(" enter e for encryption or d for dycryption or end to end ")
    if check == "e":
        P = input("enter plain text\n")
        binary_P = ''.join(format(ord(i), '08b') for i in P) # convert string to binary (binary_P is string type consist of 01011..)
        binary_P = [int(char) for char in binary_P] # binary P as list
        print(" text as binary:", binary_P)
        encrypted_stream = encryption(vector, LFSR_function, binary_P)# def encryption(vector, function, binary_strem) -> return encrypted stream and print the sequence of operations 
        print(" encrypted stream in list \n", encrypted_stream ,"\n")
        print(" encrypted stream: " + ''.join(map(str,encrypted_stream)) + "\n")
    if check =="d":
        encrypted_stream = input(" enter encryption stream  ")
        encrypted_stream = [int(char) for char in encrypted_stream]
        decrypted_stream, real_stream = decryption(vector2, LFSR_function, encrypted_stream) #return deycrpted scream and real string (in function we also pritn operations )
        print(decrypted_stream , "\n", real_stream + "\n")
    if check == "end":
        print(check_primitive(vector3 ,LFSR_function))
        break


