from google import genai
from google.genai import types

import json
from google.cloud import secretmanager
import os
from google.oauth2 import service_account
from google.cloud import storage
from dotenv import load_dotenv


#set up the GCP account and project
load_dotenv()

project_id = os.getenv("project_id", "default-project-id")
secret_name = os.getenv("secret_name", "default-secret-name")
bucket_name = os.getenv("bucket_name")


secret_client = secretmanager.SecretManagerServiceClient()
secret_version_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
response = secret_client.access_secret_version(name=secret_version_name)
secret_payload = response.payload.data.decode("UTF-8")
SECRET_DATA = json.loads(secret_payload)  # global variable
credentials = service_account.Credentials.from_service_account_info(
    SECRET_DATA,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)
# cloud storage

STORAGE_CLIENT = storage.Client(credentials=credentials)
BUCKET = STORAGE_CLIENT.get_bucket(bucket_name) if bucket_name else None


def generate(user_input):
  # define prompt and system instruction

  system_instruction = """You are an AI assistant specializing in sentiment analysis. Your task is to analyze user input and determine its sentiment, categorizing it as either positive, negative, or neutral."""

  prompt = types.Part.from_text(text=f"""Analyze the following user input and determine its sentiment. Provide the sentiment outcome and the reasoning behind your analysis in JSON format.

  User Input:
  {user_input}


  Output the sentiment analysis in the following JSON format:

  ```json
  {{
    \"sentiment\": \"positive | negative | neutral\",
    \"reasoning\": \"Explanation of why the sentiment was classified as such.\"
  }}
  ```

  Example:

  ```json
  {{
    \"sentiment\": \"positive\",
    \"reasoning\": \"The user expressed satisfaction with the product and praised its features.\"
  }}
  ```""")

  client = genai.Client(
      vertexai=True,

      project=project_id,
      location="global",
      credentials=credentials
  )
# prompt
  text1 = prompt
  si_text1 = system_instruction

  model = "gemini-2.5-flash-lite"
  contents = [
    types.Content(
      role="user",
      parts=[
        text1
      ]
    )
  ]

  generate_content_config = types.GenerateContentConfig(
    temperature = 0.2,
    top_p = 0.3,
    max_output_tokens = 65535,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    system_instruction=[types.Part.from_text(text=si_text1)],
    thinking_config=types.ThinkingConfig(
      thinking_budget=0,
    ),
  )

  response = client.models.generate_content(
        model = model,
        contents = contents,
        config = generate_content_config)


  # try:
  #   result_json = json.loads(response.text)
  # except json.JSONDecodeError:
  #   result_json = {"sentiment": "Unknown", "reasoning": "Parsing error"}

  print(response.text)

  return response.text

