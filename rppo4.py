import math
import time
import base64
import sys

new_depth_limit = 100000
sys.setrecursionlimit(new_depth_limit)

def generate_blocks(source_block, num_iterations, target_block_number, intermediate_blocks=None):
    if intermediate_blocks is None:
        intermediate_blocks = [source_block]

    def generate_block_recursive(block, remaining_iterations, operation_count=0):
        nonlocal intermediate_blocks

        if remaining_iterations == 0 or len(intermediate_blocks) > target_block_number:
            return operation_count

        xor_result = 0
        for i in range(len(block)):
            xor_result ^= block[i]
            operation_count += 1
            block[i] = xor_result

        intermediate_blocks.append(block)
        revert_changes(block)  # Revert changes to reuse the block instance
        return generate_block_recursive(block, remaining_iterations - 1, operation_count)

    total_operations = generate_block_recursive(source_block.copy(), num_iterations)
    return intermediate_blocks, total_operations

def revert_changes(block):
    xor_result = 0
    for i in range(len(block) - 1, 0, -1):
        xor_result ^= block[i]
        block[i] = xor_result

def encrypt(source_block, block_number, num_iterations):
    intermediate_blocks, total_operations = generate_blocks(source_block, num_iterations, block_number)
    if block_number < len(intermediate_blocks):
        return intermediate_blocks[block_number], total_operations
    else:
        return [], 0

def decrypt(final_block, block_number, num_iterations):
    if block_number >= len(final_block):
        return [], 0

    decrypted_blocks = [final_block]

    def generate_block_recursive(block, remaining_iterations, operation_count=0):
        nonlocal decrypted_blocks

        if remaining_iterations == 0:
            return operation_count

        xor_result = 0
        for i in range(len(block)):
            xor_result ^= block[i]
            operation_count += 1
            block[i] = xor_result

        decrypted_blocks.append(block)
        revert_changes(block)  # Revert changes to reuse the block instance
        return generate_block_recursive(block, remaining_iterations - 1, operation_count)

    total_operations = generate_block_recursive(final_block.copy(), num_iterations - block_number)
    return decrypted_blocks, total_operations

def string_to_binary(string):
    return (int(bit) for byte in string.encode('utf-8') for bit in f"{byte:08b}")

def binary_to_string(binary_values):
    if len(binary_values) % 8 != 0:
        raise ValueError("Binary values length must be a multiple of 8 for proper decoding.")

    bytes_data = bytes(int(''.join(map(str, binary_values[i:i+8])), 2) for i in range(0, len(binary_values), 8))
    return bytes_data.decode('utf-8', errors='ignore')

def main():
    input_file = 'input2.txt'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.txt'  # Change to the desired encrypted output file path
    decrypted_output_file = 'decrypted.txt'  # Change to the desired decrypted output file path

    # Read the input from a file
    with open(input_file, 'r', encoding='utf-8') as file:
        input_string = file.read()

    # Convert the input string to the source block
    source_block = list(string_to_binary(input_string))

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
