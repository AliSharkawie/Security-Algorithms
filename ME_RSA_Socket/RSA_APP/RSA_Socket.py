import random
import ast
# Step 1: Selecting Prime Numbers (p, q) using Fermat Algorithm
def is_prime(n, k=5):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Use Fermat's Little Theorem for primality testing
    # select any number a in range (n-1) -> if  a^n-1 % n  == 1  so n is prime 
    # if n is prime so any a will be correlatively prime with n and  (a^n-1 % n = 1)  if n prime n-1 is p-1
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:   # = a^n-1 % n
            return False
    return True

def select_prime():
    while True:
        p = random.randint(100, 500)
        if is_prime(p):
            return p


# Step 2: Generating Keys (e, d)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#  calculate inverse using the Extended Euclidean Algorithm
def mod_inverse(a, m):
    m0, ti_1, ti = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        #x0, x1 = x1 - q * x0, x0
        # update
        ti_1, ti = ti - q * ti_1, ti_1
    return ti + m0 if ti < 0 else ti

def generate_keys(p, q):
    n = p * q  # Modulus
    phi = (p - 1) * (q - 1)  # Euler's totient function

    # Choose a public exponent 'e' (must be relatively prime to phi)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Calculate the private exponent 'd'
    d = mod_inverse(e, phi)

    return e, n, d

####################################################
p = select_prime()
q = select_prime()
while p == q:
    q = select_prime()

e, n, d = generate_keys(p, q)
####################################################

# Step 3: Square and Multiply Function (Modular Exponentiation)
def square_and_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus
    #
    # exponent >>= 1 #integer division on 2 to go to next digit
    #
    while exponent > 0:
        if exponent % 2 == 1: # check the right bit if it 1 (odd num) or 0 
            result = (result * base) % modulus  # multiply
        base = (base * base) % modulus # square
        exponent //= 2 #integer division on 2 to go to next digit
    return result

# Step 4: Encryption
def encrypt(message, e, n):  # take string character 
    # ord(char) # Converts the character to its ASCII value
    cipher_text = [square_and_multiply(ord(char), e, n) for char in message]
    # convert int list to string
    #cipher_text = ''.join(map(str, cipher_text)) 
    return cipher_text  # int list # string ( the integer list as string )

# take int list ( from decryption)
def decrypt(cipher_text, d, p, q):
    # take scipher text as string from encrypt 
    # firstly return the int list then dycrept
    # convert string to int list
    # cipher_text = list(map(int, cipher_text.split(" ")))
    # cipher_text = list(map(int, cipher_text))

    dp = d % (p - 1)
    dq = d % (q - 1)

    decrypted_text = []
    for char in cipher_text:
        xp = pow(char, dp, p)
        xq = pow(char, dq, q)

        cp = mod_inverse(q, p)
        cq = mod_inverse(p, q)

        yp = xq * p * cq
        yq = xp * q * cp

        y = (yp + yq) % (p  * q)
        decrypted_text.append(y)
        #decrypted_text.append(" ")
    

#    return "".join(chr(char) for char in decrypted_text)
    decrypted_text = ''.join(map(chr, decrypted_text))
    return decrypted_text



###########################################################################################################################
def main():
    choice = "asd"
    while choice != "end":
        choice = (input(" encrypt  or decrypt    or end to end \n")).lower()
        if choice == "end":
            break
        if choice == "encrypt" or choice == "e":
            sentence = input(" enter plain text \n ")
            encrypted_sentence = (encrypt(sentence, e, n)) # return list then .join
            print("cipher text is : \t" ,  encrypted_sentence)

            # encrypted_sentence = ''.join(map(chr, encrypted_sentence))
            # print(encrypted_sentence)
            # # Encode the string to bytes using utf-8 encoding
            # encrypted_as_byte_data = encrypted_sentence.encode('utf-8')
            # print(encrypted_sentence)

            # byte_recieved_data = encrypted_as_byte_data.decode('utf-8')
            # print(byte_recieved_data)
            # user_ciphertext_int_list = [ord(char) for char in byte_recieved_data]
            # print(user_ciphertext_int_list)


            # decrypted_text = (decrypt(user_ciphertext_int_list,d,p,q))
            # print(' decryption is : ', decrypted_text)

        else :
            cipher = input(" enter cipher text ")
            #cipher = "[" + cipher + "]"

            # Safely evaluate the input string to get a list of integers
            cipher = ast.literal_eval(cipher)
            plain = decrypt(cipher, d, p, q)
            print("plain text is:\t " + plain)


#Demonstration

if __name__ == "__main__":
    main()








# In Python, when you run a script, the interpreter sets a special variable called __name__. The __name__ variable is a built-in variable that
# indicates the "namespace" of the script. Specifically:

# If the script is being run as the main program (i.e., it is the entry point of execution), then __name__ is set to "__main__".
# If the script is being imported as a module into another script or program, then __name__ is set to the name of the module (i.e., not "__main__").

# When you run your script directly (not imported as a module), Python sets __name__ to "__main__".
# The condition if __name__ == "__main__": is satisfied, and the main() function is called, initiating the execution of 
# the main part of your script.

# If someone else imports your script as a module in another Python script, the __name__ variable is set to the name of the module (not "__main__").
# In this case, the condition if __name__ == "__main__": evaluates to False, and the code inside the block is not executed. This allows the script 
# to be used as a module without automatically running the main() function.


# def decrypt(x, d, p, q): # c -> x
#     # Calculate dp and dq
#     # dp ≡ d mod (p-1)    ,    dq ≡ d mod (q-1)
#     dp = d % (p - 1)
#     dq = d % (q - 1)

#     # Calculate xp and xq
#     # xp ≡ x mod p   ,  xq ≡ x mod q
#     xp = (int(x) % p)
#     xq = (int(x) % q)

#     # Calculate yp and yq
#     # yp ≡ xp^dp mod p   ,    yq ≡ xqdq mod q
#     yp = square_and_multiply(xp, dp, p)
#     yq = square_and_multiply(xq, dq, q)

#     # Calculate cp and cq
#     # cp ≡ q-1 mod p     ,   cq ≡ p-1 mod q
#     cp = mod_inverse(q, p)
#     cq = mod_inverse(p, q)

#     # y ≡ [ q * cp ] * yp + [ p * cq ] * yq mod n
#     y = (q * cp * yp + p * cq * yq) % (p * q) 















