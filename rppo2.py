#This is the version which will fully generate blocks until the size of the block

def generate_blocks(source_block):
    intermediate_blocks = []
    intermediate_blocks.append(source_block.copy())

    num_iterations = len(source_block)

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

def main():
    size = int(input("Enter the size of the source block: "))
    source_block = []
    for i in range(size):
        bit = int(input(f"Enter bit {i + 1} (0 or 1) for the source block: "))
        source_block.append(bit)

    intermediate_blocks = generate_blocks(source_block)

    # Rename the initial block to "Source Block"
    intermediate_blocks[0] = source_block

    # Print the "Source Block"
    print(f'Source Block: {source_block}')

    # Print the other intermediate blocks
    for i, block in enumerate(intermediate_blocks[1:], start=1):
        print(f'Block {i}: {block}')

if __name__ == "__main__":
    main()
