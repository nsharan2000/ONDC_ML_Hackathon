# ONDC Hackathon Submission

This is our submission for the ONDC Hackathon. Our application is currently deployed in Google Cloud. You can use Postman or any tool capable of sending GET and POST requests.

**Requirements:**
- Internet connection.
- A valid JSON file with the necessary parameters.

## Step 1: Download and Install Postman

If you don't have Postman installed, you can download it from [Postman Downloads](https://www.postman.com/downloads/). Follow the installation instructions for your operating system.

## Step 2: Prepare JSON Request

Create a JSON file with the following content. This JSON file specifies the model, response format, and messages for the Ondc Work endpoint.

```json
{
    "model": "gpt-4",
    "response_format": {"type": "json_object"},
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful Assistant who is knowledgeable about all PDFs and their data inside it",
            "topic": "Food"
        },
        {
            "role": "user",
            "content": "are there any restrictions on advertisements regarding food and beverages?"
        }
    ]
}



Feel free to modify the "topic" and "content" values according to your specific questions or topics of interest.

Step 3: Send POST Request using Postman
Open Postman and follow these steps:

Set the request type to POST.
Enter the Ondc Work endpoint URL: http://34.29.172.77:80/predict.
Go to the "Body" tab, select "raw," and paste the prepared JSON file.
Click the "Send" button to execute the request.
Step 4: Await Response
After sending the request, wait for a few seconds for the Ondc Work service to process your query. The response will be displayed in the Postman interface.

Explore the response to find the answer to your question or gather insights based on the topic you provided in the JSON file.








This guide provides step-by-step instructions for setting up and running the code to utilize Our RAG model for extracting information from PDF or text files.

## Prerequisites

Before you begin, ensure that the following prerequisites are met:

- Git installed on your machine
- Python (version 3.9 or higher) installed
- An OpenAI API key for GPT-4

## Step 1: Clone the Repository

```bash
git clone https://github.com/SouSingh/DCPR_Backend
cd DCPR_Backend
```


## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

# Step 3: Configure Environment

To configure the environment for using the GPT-4 Document Analysis Tool, follow these steps:

1. **Rename the Environment File:**
   - Locate the `.env.example` file in the root of your project.
   - Rename it to `.env`.

2. **Insert OpenAI API Key:**
   - Open the newly created `.env` file in a text editor.

3. **Add Your OpenAI API Key:**
   - Insert your OpenAI API key in the following format:
     ```ini
     OPENAI_API_KEY="your-api-key"
     ```

   Replace `"your-api-key"` with the actual API key you obtained from OpenAI.

Save the changes to the `.env` file.

With this configuration, the GPT-4 Document Analysis Tool will be able to authenticate with the OpenAI API using your provided key.


# Step 4: Provide Input Data

To analyze a specific PDF or text file, follow these steps:

1. **Locate Your Document:**
   - Identify the PDF or text file that you want to analyze.

2. **Place the Document in the Data Folder:**
   - Navigate to the `Data` folder in the project directory.
   - Copy or move your chosen document into this folder.

   The tool will process files located in the `Data` folder, so make sure your document is placed there before running the application.

Now, you are ready to proceed to the next steps and run the GPT-4 Document Analysis Tool on your provided document.

# Step 5: Run the Application

To run the GPT-4 Document Analysis Tool, follow these steps:

1. **Open a Terminal:**
   - Open a terminal or command prompt on your machine.

2. **Navigate to Your Project Directory:**
   - Change your working directory to the root of your project where the tool is located.
     ```bash
     cd DCPR_Backend
     ```

3. **Run the Application:**
   - Execute the following command to start the application:
     ```bash
     uvicorn main:app --reload
     ```

   The `--reload` flag enables automatic code reloading, which is useful during development.

4. **Access the Application:**
   - Once the application is running, you can access it by opening a web browser and navigating to `http://127.0.0.1:8000/`.

Now, the GPT-4 Document Analysis Tool is up and running. You can proceed to the next steps to send requests and analyze your documents.

# Step 6: Send POST Request

To utilize the GPT-4 Document Analysis Tool and obtain insights from your documents, follow these steps:

1. **Use an API Client:**
   - Choose your preferred API client, such as Postman or cURL.

2. **Send a POST Request:**
   - Send a POST request to `http://127.0.0.1:8000/predict` with the following JSON format:
     ```json
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
     ```

   Customize the topic and question in the JSON payload according to your specific use case.

3. **Review the Response:**
   - You will receive a response with the language model's output, including relevant information related to your question's topic, such as page numbers and context within the provided PDF or text file.

Feel free to experiment with different queries and adapt the JSON payload to suit your document analysis requirements.

# Step 7: Review the Response

After sending a POST request and receiving a response from the GPT-4 Document Analysis Tool, follow these steps to review the obtained insights:

1. **Inspect the Output:**
   - Examine the response received from the tool. It will include information generated by the GPT-4 language model based on the provided query.

2. **Extracted Information:**
   - Look for relevant details related to your question's topic, such as page numbers, context, and any other pertinent information within the provided PDF or text file.

3. **Customize Queries:**
   - If needed, customize the topic and question in the JSON payload sent during the POST request to refine and explore different aspects of the document.

4. **Iterate as Necessary:**
   - Experiment with various queries to extract different insights from your documents.

By following these steps, you can effectively utilize the GPT-4 Document Analysis Tool to gain valuable information from your PDF or text files.

