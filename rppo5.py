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

def binary_to_string(binary_values):
    # Convert binary values to 32-bit integers
    ints_list = [binary_values[i:i+32] for i in range(0, len(binary_values), 32)]
    utf32_values = [int(''.join(map(str, bits)), 2) for bits in ints_list if len(bits) == 32]

    # Filter out invalid code points and convert UTF-32 values to the original string
    utf32_string = ''.join([chr(value) for value in utf32_values if 0 <= value <= 0x10FFFF])

    return utf32_string


def string_to_binary(string):
    utf32_values = [ord(char) for char in string]
    binary_values = []
    for value in utf32_values:
        binary_value = format(value, '032b')  # Convert value to 32-bit binary
        binary_values.extend([int(bit) for bit in binary_value])
    return binary_values



def main():
    input_string = input("Enter a string to encrypt: ")
    source_block = string_to_binary(input_string)
    size = len(source_block)

    # Calculate the number of iterations based on the size of the source block
    num_iterations = 2 ** math.ceil(math.log2(size))

    block_number = int(input("Enter the block number of encryption: "))

    intermediate_blocks = generate_blocks(source_block, num_iterations)

    print(f'Source String: {input_string}')
    print(f'\nSource UTF-32 Values: {[ord(char) for char in input_string]}\n')

    print(f'Source Block (Binary): {source_block}\n')

    for i, block in enumerate(intermediate_blocks[1:block_number + 1], start=1):
        print(f'Encrypted Block {i}: {block}\n')

    encrypted_block = encrypt(source_block, block_number, num_iterations)
    encrypted_string = binary_to_string(encrypted_block)
    print(f'\nEncrypted UTF-32 Values: {[ord(char) for char in encrypted_string]}\n')
    print(f'\nEncrypted String: {encrypted_string}')
    
    decrypted_blocks = decrypt(encrypted_block, block_number, num_iterations)

    for i, block in enumerate(decrypted_blocks):
        print(f'\nDecrypted Block {i + block_number + 1}: {block}\n')

    decrypted_string = binary_to_string(decrypted_blocks[-1])
    print(f'\nDecrypted UTF-32 Values: {[ord(char) for char in decrypted_string]}')
    print(f'\nDecrypted String: {decrypted_string}')

    print(f'\nEncrypted String: {encrypted_string}')

if __name__ == "__main__":
    main()
