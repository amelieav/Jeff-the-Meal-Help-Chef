from getRecipeFromJSON import RecipeList

input_file = "links.txt"
output_file = "adjusted-link.txt"

# Read the contents of the input file
with open(input_file, "r") as f:
    lines = f.readlines()

# Modify each line to include speech marks at the start and end, and add a comma
modified_lines = [f'"{line.strip()}",' for line in lines]

# Write the modified lines to the output file
with open(output_file, "w") as f:
    f.write("\n".join(modified_lines))
