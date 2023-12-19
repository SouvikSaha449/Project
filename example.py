file_size = 16723  # Specify the desired file size in bytes
output_file_path = 'generated_file.cpp'

# Create content for the CPP file with a print statement
content = f'#include <iostream>\n\nint main() {{\n    std::cout << "File Size: {file_size} bytes" << std::endl;\n    return 0;\n}}\n'

# Calculate the number of repetitions needed to achieve the desired size
repetitions = file_size // len(content) + 1

# Generate the content by repeating the lines
final_content = content * repetitions

# Write the content to the CPP file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(final_content)

print(f'CPP file "{output_file_path}" generated with a size of {file_size} bytes.')
