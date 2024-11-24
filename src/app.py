from generate import generate_claude_code,generate_mixtral_code

if __name__ == "__main__":
    # Example user instructions
    user_instructions = "Replace the data with finance data in the below code and strictly write code to generate the chart type. Strictly change the font ,fontsize, colours, and overall theme "

    # Path to the templates directory
    template_dir = "templates"

    # Call the function from generate.py
    generated_code = generate_mixtral_code(template_dir, user_instructions)
    print("Generated Code:\n", generated_code)