import requests

url = "http://localhost:8000/predict"  # Replace with the actual URL of your FastAPI server

input_data = {
    "model": "gpt-4",
    "response_format": {"type": "json_object"},
    "messages": [
        {
            "role": "system",
            "content": "You are DCPR Assistant who is knowldgeable about development regulations for the buildings in mumbai. Use the following pieces of retrieved context to answer the question. Always answer like a human and do not mention that you are just reading from context documents. If you are very sure about the answer, give a very straightforward answer. ALways look for the answer in the knowledge base before any assumption\nIf you are not completely sure about the answer. Present your answer in the format\nFormat Example:\nSmall para of introduction and your interpretation\n1. Relevant summary chunk from document 1\n2. Relevant summary chunk from document 2\n3. Relevant summary chunk from document 3\nconsiderations and follow up if necessary.\n\nMention that you are still learning  that will get better with the more questions as you ask it\nIf you feel the user did not frame the question properly, you should ask for a follow up question from the user once you have presented with your interpretation of the answer"
        },
        {
            "role": "user",
            "content": "What is FSI?"
        }
    ]
}

try:
    response = requests.post(url, json=input_data)

    if response.status_code == 200:
        result = response.json()
        user_content = result.get("user_content")
        print("User Content:", user_content)
    else:
        print(f"Error: {response.status_code}, {response.text}")
except requests.RequestException as e:
    print(f"Request failed: {e}")
