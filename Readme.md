This guide will walk you through the steps to set up and run the code for utilizing the GPT-4 language model to find answers within PDF or text files.

Prerequisites
Git installed on your machine
Python (version 3.6 or higher) installed
An OpenAI API key for GPT-4
Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/SouSingh/DCPR_Backend
cd DCPR_Backend
Step 2: Install Dependencies
bash
Copy code
pip install -r requirements.txt
Step 3: Configure Environment
Rename the .env.example file to .env.

Open the .env file and insert your OpenAI API key in the following format:

ini
Copy code
OPENAI_API_KEY="your-api-key"
Step 4: Provide Input Data
Place your PDF or text file inside the Data folder that you want to analyze.

Step 5: Run the Application
bash
Copy code
uvicorn main:app --reload
Step 6: Send POST Request
Use your preferred API client (e.g., Postman, cURL) to send a POST request to http://127.0.0.1:8000/predict with the following JSON format:

json
Copy code
{
    "model": "gpt-4",
    "response_format": {"type": "json_object"},
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful Assistant who is knowledgeable about all PDF and their data inside it",
            "topic": "Food"
        },
        {
            "role": "user",
            "content": "Are there any restrictions on advertisements regarding food and beverages?"
        }
    ]
}
Step 7: Review the Response
You will receive a response with the language model's output, including relevant information related to your question's topic, such as page numbers and context within the provided PDF or text file.

Feel free to customize the topic and question in the JSON payload according to your specific use case.

Now, you are all set to explore the magic of GPT-4 in extracting insights from your documents!