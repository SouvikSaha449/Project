import math
import time
import base64
import sys
import os
import numpy as np
from functools import lru_cache

new_depth_limit = 100000
sys.setrecursionlimit(new_depth_limit)

def read_file(file_path):
    _, file_extension = os.path.splitext(file_path.lower())
    supported_extensions = ['.cpp', '.sys', '.exe', '.dll', '.com']
    if file_extension in supported_extensions:
        with open(file_path, 'rb') as file:
            return file.read()
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def write_file(file_path, content):
    _, file_extension = os.path.splitext(file_path.lower())
    supported_extensions = ['.cpp', '.sys', '.exe', '.dll', '.com']
    if file_extension in supported_extensions:
        with open(file_path, 'wb') as file:
            file.write(content)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def generate_blocks(source_block, num_iterations, target_block_number, block_size=1024):
    intermediate_blocks = [source_block]
    intermediate_blocks_len = len(intermediate_blocks)

    def generate_block_recursive(block, remaining_iterations, operation_count=0):
        nonlocal intermediate_blocks, intermediate_blocks_len

        if remaining_iterations == 0 or intermediate_blocks_len > target_block_number:
            return operation_count

        new_block = np.zeros_like(block)
        xor_result = 0

        for j in range(len(block)):
            xor_result ^= block[j]
            new_block[j] = xor_result

        intermediate_blocks.append(new_block)
        intermediate_blocks_len += 1
        return generate_block_recursive(new_block, remaining_iterations - 1, operation_count + len(new_block))

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

def encrypt(source_block, block_number, num_iterations, block_size=1024):
    intermediate_blocks, total_operations = generate_blocks(
        source_block, num_iterations, block_number, block_size)
    if block_number < len(intermediate_blocks):
        return intermediate_blocks[block_number], total_operations
    else:
        return [], 0
    
def detect_changes(source_block, encrypted_block):
    source_binary = ''.join(map(str, source_block))
    encrypted_binary = ''.join(map(str, encrypted_block))

    changes = []
    for i, (src_bit, enc_bit) in enumerate(zip(source_binary, encrypted_binary)):
        if src_bit != enc_bit:
            changes.append(i)

    return changes

def decrypt(final_block, block_number, num_iterations, block_size=1024):
    if block_number >= num_iterations:
        print("Decryption failed. Block number out of range.")
        return None, 0

    decrypted_block = final_block.copy()

    def generate_block_recursive(block, remaining_iterations, operation_count=0):
        nonlocal decrypted_block

        if remaining_iterations == 0:
            return operation_count

        new_block = np.zeros_like(block)
        xor_result = 0

        for j in reversed(range(len(block))):
            new_block[j] = xor_result
            xor_result ^= block[j]

        decrypted_block = np.bitwise_xor(decrypted_block, new_block)  # XOR with the new_block
        return generate_block_recursive(new_block, remaining_iterations - 1, operation_count + len(new_block))

    chunk_size = min(block_size, num_iterations - block_number)
    total_operations = generate_block_recursive(final_block, chunk_size)

    return decrypted_block, total_operations

def string_to_binary(string):
    return np.array([int(bit) for byte in string.encode('utf-8') for bit in f"{byte:08b}"], dtype=np.uint8)

def binary_to_string(binary_values):
    if len(binary_values) % 8 != 0:
        raise ValueError("Binary values length must be a multiple of 8 for proper decoding.")

    bytes_data = bytes(
        int(''.join(map(str, binary_values[i:i + 8])), 2) for i in range(0, len(binary_values), 8))
    return bytes_data.decode('utf-8', errors='ignore')

def main():
    input_file = 'YourDll.dll'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.dll'
    decrypted_output_file = 'decrypted.dll'

    print(f'Input File: {input_file}')

    _, input_file_extension = os.path.splitext(input_file.lower())
    is_docx = input_file_extension == '.docx'

    # Print the size of the input file
    input_file_size = os.path.getsize(input_file)
    print(f'Input File Size: {input_file_size} bytes')

    input_file_content = read_file(input_file)

    source_block = np.frombuffer(input_file_content, dtype=np.uint8)

    num_iterations = 2 ** math.ceil(math.log2(len(source_block)))

    block_number = int(input("Enter the block number for encryption: "))

    start_time = time.time()
    encrypted_block, encryption_operations = encrypt(source_block, block_number, num_iterations)
    end_time = time.time()
    encryption_time = end_time - start_time

    # Calculate the size of the encrypted block in bits
    encrypted_block_size_bits = len(encrypted_block) * 8

    encrypted_base64 = base64.b64encode(np.array(list(encrypted_block)).tobytes()).decode('utf-8')

    write_file(encrypted_output_file, base64.b64decode(encrypted_base64))

    if block_number < len(encrypted_block):
        print("Block matched!")

        print(f'Encryption Time: {encryption_time:.4f} seconds')
        changes = detect_changes(source_block, encrypted_block)
        print(f'Changes in Position: {changes}')
        print(f'Number of XOR Operations (Encryption): {encryption_operations}')
        print(f'Size of Encrypted Block: {encrypted_block_size_bits} bits')  # Add this line

    start_time = time.time()
    decrypted_blocks, decryption_operations = decrypt(encrypted_block, block_number, num_iterations)
    end_time = time.time()
    decryption_time = end_time - start_time

    accuracy_percentage = calculate_accuracy(source_block, decrypted_blocks[0])  # Use the source_block for accuracy calculation

    print(f'Accuracy Percentage: {accuracy_percentage:.2f}%')

    decrypted_file_content = decrypted_blocks.tobytes()
    write_file(decrypted_output_file, decrypted_file_content)
    print(f'Decryption Time: {decryption_time:.4f} seconds')
    print()
    print("Final Results")
    print("------------------------")
    print(f'Input File: {input_file}')
    print(f'Input File Size: {input_file_size} bytes')
    print(f'Encryption Time: {encryption_time:.4f} seconds')
    print(f'Decryption Time: {decryption_time:.4f} seconds')
    print(f'Accuracy Percentage: {accuracy_percentage:.2f}%')
    print("Encryption and decryption completed.\n")

if __name__ == "__main__":
    main()
