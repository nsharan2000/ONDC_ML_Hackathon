from fastapi import FastAPI, Path, Body, HTTPException
from llmware.prompts import Prompt
from llmware.configs import LLMWareConfig
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import uvicorn

load_dotenv()

app = FastAPI()

api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def print_json(obj):
    json_str = obj.model_dump_json()
    parsed_json = json.loads(json_str)
    return parsed_json

@app.post('/assistant')
async def threadscall(data: dict = Body(...)):
    token = data.get("token")
    client = OpenAI(api_key=token)
    assistant = client.beta.assistants.create(
            name="DCPR Bot",
            instructions="You are DCPR Assistant who is knowldgeable about development regulations for the buildings in mumbai. Use the following pieces of retrieved context to answer the question. Always answer like a human and do not mention that you are just reading from context documents. If you are very sure about the answer, give a very straightforward answer. ALways look for the answer in the knowledge base before any assumption\nIf you are not completely sure about the answer. Present your answer in the format\nFormat Example:\nSmall para of introduction and your interpretation\n1. Relevant summary chunk from document 1\n2. Relevant summary chunk from document 2\n3. Relevant summary chunk from document 3\nconsiderations and follow up if necessary.\n\nMention that you are still learning  that will get better with the more questions as you ask it\nIf you feel the user did not frame the question properly, you should ask for a follow up question from the user once you have presented with your interpretation of the answer",
            model="gpt-4-1106-preview",)
    return print_json(assistant)

@app.post('/threads')
async def threadscall(data: dict = Body(...)):
    token = data.get("token")
    client = OpenAI(api_key=token)
    thread = client.beta.threads.create()
    return print_json(thread)

@app.post('/threads/threadId/messages')
async def messages(
    data: dict = Body(...)):  
    threadId = data.get('threadId')
    print(threadId)
    content = data.get('content')
    print(content)
    token = data.get('token')
    print(token)

    if not content or not token:
        raise HTTPException(status_code=400, detail="Content and token are required in the request.")

    try:
        client = OpenAI(api_key=token)
        message = client.beta.threads.messages.create(
            thread_id=threadId,
            role="user",
            content=f"{content}"
        )
        return message
    except NotFoundError as not_found_error:
        raise HTTPException(status_code=404, detail=f"Thread not found with id '{threadId}'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")

@app.post('/threads/threadId/runs')
async def messages(
    data: dict = Body(...)):  
    threadId = data.get('threadId')
    print(threadId)
    assistantID = data.get('assistantID')
    print(assistantID)
    token = data.get('token')
    print(token)

    if not assistantID or not token:
        raise HTTPException(status_code=400, detail="Content and token are required in the request.")

    try:
        client = OpenAI(api_key=token)
        run = client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=assistantID,
            )
        return run
    except NotFoundError as not_found_error:
        raise HTTPException(status_code=404, detail=f"Thread not found with id '{threadId}'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")

@app.post('/threads/threadID/runs/runID')
async def messages(
    data: dict = Body(...)):  
    threadId = data.get('threadId')
    print(threadId)
    runId = data.get('runID')
    print(runId)
    token = data.get('token')
    print(token)

    if not runId or not token:
        raise HTTPException(status_code=400, detail="Content and token are required in the request.")

    try:
        client = OpenAI(api_key=token)
        run = client.beta.threads.runs.retrieve(
            thread_id=threadId,
            run_id=runId,
            )
        return run
    except NotFoundError as not_found_error:
        raise HTTPException(status_code=404, detail=f"Thread not found with id '{threadId}'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")

@app.post('/threads/threadID/messages')
async def messages(
    data: dict = Body(...)):  
    threadId = data.get('threadId')
    print(threadId)
    token = data.get('token')
    print(token)

    try:
        client = OpenAI(api_key=token)
        run = client.beta.threads.messages.list(
            thread_id=threadId)
        print(run.data[1].content[0].text.value)
        return run
    except NotFoundError as not_found_error:
        raise HTTPException(status_code=404, detail=f"Thread not found with id '{threadId}'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")


@app.post("/contract-analysis")
async def contract_analysis_w_fact_checking(data: dict = Body(...)):
    text = data.get("text")

    if not text:
        raise HTTPException(status_code=400, detail="Text field is required in the input data.")

    contracts_path = "./Data"

    # create prompt object
    prompter = Prompt().load_model("gpt-4", api_key=os.getenv('OPENAI_API_KEY'), from_hf=False)

    research = {"topic": "DCPR", "prompt": f"{text}"}

    # Results will be stored in this list
    results = []

    for i, contract in enumerate(os.listdir(contracts_path)):
        print("\nAnalyzing Contract - ", str(i+1), contract)

        print("Question: ", research["prompt"])

        source = prompter.add_source_document(contracts_path, contract, query=research["topic"])

        responses = prompter.prompt_with_source(research["prompt"], prompt_name="just_the_facts", temperature=0.3)

        ev_numbers = prompter.evidence_check_numbers(responses)
        ev_sources = prompter.evidence_check_sources(responses)
        ev_stats = prompter.evidence_comparison_stats(responses)
        z = prompter.classify_not_found_response(responses, parse_response=True, evidence_match=True, ask_the_model=False)

        contract_results = []

        for r, response in enumerate(responses):
            contract_results.append({
                "LLM Response": response["llm_response"],
                "Sources": ev_sources[r]["source_review"],
                "Stats": ev_stats[r]["comparison_stats"],
                "Not Found Check": z[r]
            })

        

        results.append(contract_results)

        prompter.clear_source_materials()

    print("\nupdate: prompt state saved at: ", os.path.join(LLMWareConfig.get_prompt_path(), prompter.prompt_id))
    prompter.save_state()

    return {"results": results}


