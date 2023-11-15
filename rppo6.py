import math
import base64

def generate_blocks(source_block, num_iterations):
    intermediate_blocks = []
    intermediate_blocks.append(source_block.copy())

    def generate_block_recursive(block, remaining_iterations):
        if remaining_iterations == 0:
            return
        new_block = block.copy()
        for j in range(len(block)):
            xor_result = 0
            for k in range(j + 1):
                xor_result ^= block[k]
            new_block[j] = xor_result
        intermediate_blocks.append(new_block)
        generate_block_recursive(new_block, remaining_iterations - 1)

    generate_block_recursive(source_block, num_iterations)

    return intermediate_blocks

def encrypt(source_block, block_number, num_iterations):
    intermediate_blocks = generate_blocks(source_block, num_iterations)
    return intermediate_blocks[block_number]

def decrypt(final_block, block_number, num_iterations):
    if block_number >= len(final_block):
        return []

    decrypted_blocks = []

    def generate_block_recursive(block, remaining_iterations):
        if remaining_iterations == 0:
            return
        new_block = block.copy()
        for j in range(len(block)):
            xor_result = 0
            for k in range(j + 1):
                xor_result ^= block[k]
            new_block[j] = xor_result
        decrypted_blocks.append(new_block)
        generate_block_recursive(new_block, remaining_iterations - 1)

    generate_block_recursive(final_block, num_iterations - block_number)

    return decrypted_blocks

def string_to_binary(string):
    utf8_bytes = string.encode('utf-8')
    binary_values = []
    for byte in utf8_bytes:
        binary_value = format(byte, '08b')  # Convert byte to 8-bit binary
        binary_values.extend([int(bit) for bit in binary_value])
    return binary_values

def binary_to_string(binary_values):
    # Convert binary values to bytes
    bytes_list = [binary_values[i:i+8] for i in range(0, len(binary_values), 8)]
    bytes_data = bytearray([int(''.join(map(str, byte)), 2) for byte in bytes_list])

    # Convert bytes to the original UTF-8 encoded string
    return bytes_data.decode('utf-8', errors='ignore')

def main(input_file, encrypted_output_file, decrypted_output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_string = file.read()  # Read the entire input file as a single string

            source_block = string_to_binary(input_string)
            size = len(source_block)

            num_iterations = 2 ** math.ceil(math.log2(size))
            block_number = int(input("Enter the block number for encryption: "))  # Prompt for block number

            intermediate_blocks = generate_blocks(source_block, num_iterations)

            # Print the intermediate blocks
            for i, block in enumerate(intermediate_blocks[1:block_number + 1], start=1):
                print(f'Encrypted Block {i}: {block}')

            # Encryption
            encrypted_block = encrypt(source_block, block_number, num_iterations)
            encrypted_string = binary_to_string(encrypted_block)

            with open(encrypted_output_file, 'w', encoding='utf-8') as encrypted_file:
                encrypted_file.write(encrypted_string)
            
            # Print the encrypted block
            print(f'Encrypted Block {block_number}: {encrypted_block}')

            # Decryption
            decrypted_blocks = decrypt(encrypted_block, block_number, num_iterations)
            decrypted_string = binary_to_string(decrypted_blocks[-1])

            with open(decrypted_output_file, 'w', encoding='utf-8') as decrypted_file:
                decrypted_file.write(decrypted_string)

            # Print the decrypted blocks
            for i, block in enumerate(decrypted_blocks):
                print(f'Decrypted Block {i + block_number + 1}: {block}')

            # Print progress
            print(f'Processed input from file: {input_file}')
            print(f'Encrypted String: {encrypted_string}')
            print(f'Decrypted String: {decrypted_string}')
            print(f'Encrypted Block {block_number}: {encrypted_block}')

        print("Encryption and decryption completed.")
    except FileNotFoundError:
        print(f"File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = 'input.txt'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.txt'  # Change to the desired encrypted output file path
    decrypted_output_file = 'decrypted.txt'  # Change to the desired decrypted output file path
    main(input_file, encrypted_output_file, decrypted_output_file)
