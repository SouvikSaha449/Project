# This is the RPPO Code of bits

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

def main():
    size = int(input("Enter the size of the source block: "))
    source_block = []
    for i in range(size):
        bit = int(input(f"Enter bit {i + 1} (0 or 1) for the source block: "))
        source_block.append(bit)

    if size in [2, 4, 8, 16]:
        num_iterations = size
    elif size % 2 == 0 and size <= 16:
        num_iterations = 16
    else:
        num_iterations = size

    block_number = int(input("Enter the block number of encryption: "))

    intermediate_blocks = generate_blocks(source_block, num_iterations)

   
    source_block = source_block

  
    print(f'Source Block: {source_block}')

    print()


    for i, block in enumerate(intermediate_blocks[1:block_number + 1], start=1):
        print(f'Encrypted Block {i}: {block}')

    print()

 
    encrypted_block = encrypt(source_block, block_number, num_iterations)
    print(f'Encrypted : {encrypted_block}')

    print()

  
    decrypted_blocks = decrypt(encrypted_block, block_number, num_iterations)


    for i, block in enumerate(decrypted_blocks):
        print(f'Decrypted Block {i + block_number + 1}: {block}')

    print()

    print(f'Decrypted : {decrypted_blocks[-1]}')

if __name__ == "__main__":
    main()
