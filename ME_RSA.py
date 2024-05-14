import random

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

p = select_prime()
q = select_prime()
while p == q:
    q = select_prime()

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

    return e, d

# Step 3: Square and Multiply Function (Modular Exponentiation)
def square_and_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1: # check the right bit if it 1 (odd num) or 0 
            result = (result * base) % modulus  # multiply
        base = (base * base) % modulus # square
        exponent //= 2 #integer division on 2 to go to next digit
    return result

# Step 4: Encryption
def encrypt(character, e, p, q):  # take one character
    n = p * q
    X_ascii = ord(character) # Converts the character to its ASCII value
    cipher_text = str(square_and_multiply(X_ascii, e, n))
    return cipher_text

# Step 5: Decryption    decrypt char by char
def decrypt(x, d_p, d_q, p, q): # c -> x
    # Calculate dp and dq
    # dp ≡ d mod (p-1)    ,    dq ≡ d mod (q-1)
    dp = d_p % (p - 1)
    dq = d_q % (q - 1)

    # Calculate xp and xq
    # xp ≡ x mod p   ,  xq ≡ x mod q
    xp = (int(x) % p)
    xq = (int(x) % q)

    # Calculate yp and yq
    # yp ≡ xp^dp mod p   ,    yq ≡ xqdq mod q
    yp = square_and_multiply(xp, dp, p)
    yq = square_and_multiply(xq, dq, q)

    # Calculate cp and cq
    # cp ≡ q-1 mod p     ,   cq ≡ p-1 mod q
    cp = mod_inverse(q, p)
    cq = mod_inverse(p, q)

    # y ≡ [ q * cp ] * yp + [ p * cq ] * yq mod n
    y = (q * cp * yp + p * cq * yq) % (p * q) 

    return chr(y)



# Demonstration
def main():
    plaintext = input("Enter the plain text: ").upper()
    
    ciphertext = ""
    e_values = []
    d_values_p = []
    d_values_q = []

    for char in plaintext:
        e, d = generate_keys(p, q)
        c = encrypt(char, e, p, q) # return number as a string
        ciphertext += c + " "
        e_values.append(e)
        d_values_p.append(d % (p-1))
        d_values_q.append(d % (q-1))

    print("\nOriginal Text:", plaintext)
    #strip Return a copy of the string with leading and trailing whitespace removed. If chars is given and not None, remove 
    # characters in chars instead.
    print("Ciphertext:", ciphertext.strip()) 

    # Allow decryption with user-input ciphertext
    user_input = input("\nDo you want to decrypt? (yes/no): ").lower() 
    if user_input == "yes":
        try:
            user_ciphertext = input("Enter the ciphertext (space-separated): ")
            decrypted_text = ""

            for i, c in enumerate(user_ciphertext.split()):
                decrypted_char = decrypt(c, d_values_p[i], d_values_q[i], p, q)
                decrypted_text += decrypted_char

            print("Decrypted Text:", decrypted_text.lower())
        except ValueError:
            print("Invalid input. Please enter integers separated by spaces.")

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

