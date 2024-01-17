from llmware.prompts import Prompt
from llmware.configs import LLMWareConfig
import os
from fastapi.responses import StreamingResponse




def contract_analysis_w_fact_checking(text):

    contracts_path = "./Data"

    # create prompt object
    prompter = Prompt().load_model("gpt-4", api_key=f"{os.getenv('OPENAI_API_KEY')}", from_hf=False)

    research = {"topic": "DCPR", "prompt": f"{text}"}

    for i, contract in enumerate(os.listdir(contracts_path)):

        print("\nAnalyzing Contract - ", str(i+1), contract)

        print("Question: ", research["prompt"])

        # contract is parsed, text-chunked, and then filtered by "base salary'
        source = prompter.add_source_document(contracts_path, contract, query=research["topic"])

        # calling the LLM with 'source' information from the contract automatically packaged into the prompt
        responses = prompter.prompt_with_source(research["prompt"], prompt_name="just_the_facts", temperature=0.3)

        # run several fact checks
        ev_numbers = prompter.evidence_check_numbers(responses)
        ev_sources = prompter.evidence_check_sources(responses)
        ev_stats = prompter.evidence_comparison_stats(responses)
        z = prompter.classify_not_found_response(responses, parse_response=True, evidence_match=True,ask_the_model=False)

        for r, response in enumerate(responses):

            print("LLM Response: ", response["llm_response"])
            print("Sources: ", ev_sources[r]["source_review"])
            print("Stats: ", ev_stats[r]["comparison_stats"])
            print("Not Found Check: ", z[r])

            # We're done with this contract, clear the source from the prompt
            prompter.clear_source_materials()

    # Save jsonl report to jsonl to /prompt_history folder
    print("\nupdate: prompt state saved at: ", os.path.join(LLMWareConfig.get_prompt_path(),prompter.prompt_id))

    prompter.save_state()

#saifu19
text = "what is FSI?"
contract_analysis_w_fact_checking(text)
