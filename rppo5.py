import math
import time
import base64
import sys
import os
import numpy as np

new_depth_limit = 100000
sys.setrecursionlimit(new_depth_limit)


def generate_blocks(source_block, num_iterations, target_block_number, block_size=1024):
    intermediate_blocks = [source_block]
    intermediate_blocks_len = len(intermediate_blocks)

    def generate_block_recursive(block, remaining_iterations, operation_count=0):
        nonlocal intermediate_blocks, intermediate_blocks_len

        if remaining_iterations == 0 or intermediate_blocks_len > target_block_number:
            return operation_count

        xor_result = np.bitwise_xor.reduce(block, axis=0)
        block = np.bitwise_xor(block, xor_result)
        operation_count += len(block)

        intermediate_blocks.append(block)
        intermediate_blocks_len += 1
        return generate_block_recursive(block, remaining_iterations - 1, operation_count)

    chunk_size = min(block_size, num_iterations)
    for i in range(0, num_iterations, chunk_size):
        total_operations = generate_block_recursive(
            intermediate_blocks[-1], chunk_size)
        if intermediate_blocks_len > target_block_number:
            break

    return intermediate_blocks, total_operations


def calculate_accuracy(original_block, decrypted_block):
    correct_bits = np.sum(original_block == decrypted_block)
    total_bits = len(original_block)
    accuracy_percentage = (correct_bits / total_bits) * 100
    return accuracy_percentage


def calculate_hamming_distance(original_block, decrypted_block):
    hamming_distance = np.count_nonzero(original_block != decrypted_block)
    return hamming_distance


def encrypt(source_block, block_number, num_iterations):
    intermediate_blocks, total_operations = generate_blocks(
        source_block, num_iterations, block_number)
    if block_number < len(intermediate_blocks):
        return intermediate_blocks[block_number], total_operations
    else:
        return [], 0


def decrypt(final_block, block_number, num_iterations, block_size=1024):
    if block_number >= num_iterations:
        print("Decryption failed. Block number out of range.")
        return [], 0

    decrypted_blocks = [final_block]
    intermediate_blocks_len = len(decrypted_blocks)

    def generate_block_recursive(block, remaining_iterations, operation_count=0):
        nonlocal decrypted_blocks, intermediate_blocks_len

        if remaining_iterations == 0:
            return operation_count

        xor_result = np.bitwise_xor.reduce(block, axis=0)
        block = np.bitwise_xor(block, xor_result)
        operation_count += len(block)

        decrypted_blocks.append(block)
        intermediate_blocks_len += 1
        return generate_block_recursive(block, remaining_iterations - 1, operation_count)

    chunk_size = min(block_size, num_iterations - block_number)
    for i in range(0, num_iterations - block_number, chunk_size):
        total_operations = generate_block_recursive(
            decrypted_blocks[-1], chunk_size)
        if intermediate_blocks_len > block_number:
            break

    return decrypted_blocks, total_operations


def string_to_binary(string):
    return np.array([int(bit) for byte in string.encode('utf-8') for bit in f"{byte:08b}"], dtype=np.uint8)


def binary_to_string(binary_values):
    if len(binary_values) % 8 != 0:
        raise ValueError("Binary values length must be a multiple of 8 for proper decoding.")

    bytes_data = bytes(
        int(''.join(map(str, binary_values[i:i + 8])), 2) for i in range(0, len(binary_values), 8))
    return bytes_data.decode('utf-8', errors='ignore')


def main():
    input_file = 'input4.txt'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.txt'
    decrypted_output_file = 'decrypted.txt'

    # Calculate input file size
    input_file_size = os.path.getsize(input_file) / 1024  # Size in KB

    with open(input_file, 'r', encoding='utf-8') as file:
        input_string = file.read()

    source_block = np.array(list(string_to_binary(input_string)))

    # Calculate source block size
    source_block_size = source_block.nbytes / 1024  # Size in KB

    num_iterations = 2 ** math.ceil(math.log2(len(source_block)))

    block_number = int(input("Enter the block number for encryption: "))

    start_time = time.time()
    encrypted_block, encryption_operations = encrypt(
        source_block, block_number, num_iterations)
    end_time = time.time()
    encryption_time = end_time - start_time

    encrypted_base64 = base64.b64encode(
        bytes(encrypted_block)).decode('utf-8')

    with open(encrypted_output_file, 'w', encoding='utf-8') as encrypted_file:
        encrypted_file.write(encrypted_base64)

    # Print the encrypted binary block
    print(f'Encrypted Binary Block: {encrypted_block}')

    if block_number < len(encrypted_block):
        print("Block matched!")

    start_time = time.time()
    decrypted_blocks, decryption_operations = decrypt(
        encrypted_block, block_number, num_iterations)
    end_time = time.time()
    decryption_time = end_time - start_time

    accuracy_percentage = calculate_accuracy(source_block, decrypted_blocks[-1])

    with open(decrypted_output_file, 'w', encoding='utf-8') as decrypted_file:
        decrypted_file.write(binary_to_string(bytes(decrypted_blocks[-1])))

    print(f'Input File Size: {input_file_size:.2f} KB')
    print(f'Source Block Size: {source_block_size:.2f} KB')
    print(f'Encryption Time: {encryption_time:.4f} seconds')
    print(f'Decryption Time: {decryption_time:.4f} seconds')
    print(f'Number of XOR Operations (Encryption): {encryption_operations}')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')
    print(f'Accuracy Percentage: {accuracy_percentage:.2f}%')

    print("Encryption and decryption completed.")


if __name__ == "__main__":
    main()
