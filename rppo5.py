import os
import sys
import time


# Set a new recursion depth limit
new_depth_limit = 100000  # Adjust to your desired limit
sys.setrecursionlimit(new_depth_limit)


def generate_blocks(source_block, num_iterations, encryption_number):
    intermediate_blocks = []
    intermediate_blocks.append(source_block.copy())

    def generate_block_recursive(block, remaining_iterations):
        if remaining_iterations == 0 or len(intermediate_blocks) > encryption_number:
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


def pad_source_block(source_block, num_iterations):
    size = len(source_block)
    padded_size = num_iterations
    if size < padded_size:
        # Calculate the number of bits to pad
        num_bits_to_pad = padded_size - size
        # Pad the source block at the beginning with bits 0
        padded_block = [0] * num_bits_to_pad + source_block
    else:
        padded_block = source_block.copy()
    return padded_block, padded_size  # Return the padded block and its size


def encrypt(padded_source_block, encryption_number, num_iterations):
    intermediate_blocks = generate_blocks(padded_source_block, num_iterations, encryption_number)
    return intermediate_blocks[min(encryption_number, len(intermediate_blocks) - 1)]


def decrypt(final_block, encryption_number, num_iterations):
    if encryption_number >= len(final_block):
        return [], 0

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

    generate_block_recursive(final_block, num_iterations - encryption_number)
    return decrypted_blocks


def split_into_blocks(source_string, block_size):
    # Split the source string into blocks of fixed size
    blocks = [source_string[i:i + block_size] for i in range(0, len(source_string), block_size)]
    # If the last block is less than the block size, pad it with zeros
    if len(blocks[-1]) < block_size:
        blocks[-1] += '0' * (block_size - len(blocks[-1]))
    elif len(blocks[-1]) > block_size:
        blocks[-1] = blocks[-1][:block_size]  # Trim the last block if it's longer than the block size
    return blocks


def string_to_binary(string):
    binary_values = []
    for char in string:
        # Convert each character to its ASCII value and then to 8-bit binary representation
        ascii_value = ord(char)
        binary_value = format(ascii_value, '08b')  # Convert ASCII to 8-bit binary
        binary_values.extend([int(bit) for bit in binary_value])
    return binary_values


def binary_to_string(binary_values):
    binary_string = ''.join(map(str, binary_values))
    chars = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])


def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def read_file(file_path):
    _, file_extension = os.path.splitext(file_path.lower())
    supported_extensions = ['.cpp', '.sys', '.exe', '.dll', '.com', '.txt','.pdf']
    if file_extension in supported_extensions:
        with open(file_path, 'rb') as file:
            return file.read()
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def write_file(file_path, content):
    _, file_extension = os.path.splitext(file_path.lower())
    supported_extensions = ['.cpp', '.sys', '.exe', '.dll', '.com', '.txt','.pdf']
    if file_extension in supported_extensions:
        with open(file_path, 'wb') as file:
            file.write(content)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
def calculate_accuracy(list1, list2):
    if len(list1) != len(list2):
        return "Lists are not the same size"
    
    num_elements = len(list1)
    num_same = sum(1 for i in range(num_elements) if list1[i] == list2[i])
    accuracy = (num_same / num_elements) * 100
    return accuracy

def main():
    
    input_file_path = 'Txt Files/input.txt'  # Change to the actual input file path
    input_file_size = os.path.getsize(input_file_path)
    print(f'Input File Size: {input_file_size} bytes')
    source_string = read_file_content(input_file_path)
    

    source_blocks = [string_to_binary(source_string[i:i + 2]) for i in range(0, len(source_string), 2)]
    # print(source_blocks)
    # print([len(block) for block in source_blocks])
    max_sub_source_block_size = max(source_blocks, key=len)
    # if len(source_blocks) > 16:
    #      sum+=1
    # print(f"{sum} blocks are over 16bits")
    print(f'maximum block number of encryption: {len(max_sub_source_block_size)}\n')

    encryption_number = int(input("Enter the block number of encryption: "))

    encrypted_strings = []
    decrypted_strings = []
    total_encryption_time = 0
    total_decryption_time = 0

    if encryption_number >= len(max_sub_source_block_size):
        print("Encryption not possible")
    else:
        for block_number, source_block in enumerate(source_blocks):
            num_iterations = len(max_sub_source_block_size)

            padded_source_block, _ = pad_source_block(source_block, num_iterations)

            intermediate_blocks = generate_blocks(padded_source_block, num_iterations, encryption_number)

            # Check if the length of the block exceeds 16 bits and print it if it does
            
            # if len(padded_source_block) > 16:
            #     sum+=1
            # print(f"{sum} blocks are over 16bits")


            """print(f'Block {block_number + 1}:')
            print(f'Source String: {binary_to_string(padded_source_block)}')
            print(f'Source Block (Binary): {source_block}\n')"""

            # Encryption Time Calculation
            start_time_encryption = time.time()
            """for i, block in enumerate(intermediate_blocks[1:], start=1):
                print(f'Encrypted Block {i}: {block}\n')"""

            encrypted_block = encrypt(padded_source_block, encryption_number, num_iterations)

            encrypted_string = binary_to_string(encrypted_block)

            encrypted_strings.append(encrypted_string)
            end_time_encryption = time.time()
            total_encryption_time += (end_time_encryption - start_time_encryption)

            """print(f'Encrypted Block (Binary): {encrypted_block}\n')
            print(f'Encrypted String: {encrypted_string}\n')"""

            # Decryption Time Calculation
            start_time_decryption = time.time()
            decrypted_blocks = decrypt(encrypted_block, encryption_number, num_iterations)

            # for i, block in enumerate(decrypted_blocks):
            #     decrypt_itr_number = i + encryption_number + 1
            #     print(f'Decrypted Block {decrypt_itr_number}: {block}\n')
            # print(decrypted_blocks)
            decrypted_string = binary_to_string(decrypted_blocks[-1])
            decrypted_strings.append(decrypted_string)
            end_time_decryption = time.time()
            total_decryption_time += (end_time_decryption - start_time_decryption)

            # Accuracy Calculation
            # accuracy = calculate_accuracy(padded_source_block, decrypted_blocks)
            # print(accuracy)


            """print(f'Decrypted String: {decrypted_string}\n')"""

        """print("Final Encrypted String:")"""
        final_encrypted_string = ''.join(encrypted_strings)
        encrypted_content = final_encrypted_string.encode('utf-8')  # Replace encrypted_ascii_var with your encrypted content
        write_file('encrypted.txt', encrypted_content)

        """print("\nFinal Decrypted String:")"""
        final_decrypted_string = ''.join(decrypted_strings)
        decrypted_content = final_decrypted_string.encode('utf-8')  # Replace decrypted_ascii_var with your decrypted content
        write_file('decrypted.txt', decrypted_content)

        print("\nTotal Encryption Time:", total_encryption_time, "seconds")
        print("Total Decryption Time:", total_decryption_time, "seconds")
        
if __name__ == "__main__":
    main()