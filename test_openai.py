from open import OpenAI

# Put your API key here temporarily (for testing only)
client = OpenAI(api_key="sk-your-api-key-here")

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # ✅ same model used in your app
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you confirm if my API key is working?"}
        ],
        max_tokens=50
    )

    print("✅ Success! GPT Response:")
    print(response.choices[0].message.content.strip())

except Exception as e:
    print("❌ Error:", e)