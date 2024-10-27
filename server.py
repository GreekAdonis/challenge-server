import json
import requests
import os
from collections import defaultdict

def create_response(status_code, body):
   
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    try:
        if 'body' in event:
            file_content = event['body']

            response_body = categorise_intents(file_content)
            return create_response(200, json.dumps(response_body))
            
        else:
            with open('all_intents.txt', 'r') as file:
                json_string = file.read()
            data = json.loads(json_string)
            return create_response(200, json.dumps(data))
        
    except Exception as e:
        return create_response(500, json.dumps({
                'error': str(e)
            }))

def categorise_intents(input_file):
    chunk_size = int(os.environ.get('chunk_size'))
    results = defaultdict(list)
    lines = input_file.split("\n")
    total_lines = len(lines)
    for i in range(0, total_lines, chunk_size):
        chunk = lines[i:min(i+chunk_size, total_lines)]

        if i == 0:
            prompt = "Given the below list of user intents respond with only a JSON dictionary of the intents keyed by category. The goal is to choose broad categories so that all of the intents can be visualised along with overlap. Respond with only JSON.\n\n" + ''.join(chunk)
            generate_categories(results, prompt)

        else:
            prompt = "Below is a list of categories and a list of user intents. Respond with only a JSON dictionary matching each user intent to all suitable categories and create new categories where appropriate. The goal is to choose broad categories so that all of the intents can be visualised along with overlap. Respond with ONLY a JSON dictionary of the intents keyed by category without triple backticks.\n\nCategories:\n" + "\n".join(results.keys()) + "\n\nUser Intents:\n" + ''.join(chunk)
            generate_categories(results, prompt)            
    
    return results

def generate_categories(result_dict, prompt):
    generated_dict = json.loads(generate_response(prompt))
    for key, value in generated_dict.items():
        if key in result_dict:
            result_dict[key].extend(value)
        else:
            result_dict[key] = value


def generate_response(prompt):
    response = requests.post(
        url=os.environ.get('llm_api_url'),
        headers={"Authorization": os.environ.get('llm_api_token')},
        data=json.dumps({
            "model": os.environ.get('llm_api_model'),
            "messages":[{"role":"user","content":prompt}]}))
    json_string = json.loads(json.dumps(response.json()))
    return json_string["choices"][0]['message']['content'].strip()    