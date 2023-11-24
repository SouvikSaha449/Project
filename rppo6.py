import math
import time
import base64
import sys
import numpy as np

new_depth_limit = 100000
sys.setrecursionlimit(new_depth_limit)

def generate_blocks(source_block, num_iterations, target_block_number):
    intermediate_blocks = np.empty((num_iterations, len(source_block)), dtype=int)
    intermediate_blocks[0] = source_block

    def generate_block_recursive(i, remaining_iterations, operation_count=0):
        nonlocal intermediate_blocks

        if i == num_iterations or i > target_block_number:
            return operation_count

        xor_result = np.bitwise_xor.reduce(intermediate_blocks[i - 1], axis=0)
        intermediate_blocks[i] = np.bitwise_xor(intermediate_blocks[i - 1], xor_result)
        operation_count += len(intermediate_blocks[i])

        return generate_block_recursive(i + 1, remaining_iterations - 1, operation_count)

    total_operations = generate_block_recursive(1, num_iterations)
    return intermediate_blocks[:target_block_number + 1], total_operations

def encrypt(source_block, block_number, num_iterations):
    intermediate_blocks, total_operations = generate_blocks(source_block, num_iterations, block_number)
    if block_number < len(intermediate_blocks):
        return intermediate_blocks[block_number], total_operations
    else:
        return np.empty((0, len(source_block)), dtype=int), 0

def decrypt(final_block, block_number, num_iterations):
    if block_number >= len(final_block):
        return np.empty((0, final_block.shape[1]), dtype=int), 0

    decrypted_blocks = np.empty((num_iterations - block_number, final_block.shape[1]), dtype=int)
    decrypted_blocks[0] = final_block[block_number]

    def generate_block_recursive(i, remaining_iterations, operation_count=0):
        nonlocal decrypted_blocks

        if i == num_iterations - block_number:
            return operation_count

        xor_result = np.bitwise_xor.reduce(decrypted_blocks[i - 1], axis=0)
        decrypted_blocks[i] = np.bitwise_xor(decrypted_blocks[i - 1], xor_result)
        operation_count += len(decrypted_blocks[i])

        return generate_block_recursive(i + 1, remaining_iterations - 1, operation_count)

    total_operations = generate_block_recursive(1, num_iterations - block_number)
    return decrypted_blocks[:num_iterations - block_number], total_operations

def string_to_binary(string):
    return np.array([int(bit) for byte in string.encode('utf-8') for bit in f"{byte:08b}"])

def binary_to_string(binary_values):
    if len(binary_values) % 8 != 0:
        raise ValueError("Binary values length must be a multiple of 8 for proper decoding.")

    bytes_data = bytes(int(''.join(map(str, binary_values[i:i+8])), 2) for i in range(0, len(binary_values), 8))
    return bytes_data.decode('utf-8', errors='ignore')

def main():
    input_file = 'input4.txt'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.txt'  # Change to the desired encrypted output file path
    decrypted_output_file = 'decrypted.txt'  # Change to the desired decrypted output file path

    # Read the input from a file
    with open(input_file, 'r', encoding='utf-8') as file:
        input_string = file.read()

    # Convert the input string to the source block
    source_block = np.array(list(string_to_binary(input_string)))

    size = len(source_block)  # Size of the source block in bits
    num_iterations = 2 ** math.ceil(math.log2(size))

    # Prompt for the block number
    block_number = int(input("Enter the block number for encryption: "))

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

    print(f'Size of Source Block: {size} bits')
    print(f'Encryption Time: {encryption_time:.4f} seconds')
    print(f'Decryption Time: {decryption_time:.4f} seconds')

    print(f'Number of XOR Operations (Encryption): {encryption_operations}')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')

    print("Encryption and decryption completed.")

if __name__ == "__main__":
    main()
