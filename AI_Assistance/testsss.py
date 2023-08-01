import os
import openai
openai.api_key="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"
# openai.Model.list()

response = openai.Completion.create(
    engine='text-davinci-003',  # Specify the GPT-3 model variant
    prompt='Who is shivaji',
    max_tokens=100  # Set the desired length of the generated text
)

generated_text = response.choices[0].text.strip()
print(generated_text)
