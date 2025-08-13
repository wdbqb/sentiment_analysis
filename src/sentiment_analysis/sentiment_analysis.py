from google import genai
from google.genai import types

from src.sentiment_analysis.main import user_input

# define the system instruction
user_input = 'GOOD JOB'
system_instruction = """You are an AI assistant specializing in sentiment analysis. Your task is to analyze user input and determine its sentiment, categorizing it as either positive, negative, or neutral."""
prompt = types.Part.from_text(text=f"""Analyze the following user input and determine its sentiment. Provide the sentiment outcome and the reasoning behind your analysis in JSON format.

User Input:
{user_input}


Output the sentiment analysis in the following JSON format:

```json
{
  \"sentiment\": \"positive | negative | neutral\",
  \"reasoning\": \"Explanation of why the sentiment was classified as such.\"
}
```

Example:

```json
{
  \"sentiment\": \"positive\",
  \"reasoning\": \"The user expressed satisfaction with the product and praised its features.\"
}
```""")



def generate():
  client = genai.Client(
      vertexai=True,
      project="sentiment-analysis-468823",
      location="global",
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
  print(response.text)

  return response.text

generate()

