import pandas as pd
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
from huggingface_hub import login
login("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")

# 1. Загрузка и подготовка данных
def load_and_prepare_data(excel_path):
    # Чтение Excel файла
    df = pd.read_excel(excel_path)

    # Объединение столбцов B и D в выходной текст
    df['output'] = "Группа: " + df['B'].astype(str) + "; Краткая формулировка: " + df['D'].astype(str)

    # Создание промптов в формате для обучения
    df['text'] = df.apply(lambda row: f"Заявка пользователя: {row['A']}\nОтвет: {row['output']}", axis=1)

    # Преобразование в формат Dataset
    dataset = Dataset.from_pandas(df[['text']])
    return dataset


# 2. Загрузка модели и токенизатора
model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Установка pad_token
print("start")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map="auto"
)

# 3. Настройка LoRA
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]  # Для Mistral
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# 4. Параметры обучения
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    optim="paged_adamw_32bit",
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    save_strategy="epoch",
    logging_steps=10,
    num_train_epochs=3,
    max_steps=-1,
    fp16=True,
    push_to_hub=False
)

# 5. Создание тренера
trainer = SFTTrainer(
    model=model,
    train_dataset=load_and_prepare_data("L_proceed.xlsx"),  # Укажите путь к вашему Excel файлу
    peft_config=peft_config,
    dataset_text_field="text",
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=training_args,
    packing=False
)

# 6. Обучение
trainer.train()

# 7. Сохранение модели
trainer.save_model("fine_tuned_mistral")
tokenizer.save_pretrained("fine_tuned_mistral")