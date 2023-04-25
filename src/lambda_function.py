import os
import openai
import json

# Set up the OpenAI API client
openai.api_key = os.environ['OPENAI_API_KEY']

def lambda_handler(event, context):
    # Retrieve the input prompt from the request
    prompt = event['input']
    
    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Retrieve the response from the API
    output = response.choices[0].text
    
    # Return the response to the calling function of the lambda
    return {
        'statusCode': 200,
        'body': json.dumps(output),
        'headers': {
            'Content-Type': 'application/json'
        }
    }