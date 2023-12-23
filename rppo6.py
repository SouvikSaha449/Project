import math
import time
import base64
import sys
import os
import numpy as np
from docx import Document  # Import the python-docx library
from scipy.stats import chisquare

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

def calculate_chi_square_and_df(observed_frequencies, expected_frequencies):
    if observed_frequencies.ndim == 1:
        observed_frequencies = observed_frequencies.reshape(1, -1)

    if expected_frequencies.ndim == 1:
        expected_frequencies = expected_frequencies.reshape(1, -1)

    if observed_frequencies.shape != expected_frequencies.shape:
        raise ValueError("Mismatched dimensions between observed and expected frequencies.")

    chi_square_value, p_value = chisquare(observed_frequencies, f_exp=expected_frequencies, axis=None)
    df = np.prod(observed_frequencies.shape) - 1
    return chi_square_value, df

def calculate_observed_frequencies(block):
    unique, counts = np.unique(block, return_counts=True)
    max_value = np.max(unique)
    
    observed_frequencies = np.zeros(max_value + 1)
    
    for value, count in zip(unique, counts):
        observed_frequencies[value] = count
    
    return np.array(observed_frequencies, dtype=np.float64)


def calculate_expected_frequencies(block):
    total_bits = len(block)
    expected_frequency_0 = total_bits / 2
    expected_frequency_1 = total_bits / 2
    return np.array([expected_frequency_0, expected_frequency_1], dtype=np.float64)

def calculate_accuracy(original_block, decrypted_block):
    correct_bits = np.sum(original_block == decrypted_block)
    total_bits = len(original_block)
    accuracy_percentage = (correct_bits / total_bits) * 100
    return accuracy_percentage

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
    remaining_bits = len(binary_values) % 8
    if remaining_bits != 0:
        # Pad with zeros to make the length a multiple of 8
        padding = np.zeros(8 - remaining_bits, dtype=np.uint8)
        binary_values = np.concatenate((np.atleast_1d(binary_values), padding))

    # Convert binary values to bytes
    byte_array = bytearray()
    for i in range(0, len(binary_values), 8):
        byte_str = ''.join(map(str, binary_values[i:i + 8]))
        try:
            byte = int(byte_str, 2)
            byte_array.append(byte)
        except ValueError:
            pass  # Ignore non-binary characters

    return bytes(byte_array)



def main():
    input_file = 'YourDLL.dll'  # Change to the actual input file path
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
    encrypted_block, encryption_operations = encrypt(
        source_block, block_number, num_iterations)
    end_time = time.time()
    encryption_time = end_time - start_time

    encrypted_base64 = base64.b64encode(encrypted_block.tobytes()).decode('utf-8')

    write_file(encrypted_output_file, base64.b64decode(encrypted_base64))

    if block_number < len(encrypted_block):
        print("Block matched!")

        print(f'Encryption Time: {encryption_time:.4f} seconds')
        print(f'Number of XOR Operations (Encryption): {encryption_operations}')

    start_time = time.time()
    decrypted_blocks, decryption_operations = decrypt(
        encrypted_block, block_number, num_iterations)
    end_time = time.time()
    decryption_time = end_time - start_time

    accuracy_percentage = calculate_accuracy(source_block, decrypted_blocks[-1])

    print(f'Accuracy Percentage: {accuracy_percentage:.2f}%')

    decrypted_file_content = binary_to_string(bytes(decrypted_blocks[-1]))
    write_file(decrypted_output_file, decrypted_file_content)

    print(f'Decryption Time: {decryption_time:.4f} seconds')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')

    expected_frequencies_source = calculate_expected_frequencies(source_block)
    observed_frequencies_source = calculate_observed_frequencies(source_block)
    chi_square_source, df_source = calculate_chi_square_and_df(observed_frequencies_source, expected_frequencies_source)

    print(f'Chi-square value for the source block: {chi_square_source}')
    print(f'Degrees of Freedom for the source block: {df_source}')

    expected_frequencies_encrypted = calculate_expected_frequencies(encrypted_block)
    observed_frequencies_encrypted = calculate_observed_frequencies(encrypted_block)
    chi_square_encrypted, df_encrypted = calculate_chi_square_and_df(observed_frequencies_encrypted, expected_frequencies_encrypted)

    print(f'Chi-square value for the encrypted block: {chi_square_encrypted}')
    print(f'Degrees of Freedom for the encrypted block: {df_encrypted}')

    expected_frequencies_decrypted = calculate_expected_frequencies(decrypted_blocks[-1])
    observed_frequencies_decrypted = calculate_observed_frequencies(decrypted_blocks[-1])
    chi_square_decrypted, df_decrypted = calculate_chi_square_and_df(observed_frequencies_decrypted, expected_frequencies_decrypted)

    print(f'Chi-square value for the decrypted block: {chi_square_decrypted}')
    print(f'Degrees of Freedom for the decrypted block: {df_decrypted}')

    print()
    print("Final Results")
    print("------------------------")
    print(f'Input File: {input_file}')
    print(f'Input File Size: {input_file_size} bytes')
    print(f'Encryption Time: {encryption_time:.4f} seconds')
    print(f'Decryption Time: {decryption_time:.4f} seconds')
    print(f'Number of XOR Operations (Encryption): {encryption_operations}')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')
    print(f'Accuracy Percentage: {accuracy_percentage:.2f}%')
    print(f'Chi-square value for the source block: {chi_square_source}')
    print(f'Degrees of Freedom for the source block: {df_source}')
    print(f'Chi-square value for the encrypted block: {chi_square_encrypted}')
    print(f'Degrees of Freedom for the encrypted block: {df_encrypted}')
    print(f'Chi-square value for the decrypted block: {chi_square_decrypted}')
    print(f'Degrees of Freedom for the decrypted block: {df_decrypted}')

    print("Encryption, decryption, and Chi-square calculations completed.\n")

if __name__ == "__main__":
    main()