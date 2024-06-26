import os
import sys
import time
import random
import math
from collections import Counter


# Set a new recursion depth limit
new_depth_limit = 100000  # Adjust to your desired limit
sys.setrecursionlimit(new_depth_limit)
encryption_xor_count = 0
decryption_xor_count = 0
accuracy = 0


def generate_blocks(source_block, num_iterations, encryption_number):
    global encryption_xor_count
    intermediate_blocks = []
    intermediate_blocks.append(source_block.copy())

    def generate_block_recursive(block, remaining_iterations):
        global encryption_xor_count
        if remaining_iterations == 0 or len(intermediate_blocks) > encryption_number:
            return
        new_block = block.copy()
        for j in range(len(block)):
            xor_result = 0
            for k in range(j + 1):
                xor_result ^= block[k]
                encryption_xor_count += 1  # Count XOR operation
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
    global decryption_xor_count
    if encryption_number >= len(final_block):
        return [], 0

    decrypted_blocks = []

    def generate_block_recursive(block, remaining_iterations):
        global decryption_xor_count
        if remaining_iterations == 0:
            return
        new_block = block.copy()
        for j in range(len(block)):
            xor_result = 0
            for k in range(j + 1):
                xor_result ^= block[k]
                decryption_xor_count += 1  # Count XOR operation
            new_block[j] = xor_result
        decrypted_blocks.append(new_block)
        generate_block_recursive(new_block, remaining_iterations - 1)

    generate_block_recursive(final_block, num_iterations - encryption_number)
    return decrypted_blocks


def string_to_binary(string):
    binary_values = []
    for char in string:
        ascii_value = ord(char)
        binary_value = format(ascii_value, '08b')  # Convert ASCII to 8-bit binary
        binary_values.extend([int(bit) for bit in binary_value])
    return binary_values


def binary_to_string(binary_values):
    binary_string = ''.join(map(str, binary_values))
    chars = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])


def read_file_content(file_path):
    valid_extensions = {'.sys', '.exe', '.cpp', '.com', '.dll','.txt'}
    file_extension = os.path.splitext(file_path)[1]
    if file_extension.lower() in valid_extensions:
        encodings = ['utf-8', 'latin-1']  # Add more encodings if needed
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                return content
            except UnicodeDecodeError:
                pass
        print("Failed to read the file. Unable to decode using any supported encoding.")
        return None
    else:
        print("Unsupported file type. Only .sys, .exe, .cpp, .com, and .docx files are supported.")
        return None

def write_file(file_path, content):
    _, file_extension = os.path.splitext(file_path.lower())
    supported_extensions = ['.cpp', '.sys', '.exe', '.com', '.txt', '.dll']
    if file_extension in supported_extensions:
        if file_extension == '.txt':
            # For .txt files, writing content in text mode
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(content.decode('utf-8'))
        else:
            # For other supported extensions, writing content in binary mode
            with open(file_path, 'ab') as file:
                file.write(content)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
def calculate_accuracy(list1, list2):
    if len(list1) != len(list2):
        return 0
    
    num_elements = len(list1)
    num_same = sum(1 for i in range(num_elements) if list1[i] == list2[i])
    accuracy = (num_same / num_elements) * 100
    return accuracy

def average_accuracy(source_blocks, decrypted_block_lists):
    total_accuracy = 0
    num_sublists = len(source_blocks)
    
    for sub_list in source_blocks:
        accuracy = calculate_accuracy(sub_list, decrypted_block_lists[source_blocks.index(sub_list)])
        total_accuracy += accuracy
    
    if num_sublists == 0:
        return 0  # to avoid division by zero error
    
    return total_accuracy / num_sublists


def count_characters(source_string):
    character_count = Counter(source_string)
    return character_count


def tabulate_character_counts(character_count_source, character_count_encrypted):
    total_source_count = 0
    total_encrypted_count = 0
    total_total_count = 0
    chi_period = 0
    all_chars = set(character_count_source.keys()) | set(character_count_encrypted.keys())
    total_unique_chars = len(all_chars)
    print("Character\tSource\t\tEncrypted\tTotal")
    print("-------------------------------------------")
    for char in sorted(all_chars):
            count_source = character_count_source.get(char, 0)
            total_source_count += count_source
            count_encrypted = character_count_encrypted.get(char, 0)
            total_encrypted_count += count_encrypted
            add = count_source + count_encrypted
            total_total_count += add
            if char.isprintable():
                print(f"{char}\t\t{count_source}\t\t{count_encrypted}\t\t{add}")
            else:
                print(f"U+{ord(char):04X}\t\t{count_source}\t\t{count_encrypted}\t\t{add}")

    for char in sorted(all_chars):
        count_source = character_count_source.get(char, 0)
        count_encrypted = character_count_encrypted.get(char, 0)
        add = count_source + count_encrypted 
        club_total_s_total_e = (total_source_count + total_encrypted_count) / 2
        chi_period += chi_period_calculate(count_source, count_encrypted, add, club_total_s_total_e, total_total_count)

    degree_of_freedom = (total_unique_chars-1) * 1
    
    print("\nTotal unique characters:", total_unique_chars)
    print("\nTotal Source Count:", total_source_count)
    print("\nTotal Encrypted Count:", total_encrypted_count)
    print("\nTotal Total Count: ", total_total_count)
    print("\nChi Square Value: ",chi_period)
    print("\nDegree of Freedom: ",degree_of_freedom)

def chi_period_calculate(count_source, count_encrypted, add, club_total_s_total_e, total_total_count):
        top = (count_source ** 2) + (count_encrypted ** 2)
        bottom = (club_total_s_total_e * add) / total_total_count
        chi_period = top / bottom
        return chi_period

def divide_file_content(source_string):
    file_size = len(source_string)
    x = math.ceil(file_size / 4)  # Lower ceiling size for each part
    y = file_size % 4  # Remainder

    # Divide into 4 parts
    list1 = source_string[:x + y]
    list2 = source_string[x + y:x + y + x]
    list3 = source_string[x + y + x:x + y + x + x]
    list4 = source_string[x + y + x + x:]

    return list1, list2, list3, list4

def shuffle_list():
    # Create the initial list
    bit_lengths = [8, 16, 32, 64]

    # Shuffle the list
    random.shuffle(bit_lengths)

    return bit_lengths

def count_spaces(input_string):
    space_positions = {}
    
    # Iterate through the string and count spaces
    for index, char in enumerate(input_string):
        if char == ' ':
            if index in space_positions:
                space_positions[index] += 1
            else:
                space_positions[index] = 1
    
    return space_positions

def main():
    input_file_path = 'TXT Files/inpit12.txt'  # Change to the actual input file path
    input_file_size = os.path.getsize(input_file_path)
    print(f'Input File Size: {input_file_size} bytes')
    source_string = read_file_content(input_file_path)
    

    num=int(input("Press 1 for normal rppo\nPress 2 for complex rppo\nEnter your choice: "))

    if num==1:

        source_blocks = [string_to_binary(source_string[i:i + 1]) for i in range(0, len(source_string), 1)]
        max_sub_source_block_size = max(source_blocks, key=len)

        # refrshing files by deleting their content

        with open("encrypted.txt","w") as file:
            pass

        with open("decrypted.txt","w") as file:
            pass

        print(f'maximum block number of encryption: {len(max_sub_source_block_size)}\n')

        encryption_number = int(input("Enter the block number of encryption: "))

        encrypted_strings = []
        decrypted_strings = []
        decrypted_block_lists = []
        total_encryption_time = 0
        total_decryption_time = 0

        if encryption_number >= len(max_sub_source_block_size):
            print("Encryption not possible")
        else:
            for block_number, source_block in enumerate(source_blocks):
                num_iterations = len(max_sub_source_block_size)

                padded_source_block, _ = pad_source_block(source_block, num_iterations)
                

                intermediate_blocks = generate_blocks(padded_source_block, num_iterations, encryption_number)

                
                print(f'Block {block_number + 1}:')
                print(f'Source String: {binary_to_string(padded_source_block)}')
                print(f'Source Block (Binary): {source_block}\n')

                # Encryption Time Calculation
                start_time_encryption = time.time()
                for i, block in enumerate(intermediate_blocks[1:], start=1):
                    print(f'Encrypted Block {i}: {block}\n')

                encrypted_block = encrypt(padded_source_block, encryption_number, num_iterations)
                encrypted_string = binary_to_string(encrypted_block)

                encrypted_strings.append(encrypted_string)
                end_time_encryption = time.time()
                total_encryption_time += (end_time_encryption - start_time_encryption)

                print(f'Encrypted Block (Binary): {encrypted_block}\n')
                print(f'Encrypted String: {encrypted_string}\n')

                # Decryption Time Calculation
                start_time_decryption = time.time()
                decrypted_blocks = decrypt(encrypted_block, encryption_number, num_iterations)

                for i, block in enumerate(decrypted_blocks):
                    decrypt_itr_number = i + encryption_number + 1
                    print(f'Decrypted Block {decrypt_itr_number}: {block}\n')

                decrypted_string = binary_to_string(decrypted_blocks[-1])
                decrypted_block_lists.append(decrypted_blocks[-1])
                decrypted_strings.append(decrypted_string)
                end_time_decryption = time.time()
                total_decryption_time += (end_time_decryption - start_time_decryption)

                print(f'Decrypted String: {decrypted_string}\n')

            
            """print("Final Encrypted String:")"""
            final_encrypted_string = ''.join(encrypted_strings)
            encrypted_content = final_encrypted_string.encode('utf-8')  # Replace encrypted_ascii_var with your encrypted content
            write_file('encrypted.txt', encrypted_content)

            """print("\nFinal Decrypted String:")"""
            final_decrypted_string = ''.join(decrypted_strings)
            decrypted_content = final_decrypted_string.encode('utf-8')  # Replace decrypted_ascii_var with your decrypted content
            write_file('decrypted.txt', decrypted_content)

            # Count characters in the source string
            if source_string:
                character_count_source = count_characters(source_string)
                
                # Count characters in the encrypted string
                encrypted_string = ''.join(encrypted_strings)
                character_count_encrypted = count_characters(encrypted_string)

                # Tabulate character counts
                print("\nCharacter Counts:")
                tabulate_character_counts(character_count_source, character_count_encrypted)
            else:
                print("No content to analyze.")

            print(f'Input File Size: {input_file_size} bytes')
            print("\nTotal Encryption Time:", total_encryption_time, "seconds")
            print("Total Decryption Time:", total_decryption_time, "seconds")
            avg_accuracy = average_accuracy(source_blocks, decrypted_block_lists)
            print("Average accuracy:", avg_accuracy)
            print("Total XOR operations during encryption:", encryption_xor_count)
            print("Total XOR operations during decryption:", decryption_xor_count)

    elif num==2:
        
        if source_string is not None:
            list1, list2, list3, list4 = divide_file_content(source_string)

            # print(f'List 1 (Size: {len(list1)}):\n{list1}')
            # print(f'List 2 (Size: {len(list2)}):\n{list2}')
            # print(f'List 3 (Size: {len(list3)}):\n{list3}')
            # print(f'List 4 (Size: {len(list4)}):\n{list4}')

            list_bulk = [list1, list2, list3, list4]
            # print(list_bulk)

            shuffled_bit_lengths = shuffle_list()
            # print(f"Shuffled list: {shuffled_bit_lengths}")

            n=0
            list_bulk2 = []

            for item in list_bulk:
                
                if shuffled_bit_lengths[n] == 8:
                    source_blocks = [string_to_binary(item[i:i + 1]) for i in range(0, len(item), 1)]

                elif shuffled_bit_lengths[n] == 16:
                    source_blocks = [string_to_binary(item[i:i + 2]) for i in range(0, len(item), 2)]

                elif shuffled_bit_lengths[n] == 32:
                    source_blocks = [string_to_binary(item[i:i + 4]) for i in range(0, len(item), 4)]

                else:
                    source_blocks = [string_to_binary(item[i:i + 8]) for i in range(0, len(item), 8)]
                n+=1
                list_bulk2.append(source_blocks)
            # print("This is list bulk2\n")
            # print(list_bulk2)

            shuffled_list_dict = {
                shuffled_bit_lengths[0]: list_bulk2[0],
                shuffled_bit_lengths[1]: list_bulk2[1],
                shuffled_bit_lengths[2]: list_bulk2[2],
                shuffled_bit_lengths[3]: list_bulk2[3]
            }

            print("\n")

            # print(shuffled_list_dict)

         # refrshing files by deleting their content

            with open("complex_encrypted.sys","w") as file:
                pass

            with open("complex_decrypted.sys","w") as file:
                pass


            print("Maximum encrption block number can't be more than 7")

            encryption_number = int(input("Enter the block number of encryption: "))
            source_blocks=[]
            padded_source_strings = ""
            complex_source_strings=""

            if encryption_number<=7:

                for key,value in shuffled_list_dict.items():
 
                    encrypted_strings = []
                    decrypted_strings = []
                    decrypted_block_lists = []
                    total_encryption_time = 0
                    total_decryption_time = 0

                    source_blocks = value
                    source_block = []
                    # print(value)
                    # for binary in source_blocks:
                    #     complex_source_strings+=binary_to_string(binary)
                    # print(complex_source_strings)


                    for block_number, source_block in enumerate(source_blocks):
                        num_iterations = key

                        padded_source_block, _ = pad_source_block(source_block, num_iterations)
                        padded_source_strings+=binary_to_string(source_block)
                        
                        # print("Padded Source Block")
                        # print(padded_source_strings)

                        intermediate_blocks = generate_blocks(padded_source_block, num_iterations, encryption_number)

                        
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
                        # complex_encryption_time += total_encryption_time

                        """print(f'Encrypted Block (Binary): {encrypted_block}\n')
                        print(f'Encrypted String: {encrypted_string}\n')"""

                        # Decryption Time Calculation
                        start_time_decryption = time.time()
                        decrypted_blocks = decrypt(encrypted_block, encryption_number, num_iterations)

                        """for i, block in enumerate(decrypted_blocks):
                            decrypt_itr_number = i + encryption_number + 1
                            print(f'Decrypted Block {decrypt_itr_number}: {block}\n')"""

                        decrypted_string = binary_to_string(decrypted_blocks[-1])
                        decrypted_block_lists.append(decrypted_blocks[-1])
                        decrypted_strings.append(decrypted_string)
                        end_time_decryption = time.time()
                        total_decryption_time += (end_time_decryption - start_time_decryption)
                        # complex_decryption_time += total_decryption_time

                        # print(f'Decrypted String: {decrypted_string}\n')

                    
                    # print("Final Encrypted String:")
                    final_encrypted_string = ''.join(encrypted_strings)
                    # print(final_encrypted_string)
                    encrypted_content = final_encrypted_string.encode('utf-8')  # Replace encrypted_ascii_var with your encrypted content
                    write_file('complex_encrypted.cpp', encrypted_content)

                    # print("\nFinal Decrypted String:")
                    final_decrypted_string = ''.join(decrypted_strings)
                    # print(final_decrypted_string)
                    decrypted_content = final_decrypted_string.encode('utf-8')  # Replace decrypted_ascii_var with your decrypted content
                    write_file('complex_decrypted.cpp', decrypted_content)
                    spaces = count_spaces(source_string)
                
                
                if source_string:
                    character_count_source = count_characters(source_string)
                    
                    # Count characters in the encrypted string
                    encrypted_string = ''.join(encrypted_strings)
                    character_count_encrypted = count_characters(encrypted_string)

                    # Tabulate character counts
                    print("\nCharacter Counts:")
                    tabulate_character_counts(character_count_source, character_count_encrypted)
                else:
                    print("No content to analyze.")   
                print("\n\nTotal Encryption Time: ", total_encryption_time)
                print("\n\nTotal Decryption Time: ", total_decryption_time)
                
                print(f'Input File Size: {input_file_size} bytes')
                avg_accuracy = average_accuracy(source_blocks, decrypted_block_lists)
                print("Average accuracy:", avg_accuracy)
                print("Total XOR operations during encryption:", encryption_xor_count)
                print("Total XOR operations during decryption:", decryption_xor_count)


if __name__ == "__main__":
    main()