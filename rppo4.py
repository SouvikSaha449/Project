import math
import base64

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

def encrypt(source_block, block_number, num_iterations):
    intermediate_blocks = generate_blocks(source_block, num_iterations)
    return intermediate_blocks[block_number]

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
    utf8_bytes = string.encode('utf-8')
    binary_values = []
    for byte in utf8_bytes:
        binary_value = format(byte, '08b')  # Convert byte to 8-bit binary
        binary_values.extend([int(bit) for bit in binary_value])
    return binary_values

def binary_to_string(binary_values):
    bytes_list = [binary_values[i:i+8] for i in range(0, len(binary_values), 8)]
    utf8_bytes = bytearray([int(''.join(map(str, byte)), 2) for byte in bytes_list])
    
    try:
        return utf8_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Handle invalid characters by ignoring them or replacing them
        return utf8_bytes.decode('utf-8', errors='ignore')


def main():
    input_string = input("Enter a string to encrypt: ")
    source_block = string_to_binary(input_string)
    size = len(source_block)

    # Calculate the number of iterations based on the size of the source block
    num_iterations = 2 ** math.ceil(math.log2(size))

    block_number = int(input("Enter the block number of encryption: "))

    intermediate_blocks = generate_blocks(source_block, num_iterations)

    print(f'Source String: {input_string}')
    print(f'Source Block (Binary): {source_block}\n')

    for i, block in enumerate(intermediate_blocks[1:block_number + 1], start=1):
        print(f'Encrypted Block {i}: {block}\n')

    encrypted_block = encrypt(source_block, block_number, num_iterations)
    encrypted_string = binary_to_string(encrypted_block)
    print(f'Encrypted String: {encrypted_string}')
    
    decrypted_blocks = decrypt(encrypted_block, block_number, num_iterations)

    for i, block in enumerate(decrypted_blocks):
        print(f'Decrypted Block {i + block_number + 1}: {block}\n')

    print(f'Source String: {input_string}')
    print(f'Encrypted String: {encrypted_string}')
    decrypted_string = binary_to_string(decrypted_blocks[-1])
    print(f'Decrypted String: {decrypted_string}')

if __name__ == "__main__":
    main()
