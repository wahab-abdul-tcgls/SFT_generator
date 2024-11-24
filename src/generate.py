import os
import subprocess
from datetime import datetime
import json
import random 
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SERVICE_NAME = os.getenv("AWS_SERVICE_NAME")
REGION_NAME = os.getenv("AWS_REGION_NAME")
ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
ACCESS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

client = boto3.client(service_name=SERVICE_NAME, region_name=REGION_NAME,
                      aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=ACCESS_SECRET_KEY)

def select_random_template(template_dir):
    """
    Select a random `.py` file from the specified templates directory.

    Args:
        template_dir (str): The directory containing template `.py` files.

    Returns:
        str: The content of the randomly selected `.py` file.
    """
    try:
        files = [f for f in os.listdir(template_dir) if f.endswith('.py')]
        if not files:
            raise FileNotFoundError("No `.py` files found in the templates directory.")
        random_file = random.choice(files)
        file_path = os.path.join(template_dir, random_file)
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        raise RuntimeError(f"Error selecting template: {e}")

def save_generated_code(code_content, code_dir):
    """
    Save the generated Python code to a file in the specified directory.

    Args:
        code_content (str): The Python code to be saved.
        code_dir (str): The directory where the code file should be saved.

    Returns:
        str: Path to the saved code file.
    """
    os.makedirs(code_dir, exist_ok=True)
    script_path = os.path.join(code_dir, 'generated_chart.py')
    with open(script_path, 'w') as script_file:
        script_file.write(code_content)
    print(f"Generated code saved in: {script_path}")
    return script_path

def save_chart(chart, library, charts_dir, filename='chart.png'):
    """
    Save a chart to the specified directory based on its library.

    Args:
        chart: The chart object to save.
        library (str): The library used to create the chart.
        charts_dir (str): The directory to save the chart.
        filename (str): The name of the file to save the chart as (default: 'chart.png').
    """
    os.makedirs(charts_dir, exist_ok=True)
    chart_path = os.path.join(charts_dir, filename)

    try:
        if library in ['matplotlib', 'seaborn']:
            import matplotlib.pyplot as plt
            plt.savefig(chart_path)
        elif library == 'altair':
            chart.save(chart_path)
        elif library == 'bokeh':
            from bokeh.io.export import export_png
            export_png(chart, filename=chart_path)
        elif library == 'squarify':
            import matplotlib.pyplot as plt
            plt.savefig(chart_path)  # Squarify relies on Matplotlib
        elif library == 'mplfinance':
            import mplfinance as mpf
            mpf.plot(chart, savefig=dict(fname=chart_path, dpi=100))
        elif library == 'plotly':
            chart.write_image(chart_path)
        else:
            raise ValueError(f"Unsupported library: {library}")
        
        print(f"Chart saved at: {chart_path}")
    except Exception as e:
        print(f"Error saving chart: {e}")

def generate_claude_code(template_dir, user_instructions):
    """
    Generate Python code using Claude LLM based on user instructions and a randomly selected template.
    Save the results (scripts and charts) in organized folders under `results/`.

    Args:
        template_dir (str): The directory containing template `.py` files.
        user_instructions (str): The instructions to modify the code.

    Returns:
        str: The modified Python code.
    """
    # Select a random template
    user_prompt_code = select_random_template(template_dir)

    model_id = 'anthropic.claude-v2'
    
    # Combine system prompt, user instructions, and user-provided code
    prompt = f"{user_instructions}\n{user_prompt_code}"
    
    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 1024,
        "temperature": 0.5
    }

    response = client.invoke_model(modelId=model_id, body=json.dumps(body))
    
    # Extract response from model
    completion = json.loads(response["body"].read())["completion"]
    generated_code = '\n'.join(completion.split('\n')[1:])
    
    # Prepare the results folder
    timestamp = datetime.now().strftime('%d %B')  # Format: 25 November
    results_base = os.path.join('results', timestamp)
    code_dir = os.path.join(results_base, 'code')
    charts_dir = os.path.join(results_base, 'charts')
    
    # Save the generated code
    script_path = save_generated_code(generated_code, code_dir)

    # Execute the script
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Charts saved in: {charts_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the generated script: {e}")

    return generated_code


# def generate_claude_code(user_prompt):
#     model_id = 'anthropic.claude-v2'
#     system_prompt = 'You are an intelligent python code assistant. Write efficient python codes for generating charts using valid libraries like matplotlib, seaborn, Altair, Bokeh, Squarify, mplfinance, plotly,GGplot, plotnine. Write the whole code including dataset and chart'
#     prompt = f"System: {system_prompt}\n\nHuman: {user_prompt}\n\nAssistant:"

#     body = {
#         "prompt": prompt,
#         "max_tokens_to_sample": 1024,
#         "temperature": 0.5
#     }

#     response = client.invoke_model(modelId=model_id, body=json.dumps(body))

#     # Extract response from model
#     completion = json.loads(response["body"].read())["completion"]
#     response = '\n'.join(completion.split('\n')[1:])

#     return response


def generate_mixtral_code(template_dir, user_instructions):
    model_id = "mistral.mixtral-8x7b-instruct-v0:1"

    # Select a random template
    user_prompt_code = select_random_template(template_dir)
    
    # Combine system prompt, user instructions, and user-provided code
    prompt = f"{user_instructions}\n{user_prompt_code}"
    
    native_request = {
        "prompt": prompt,
        "max_tokens": 4096,
        "temperature": 0.8,
    }

    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())
        response_text = model_response["outputs"][0]["text"]

        # Prepare the results folder
        timestamp = datetime.now().strftime('%d %B')  # Format: 25 November
        results_base = os.path.join('results', timestamp)
        code_dir = os.path.join(results_base, 'code')
        charts_dir = os.path.join(results_base, 'charts')
        
        # Save the generated code
        script_path = save_generated_code(response_text, code_dir)

        subprocess.run(['python', script_path], check=True)
        print(f"Charts saved in: {charts_dir}")

    except subprocess.CalledProcessError as e:
        print(f"Error executing the generated script: {e}")
        
        return response_text

    except (ClientError, Exception, json.JSONDecodeError) as e:
        print(f"ERROR: Can't invoke '{model_id}' or parse response. Reason: {e}")
        return "Summary generation failed.", "Title generation failed."