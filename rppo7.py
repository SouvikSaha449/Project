import os
import math
import random

def read_file_content(file_path):
    valid_extensions = {'.sys', '.exe', '.cpp', '.com', '.dll', '.txt'}
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
        print("Unsupported file type. Only .sys, .exe, .cpp, .com, .dll, and .txt files are supported.")
        return None

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

def string_to_binary_blocks(string, block_size):
    binary_blocks = []
    for i in range(0, len(string), block_size):
        block = string[i:i + block_size]
        binary_blocks.append(block)
    return binary_blocks

def string_to_binary(string):
    binary_values = []
    for char in string:
        ascii_value = ord(char)
        binary_value = format(ascii_value, '08b')  # Convert ASCII to 8-bit binary
        binary_values.extend([int(bit) for bit in binary_value])
    return binary_values

def shuffle_list():
    # Create the initial list
    bit_lengths = [8, 16, 32, 64]

    # Shuffle the list
    random.shuffle(bit_lengths)

    return bit_lengths

def main():
    input_file_path = 'TXT Files/inpit12.txt'  # Change to the actual input file path
    input_file_size = os.path.getsize(input_file_path)
    print(f'Input File Size: {input_file_size} bytes')
    source_string = read_file_content(input_file_path)
    if source_string is not None:
        list1, list2, list3, list4 = divide_file_content(source_string)

        print(f'List 1 (Size: {len(list1)}):\n{list1}')
        print(f'List 2 (Size: {len(list2)}):\n{list2}')
        print(f'List 3 (Size: {len(list3)}):\n{list3}')
        print(f'List 4 (Size: {len(list4)}):\n{list4}')

        list_bulk = [list1, list2, list3, list4]
        print(list_bulk)

        shuffled_bit_lengths = shuffle_list()
        print(f"Shuffled list: {shuffled_bit_lengths}")

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

        shuffled_list_dict2 = {
            shuffled_bit_lengths[0]: list_bulk2[0],
            shuffled_bit_lengths[1]: list_bulk2[1],
            shuffled_bit_lengths[2]: list_bulk2[2],
            shuffled_bit_lengths[3]: list_bulk2[3]
        }

        print("\n")

        print(shuffled_list_dict2)

        for key,values in shuffled_list_dict2.items():
            print(f"Key: {key} and values: {values}")



if __name__ == "__main__":
    main()
