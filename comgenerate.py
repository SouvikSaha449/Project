with open('output.com', 'wb') as file:
    # Specify the desired size (in bytes)
    desired_size = 32677
    
    # Write zeros to the file to achieve the desired size
    file.write(b'\x00' * desired_size)

print(f"File 'output.com' created with a size of {desired_size} bytes.")
