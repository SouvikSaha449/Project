import struct

# Define the desired size of the .sys file
file_size = 18912

# Define the content to be written inside the file
file_content = b"file created"

# Calculate the number of padding bytes needed
padding_size = file_size - len(file_content)

# Create a bytearray with the specified content
sys_file_data = bytearray(file_content)

# Add padding bytes if necessary
sys_file_data.extend(b'\x00' * padding_size)

# Specify the output file name
output_file_name = 'example.sys'

# Write the data to the file
with open(output_file_name, 'wb') as f:
    f.write(sys_file_data)

print(f"File '{output_file_name}' created successfully with a size of {file_size} bytes.")
