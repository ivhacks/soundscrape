from google import genai

with open(".env", "r") as f:
    gemini_api_key_variable = f.read()
client = genai.Client(api_key=gemini_api_key_variable)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)