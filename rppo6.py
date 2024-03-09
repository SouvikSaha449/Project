import math
import sys
import time
import numpy as np

# Set a new recursion depth limit
new_depth_limit = 100000  # Adjust to your desired limit
sys.setrecursionlimit(new_depth_limit)

class MemoizationDict:
    def __init__(self):
        self.memo_dict = {}

    def memoize(self, key, value):
        self.memo_dict[key] = value

    def get_memoized(self, key):
        return self.memo_dict.get(key, None)

def generate_block_recursive(block, remaining_iterations, memo_dict, intermediate_blocks):
    if remaining_iterations == 0:
        return
    memo_key = tuple(block)
    if (memo_result := memo_dict.get_memoized(memo_key)) is not None:
        new_block = memo_result
    else:
        new_block = np.bitwise_xor.accumulate(block)
        memo_dict.memoize(memo_key, new_block)

    intermediate_blocks.append(new_block)
    generate_block_recursive(new_block, remaining_iterations - 1, memo_dict, intermediate_blocks)

def generate_blocks(source_block, num_iterations):
    intermediate_blocks = [source_block.copy()]
    memo_dict = MemoizationDict()
    generate_block_recursive(source_block, num_iterations, memo_dict, intermediate_blocks)
    return intermediate_blocks[:num_iterations]

def encrypt(padded_source_block, block_index, num_iterations, encrypted_ascii_var):
    intermediate_blocks = generate_blocks(padded_source_block, num_iterations)
    encrypted_block = intermediate_blocks[block_index]
    encrypted_ascii_var += binary_to_string(encrypted_block)
    return encrypted_block, padded_source_block, encrypted_ascii_var

def decrypt(final_block, block_index, num_iterations, decrypted_ascii_var):
    if block_index >= len(final_block):
        return [], decrypted_ascii_var

    decrypted_blocks = []

    def generate_block_recursive(block, remaining_iterations):
        if remaining_iterations == 0:
            return
        new_block = np.bitwise_xor.accumulate(block)
        decrypted_blocks.append(new_block)
        generate_block_recursive(new_block, remaining_iterations - 1)

    generate_block_recursive(final_block, num_iterations - block_index)
    decrypted_ascii_var += binary_to_string(decrypted_blocks[-1])
    return decrypted_blocks, decrypted_ascii_var

def string_to_binary(string):
    return np.array([int(bit) for char in string for bit in format(ord(char), '08b')], dtype=int)

def binary_to_string(binary_values):
    binary_string = ''.join(map(str, binary_values))
    chars = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def main():
    input_file_path = 'Txt Files/input12.txt'
    source_string = read_file_content(input_file_path)

    source_block = string_to_binary(source_string)
    size = len(source_block)

    num_iterations = 2 ** math.ceil(math.log2(size))

    block_size = 8
    num_blocks = math.ceil(size / block_size)

    print(f'Source String: {source_string}')

    encrypted_ascii_var = ""
    decrypted_ascii_var = ""

    stop_number = int(input("Enter the stop number for encryption: "))

    for block_index in range(num_blocks):
        print(f'\nEnter the block number for encryption: {block_index + 1}')
        
        start_index = block_index * block_size
        end_index = (block_index + 1) * block_size
        current_block = source_block[start_index:end_index]

        print(f'Size of Padded Source Block: {num_iterations}')
        print(f'Source Block (Binary): {current_block}\n')

        intermediate_blocks = generate_blocks(current_block, num_iterations)

        for i, block in enumerate(intermediate_blocks[1:stop_number], start=1):
            print(f'Encrypted Block {i}: {block}\n')

        encrypted_block, _, encrypted_ascii_var = encrypt(current_block, stop_number, num_iterations, encrypted_ascii_var)
        encrypted_string = binary_to_string(encrypted_block)

        print(f'Encrypted Block (Binary): {encrypted_block}\n')
        print(f'Encrypted String: {encrypted_string}\n')

        decrypted_blocks, decrypted_ascii_var = decrypt(encrypted_block, stop_number, num_iterations, decrypted_ascii_var)

        for i, block in enumerate(decrypted_blocks):
            print(f'Decrypted Block {i + stop_number + 1}: {block}\n')

        decrypted_string = binary_to_string(decrypted_blocks[-1])
        print(f'Decrypted String: {decrypted_string}\n')

    print(f'Encrypted ASCII Version: {encrypted_ascii_var}\n')
    print(f'Decrypted ASCII Version: {decrypted_ascii_var}\n')

if __name__ == "__main__":
    main()
