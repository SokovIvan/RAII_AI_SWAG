from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True)  # Для экономии памяти

# Настройка LoRA
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, peft_config)

# Параметры обучения
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=100,
    learning_rate=2e-5,
    fp16=True
)

# Тренировка
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,  # Ваш датасет в формате Dataset
    peft_config=peft_config,
    args=training_args,
    formatting_func=formatting_func  # Функция для форматирования данных
)

trainer.train()