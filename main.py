from fastapi import FastAPI, HTTPException
from llmware.prompts import Prompt
from llmware.configs import LLMWareConfig
import openai
from dotenv import load_dotenv
import os
import json
import uvicorn

load_dotenv()

app = FastAPI()

api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

def contract_analysis_w_fact_checking(text):
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
                "Sources": [{
                    "text": source["text"],
                    "match_score": source["match_score"],
                    "source": source["source"],
                    "page_num": source.get("page_num", None)
                } for source in ev_sources[r]["source_review"]],
                "Stats": {
                    "percent_display": ev_stats[r]["comparison_stats"]["percent_display"],
                    "confirmed_words": ev_stats[r]["comparison_stats"]["confirmed_words"],
                    "unconfirmed_words": ev_stats[r]["comparison_stats"]["unconfirmed_words"],
                    "verified_token_match_ratio": ev_stats[r]["comparison_stats"]["verified_token_match_ratio"],
                    "key_point_list": [{
                        "key_point": key_point["key_point"],
                        "entry": key_point["entry"],
                        "verified_match": key_point["verified_match"]
                    } for key_point in ev_stats[r]["comparison_stats"]["key_point_list"]]
                },
                "Not Found Check": {
                    "parse_llm_response": False,
                    "evidence_match": True,
                    "not_found_classification": z[r]["not_found_classification"]
                }
            })

        results.append({
            "retrieved_chunks": contract_results
        })

        prompter.clear_source_materials()

    print("\nupdate: prompt state saved at: ", os.path.join(LLMWareConfig.get_prompt_path(), prompter.prompt_id))
    prompter.save_state()

    return {"status": "success", "message": "Chat completion successful", "model_response": results}

@app.post("/predict")
async def predict(data: dict):
    try:
        messages = data.get("messages", [])
        user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), None)
        out = contract_analysis_w_fact_checking(user_message)
        if user_message:
            return {"user_content": out}
        else:
            raise HTTPException(status_code=400, detail="User message not found in input.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"Hello": "World"}