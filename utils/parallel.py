from concurrent.futures import ThreadPoolExecutor
from models.openai_model import openai_response
from models.llama_model import llama_response
from models.geminiai_model import gemini_response


def run_parallel(promt, models):
    results = {}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            "OpenAI": executor.submit(openai_response, promt),
            "Llama": executor.submit(llama_response, promt),
            "Gemini": executor.submit(gemini_response, promt),
            
        }
        
        for model, future in futures.items():
            try:
                results[model] = future.result()
            except Exception as e:
                results[model] = f"Error: {str(e)}"
    return results
