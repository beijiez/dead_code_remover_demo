from transformers import pipeline

class DeadCodeAIExplainer:
    def __init__(self, model_name="EleutherAI/gpt-neo-1.3B", device=0):
        self.pipe = pipeline("text-generation", model=model_name, device=device)

    def explain_dead_code(self, function_code: str):
        prompt = (
            "### Task: Explain why the below dead Function code below is never executed, in one sentence.\n\n"
            f"{function_code}\n\n"
            "### Explanation: This function is never called, because \n"
        )
        result = self.pipe(prompt, max_new_tokens=100)[0]["generated_text"]
        return result.split("### Explanation:")[-1].strip()
