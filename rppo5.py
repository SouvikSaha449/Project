import math
import base64

def generate_block(source_block, num_iterations):
    for _ in range(num_iterations):
        new_block = [0] * len(source_block)
        xor_result = 0
        for i in range(len(source_block)):
            xor_result ^= source_block[i]
            new_block[i] = xor_result
        source_block = new_block
    return source_block

def encrypt(input_file, block_number):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_string = file.read()
            source_block = [int(bit) for bit in ''.join(format(ord(char), '08b') for char in input_string)]
            size = len(source_block)
            num_iterations = 2 ** math.ceil(math.log2(size))

            if block_number < num_iterations:
                encrypted_block = generate_block(source_block, num_iterations)
                # Convert the encrypted block back to a string
                encrypted_string = ''.join(str(bit) for bit in encrypted_block)
                return encrypted_string
            else:
                return "Block number is out of range."

    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def decrypt(encrypted_string, block_number):
    try:
        source_block = [int(bit) for bit in encrypted_string]
        size = len(source_block)
        num_iterations = 2 ** math.ceil(math.log2(size))

        if block_number < num_iterations:
            decrypted_block = generate_block(source_block, num_iterations)
            # Convert the decrypted block back to a string
            decrypted_string = ''.join(chr(int(''.join(str(bit) for bit in decrypted_block[i:i+8]), 2)) for i in range(0, len(decrypted_block), 8))
            return decrypted_string
        else:
            return "Block number is out of range."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    input_file = 'input.txt'  # Change to the actual input file path
    block_number = int(input("Enter the block number for encryption: "))
    encrypted_string = encrypt(input_file, block_number)
    print(f'Encrypted String: {encrypted_string}')

    decrypted_string = decrypt(encrypted_string, block_number)
    print(f'Decrypted String: {decrypted_string}')
