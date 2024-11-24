from generate import generate_claude_code

if __name__ == "__main__":
    # Example user instructions
    user_instructions = "Replace the data with finance data and generate the chart. Save the chart in a PNG file."

    # Path to the templates directory
    template_dir = "templates"

    # Call the function from generate.py
    generated_code = generate_claude_code(template_dir, user_instructions)
    print("Generated Code:\n", generated_code)