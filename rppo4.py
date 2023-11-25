import time
import base64
import numpy as np

def generate_blocks(source_block, num_iterations, target_block_number):
    intermediate_blocks = [source_block]
    intermediate_blocks_len = 1

    for _ in range(num_iterations):
        xor_result = np.bitwise_xor.reduce(intermediate_blocks[-1], axis=0)
        block = np.bitwise_xor(intermediate_blocks[-1], xor_result)
        intermediate_blocks.append(block)
        intermediate_blocks_len += 1

        if intermediate_blocks_len > target_block_number:
            break

    total_operations = num_iterations * np.int64(len(source_block))
    return intermediate_blocks, total_operations

def encrypt(source_block, block_number, num_iterations):
    intermediate_blocks, total_operations = generate_blocks(source_block, num_iterations, block_number)
    if block_number < len(intermediate_blocks):
        return intermediate_blocks[block_number], total_operations
    else:
        return [], np.int64(0)

def decrypt(final_block, block_number, num_iterations):
    decrypted_blocks = [final_block]

    for _ in range(num_iterations - block_number):
        xor_result = np.bitwise_xor.reduce(decrypted_blocks[-1], axis=0)
        block = np.bitwise_xor(decrypted_blocks[-1], xor_result)
        decrypted_blocks.append(block)

    total_operations = np.int64(num_iterations - block_number) * np.int64(len(final_block))
    return decrypted_blocks, total_operations

def string_to_binary(string):
    return np.array([int(bit) for byte in string.encode('utf-8') for bit in f"{byte:08b}"])

def binary_to_string(binary_values):
    if len(binary_values) % 8 != 0:
        raise ValueError("Binary values length must be a multiple of 8 for proper decoding.")

    bytes_data = bytes(int(''.join(map(str, binary_values[i:i+8])), 2) for i in range(0, len(binary_values), 8))
    return bytes_data.decode('utf-8', errors='ignore')

def main():
    input_file = 'input5.txt'  # Change to the actual input file path
    encrypted_output_file = 'encrypted.txt'  # Change to the desired encrypted output file path
    decrypted_output_file = 'decrypted.txt'  # Change to the desired decrypted output file path

    # Read the input from a file
    with open(input_file, 'r', encoding='utf-8') as file:
        input_string = file.read()

    # Convert the input string to the source block
    source_block = string_to_binary(input_string)

    size = len(source_block)  # Size of the source block in bits
    num_iterations = 2 ** np.ceil(np.log2(size)).astype(int)

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

    # Print additional information
    total_blocks_generated = len(encrypted_block)
    print(f'Size of Source Block: {size} bits')
    print(f'Total Blocks Generated: {total_blocks_generated}')
    print(f'Encryption Time: {encryption_time:.4f} seconds')
    print(f'Decryption Time: {decryption_time:.4f} seconds')

    print(f'Number of XOR Operations (Encryption): {encryption_operations}')
    print(f'Number of XOR Operations (Decryption): {decryption_operations}')

    print("Encryption and decryption completed.")

if __name__ == "__main__":
    main()

