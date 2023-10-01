

import math

def generate_blocks(source_block, num_iterations):
    intermediate_blocks = []
    intermediate_blocks.append(source_block.copy())

    def generate_block_recursive(block, remaining_iterations):
        if remaining_iterations == 0:
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

def encrypt(padded_source_block, block_number, num_iterations):
    intermediate_blocks = generate_blocks(padded_source_block, num_iterations)
    return intermediate_blocks[block_number], padded_source_block

def decrypt(final_block, block_number, num_iterations):
    if block_number >= len(final_block):
        return []

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

    generate_block_recursive(final_block, num_iterations - block_number)

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
    chars = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def main():
    input_string = input("Enter a string to encrypt: ")
    source_block = string_to_binary(input_string)
    size = len(source_block)
 
    num_iterations = 2 ** math.ceil(math.log2(size))

    block_number = int(input("Enter the block number of encryption: "))


    padded_source_block, _ = pad_source_block(source_block, num_iterations)

    intermediate_blocks = generate_blocks(padded_source_block, num_iterations)

    print(f'Source String: {input_string}')
    print(f'\nSource ASCII Values: {[ord(char) for char in input_string]}\n')
    print(f'\nSize of Padded Source Block: {len(padded_source_block)}')

    print(f'Source Block (Binary): {padded_source_block}\n')

    for i, block in enumerate(intermediate_blocks[1:block_number + 1], start=1):
        print(f'Encrypted Block {i}: {block}\n')

    encrypted_block, _ = encrypt(padded_source_block, block_number, num_iterations)
    encrypted_string = binary_to_string(encrypted_block)
    print(f'\nEncrypted ASCII Values: {[ord(char) for char in encrypted_string]}\n')
    print(f'\nEncrypted String: {encrypted_string}')
    
    decrypted_blocks = decrypt(encrypted_block, block_number, num_iterations)

    for i, block in enumerate(decrypted_blocks):
        print(f'\nDecrypted Block {i + block_number + 1}: {block}\n')

    decrypted_string = binary_to_string(decrypted_blocks[-1])
    print(f'\nDecrypted ASCII Values: {[ord(char) for char in decrypted_string]}')
    print(f'\nDecrypted String: {decrypted_string}')

    

if __name__ == "__main__":
    main()
