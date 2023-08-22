def char_to_ascii(input_string):
    ascii_list = [ord(char) for char in input_string]
    return ascii_list

def ascii_to_char(ascii_list):
    char_list = [chr(ascii_val) for ascii_val in ascii_list]
    return ''.join(char_list)

def recursive_paired_parity_operation(ascii_val):
    binary_val = bin(ascii_val)[2:].zfill(8)
    parity_bit = binary_val.count('1') % 2
    encrypted_val = (ascii_val << 1) | parity_bit
    return encrypted_val

def recursive_paired_parity_encrypt(ascii_values, num_steps):
    encrypted_list = []
    for ascii_val in ascii_values:
        print(f"Encryption Step 0: ASCII value {ascii_val}")
        for step in range(1, num_steps + 1):
            ascii_val = recursive_paired_parity_operation(ascii_val)
            print(f"Encryption Step {step}: ASCII value {ascii_val}")
        encrypted_list.append(ascii_val)
    return encrypted_list

def recursive_paired_parity_decrypt(encrypted_values, num_steps):
    decrypted_list = []
    for encrypted_val in encrypted_values:
        print(f"Decryption Step 0: ASCII value {encrypted_val}")
        ascii_val = encrypted_val
        for step in range(1, num_steps + 1):
            ascii_val = ascii_val >> 1
            print(f"Decryption Step {step}: ASCII value {ascii_val}")
        decrypted_list.append(ascii_val)
    return decrypted_list

input_string = input("Enter a string: ")
ascii_values = char_to_ascii(input_string)
half_length = len(ascii_values) // 2
encryption_steps = half_length
print("\nASCII Values:", ascii_values)
print("\nEncryption:")
encrypted_values = recursive_paired_parity_encrypt(ascii_values, encryption_steps)

encrypted_string = ascii_to_char(encrypted_values)
print("\nOriginal String:", input_string)
print("\nASCII Values:", ascii_values)
print("\nEncrypted String:", encrypted_string)
print("\nEncrypted ASCII Values:", encrypted_values)

# Decryption
decryption_steps = encryption_steps
print("\nDecryption:")
decrypted_values = recursive_paired_parity_decrypt(encrypted_values, decryption_steps)
decrypted_string = ascii_to_char(decrypted_values)

print("\nDecrypted String:", decrypted_string)
print("\nDecrypted ASCII Values:", decrypted_values)
