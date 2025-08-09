from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

class TunedLLMUsage:
    def __init__(self, modelName="fine_tuned_model_small"):
        self.model = AutoModelForCausalLM.from_pretrained(modelName, local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(modelName, local_files_only=True)
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def parse_response(self, generated_text):
        if generated_text.startswith("Заявка:"):
            generated_text = generated_text.split("Заявка:", 1)[1].strip()
        lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
        request = lines[0] if len(lines) > 0 else generated_text
        group = lines[1].split(":")[1].strip() if len(lines) > 1 and ":" in lines[1] else "Не указано"
        task = lines[2].split(":")[1].strip() if len(lines) > 2 and ":" in lines[2] else "Не указано"
        return {
            "request": request,
            "group": group,
            "task": task
        }

    def generate_response(self, prompt):
        full_prompt = f"Заявка: {prompt}"
        output = self.generator(full_prompt, max_length=200, num_return_sequences=1)
        generated_text = output[0]['generated_text']
        return self.parse_response(generated_text)


if __name__ == "__main__":
    llm = TunedLLMUsage("fine_tuned_model_small")
    result = llm.generate_response("Прошу демонтировать лампу во втором подъезде по причине излишней яркости")
    print("Полный ответ:", result)
    print(f"Заявка: {result['request']}")# Не использовать
    print(f"Группа: {result['group']}")
    print(f"Задача: {result['task']}")
