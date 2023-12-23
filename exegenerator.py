# Import the os and random modules
import os
import random

# Define the file name and the target size in bytes
file_name = "custom_size1.exe"
target_size = 37220

# Open the file in binary append mode
with open(file_name, "ab") as f:
    # Get the current file size
    current_size = os.path.getsize(file_name)
    # Calculate the number of bytes to append
    bytes_to_append = target_size - current_size
    # Generate a list of random bytes
    random_bytes = [random.randint(0, 255) for _ in range(bytes_to_append)]
    # Convert the list to a bytes object
    random_bytes = bytes(random_bytes)
    # Write the bytes to the file
    f.write(random_bytes)
