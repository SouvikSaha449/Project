import math
import time
import base64
import sys
import os
import numpy as np
from docx import Document
from scipy.stats import chi2_contingency
import binascii  # Add this import statement

new_depth_limit = 100000
sys.setrecursionlimit(new_depth_limit)

def read_file(file_path):
    _, file_extension = os.path.splitext(file_path.lower())
    supported_extensions = ['.cpp', '.sys', '.exe', '.dll', '.com','.docx','.txt']
    if file_extension in supported_extensions:
        with open(file_path, 'rb') as file:
            return file.read()
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def write_file(file_path, content):
    _, file_extension = os.path.splitext(file_path.lower())
    supported_extensions = ['.cpp', '.sys', '.exe', '.dll', '.com','.docx','.txt']
    if file_extension in supported_extensions:
        try:
            with open(file_path, 'wb') as file:
                file.write(content)
        except binascii.Error:
            print("Error: Incorrect padding during base64 decoding.")
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

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

# def detect_changes(source_block, encrypted_block):
#     source_binary = ''.join(map(str, source_block))
#     encrypted_binary = ''.join(map(str, encrypted_block))
#     changes = []
#     for i, (src_bit, enc_bit) in enumerate(zip(source_binary, encrypted_binary)):
#         if src_bit != enc_bit:
#             changes.append(i)
#     return changes

def encrypt(source_block, block_number, num_iterations):
    intermediate_blocks, total_operations = generate_blocks(
        source_block, num_iterations, block_number)
    if block_number < len(intermediate_blocks):
        return intermediate_blocks[block_number], total_operations
    else:
        return [], 0

def calculate_accuracy(original_block, decrypted_block):
    original_block = np.pad(original_block, (0, len(decrypted_block) - len(original_block)))  # Add padding to match shapes
    correct_bits = np.sum(original_block == decrypted_block)
    total_bits = len(original_block)
    accuracy_percentage = (correct_bits / total_bits) * 100
    return accuracy_percentage

def calculate_hamming_distance(original_block, decrypted_block):
    hamming_distance = np.count_nonzero(original_block != decrypted_block)
    return hamming_distance

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

def chi_square_test(source_block, encrypted_block):
    source_counts = [np.count_nonzero(source_block == 0), np.count_nonzero(source_block == 1)]
    encrypted_counts = [np.count_nonzero(encrypted_block == 0), np.count_nonzero(encrypted_block == 1)]

    epsilon = 1e-10
    source_counts = np.array(source_counts) + epsilon
    encrypted_counts = np.array(encrypted_counts) + epsilon

    contingency_table = np.array([source_counts, encrypted_counts])

    degrees_of_freedom = (contingency_table.shape[0] - 1) * (contingency_table.shape[1] - 1)

    chi2, p, _, _ = chi2_contingency(contingency_table)

    return chi2, p, degrees_of_freedom

def string_to_binary(data):
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))

def binary_to_string(binary_values):
    if len(binary_values) % 8 != 0:
        raise ValueError("Binary values length must be a multiple of 8 for proper decoding.")
    bytes_data = bytes(
        int(''.join(map(str, binary_values[i:i + 8])), 2) for i in range(0, len(binary_values), 8))
    return bytes_data.decode('utf-8', errors='ignore')

def main():
    input_file = 'input10.docx'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.docx'
    decrypted_output_file = 'decrypted.docx'

    print(f'Input File: {input_file}')

    input_file_size = os.path.getsize(input_file)
    print(f'Input File Size: {input_file_size} bytes')

    with open(input_file, 'r', encoding='utf-8') as file:
        input_file_content = read_file(input_file)

    source_block = np.array(list(string_to_binary(input_file_content)))

    _, input_file_extension = os.path.splitext(input_file.lower())
    is_docx = input_file_extension == '.docx'

    source_block = np.array(list(string_to_binary(input_file_content)))

    num_iterations = 2 ** math.ceil(math.log2(len(source_block)))

    block_number = int(input("Enter the block number for encryption: "))
    start_time = time.time()
    encrypted_block, encryption_operations = encrypt(
        source_block, block_number, num_iterations)
    end_time = time.time()
    encryption_time = end_time - start_time

    encrypted_base64 = base64.b64encode(bytes(encrypted_block)).decode('utf-8')

    with open(encrypted_output_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_block)

    if block_number < len(encrypted_block):
        print("Block matched!")
        print(f'Encryption Time: {encryption_time:.4f} seconds')
        print(f'Number of XOR Operations (Encryption): {encryption_operations}')
        # changes = detect_changes(source_block, encrypted_block)
        # print(f'Changes in Position: {changes}')
        chi2, p, degrees_of_freedom = chi_square_test(source_block, encrypted_block)
        print(f'Chi-square value: {chi2:.4f}')
        print(f'Degrees of Freedom: {degrees_of_freedom}')

    start_time = time.time()
    decrypted_blocks, decryption_operations = decrypt(
        encrypted_block, block_number, num_iterations)
    end_time = time.time()
    decryption_time = end_time - start_time
    accuracy_percentage = calculate_accuracy(source_block, decrypted_blocks[-1])

    print(f'Accuracy Percentage: {accuracy_percentage:.2f}%')

    with open(decrypted_output_file, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_blocks[-1])
    
    print(f'Decryption Time: {decryption_time:.4f} seconds')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')
    print()

    print("Final Results")
    print("------------------------")

    print(f'Input File: {input_file}')
    print(f'Input File Size: {input_file_size:.2f} bytes')
    print(f'Encryption Time: {encryption_time:.4f} seconds')
    print(f'Decryption Time: {decryption_time:.4f} seconds')
    print(f'Number of XOR Operations (Encryption): {encryption_operations}')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')
    print(f'Accuracy Percentage: {accuracy_percentage:.2f}%')
    print(f'Chi-square value: {chi2:.4f}')
    print(f'Degrees of Freedom: {degrees_of_freedom}')
    print("Encryption and decryption completed.\n")

if __name__ == "__main__":
    main()
