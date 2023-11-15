import math
import time
import base64
import sys

new_depth_limit = 10000000 
sys.setrecursionlimit(new_depth_limit)

def generate_blocks(source_block, num_iterations, operation_counts):
    intermediate_blocks = [source_block.copy()]

    def generate_block_recursive(block, remaining_iterations):
        if remaining_iterations == 0:
            return
        xor_result = 0
        new_block = block.copy()
        operation_count = 0  # Count operations in this iteration
        for i in range(len(block)):
            xor_result ^= block[i]
            new_block[i] = xor_result
            operation_count += 1
        intermediate_blocks.append(new_block)
        operation_counts.append(operation_count)
        generate_block_recursive(new_block, remaining_iterations - 1)

    generate_block_recursive(source_block, num_iterations)

    return intermediate_blocks

def encrypt(source_block, block_number, num_iterations):
    operation_counts = []  # To count operations
    intermediate_blocks = generate_blocks(source_block, num_iterations, operation_counts)
    if block_number < len(intermediate_blocks):
        return intermediate_blocks[block_number], sum(operation_counts[:block_number + 1])
    else:
        return [], 0

def decrypt(final_block, block_number, num_iterations):
    operation_counts = []  # To count operations
    if block_number >= len(final_block):
        return [], 0

    decrypted_blocks = []

    def generate_block_recursive(block, remaining_iterations):
        if remaining_iterations == 0:
            return
        xor_result = 0
        new_block = block.copy()
        operation_count = 0  # Count operations in this iteration
        for i in range(len(block)):
            xor_result ^= block[i]
            new_block[i] = xor_result
            operation_count += 1
        decrypted_blocks.append(new_block)
        operation_counts.append(operation_count)
        generate_block_recursive(new_block, remaining_iterations - 1)

    generate_block_recursive(final_block, num_iterations - block_number)

    return decrypted_blocks, sum(operation_counts)

def string_to_binary(string):
    utf8_bytes = string.encode('utf-8')
    binary_values = bytearray()
    for byte in utf8_bytes:
        binary_value = format(byte, '08b')  # Convert byte to 8-bit binary
        binary_values.extend([int(bit) for bit in binary_value])
    return binary_values

def binary_to_string(binary_values):
    # Ensure the length of binary_values is a multiple of 8
    if len(binary_values) % 8 != 0:
        raise ValueError("Binary values length must be a multiple of 8 for proper decoding.")

    # Convert binary values to bytes
    bytes_list = [binary_values[i:i+8] for i in range(0, len(binary_values), 8)]
    bytes_data = bytearray([int(''.join(map(str, byte)), 2) for byte in bytes_list])

    # Convert bytes to the original UTF-8 encoded string
    return bytes_data.decode('utf-8', errors='ignore')

def main():
    input_file = 'input.txt'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.txt'  # Change to the desired encrypted output file path
    decrypted_output_file = 'decrypted.txt'  # Change to the desired decrypted output file path

    # Read the input from a file
    with open(input_file, 'r', encoding='utf-8') as file:
        input_string = file.read()

    # Convert the input string to the source block
    source_block = string_to_binary(input_string)

    size = len(source_block)  # Size of the source block in bits
    num_iterations = 2 ** math.ceil(math.log2(size))

    # Prompt for the block number
    block_number = int(input("Enter the block number for encryption: "))

    intermediate_blocks = generate_blocks(source_block, num_iterations, [])

    # Encryption
    start_time = time.time()
    encrypted_block, encryption_operations = encrypt(source_block, block_number, num_iterations)
    end_time = time.time()
    encryption_time = end_time - start_time

    # Encode the encrypted data as base64
    encrypted_base64 = base64.b64encode(bytes(encrypted_block)).decode('utf-8')

    # Write the encrypted base64 string to the encrypted output file
    with open(encrypted_output_file, 'w', encoding='utf-8') as encrypted_file:
        encrypted_file.write(encrypted_base64)

    # Decryption
    start_time = time.time()
    decrypted_blocks, decryption_operations = decrypt(encrypted_block, block_number, num_iterations)
    end_time = time.time()
    decryption_time = end_time - start_time

    # Convert the decrypted binary data to a string
    decrypted_string = binary_to_string(bytes(decrypted_blocks[-1]))

    # Write the decrypted string to the decrypted output file
    with open(decrypted_output_file, 'w', encoding='utf-8') as decrypted_file:
        decrypted_file.write(decrypted_string)

    print("Encryption and decryption completed.")
    print("Encrypted Base64 String:")
    print(encrypted_base64)
    print("Decrypted String:")
    print(decrypted_string)
    print(f'Size of Source Block: {size} bits')
    print(f'Encryption Time: {encryption_time:.4f} seconds')
    print(f'Decryption Time: {decryption_time:.4f} seconds')

    print(f'Number of XOR Operations (Encryption): {encryption_operations}')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')

if __name__ == "__main__":
    main()