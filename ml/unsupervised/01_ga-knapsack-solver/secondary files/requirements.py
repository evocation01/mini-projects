# requirements.py: Update problematic requirements in requirements.txt
def update_requirements(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        # Check for pywin32 and fix its versioning
        if "pywin32~=" in line:
            updated_lines.append("pywin32==307\n")
        else:
            updated_lines.append(line)

    # Save the updated lines back to the file
    with open(file_path, "w") as file:
        file.writelines(updated_lines)

    print(f"Updated {file_path} successfully!")


# Path to requirements.txt
file_path = "Projects/python/knapsack-genome-project/requirements.txt"

# Call the function
if __name__ == "__main__":
    update_requirements(file_path)
