import pandas as pd
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

# Загрузка модели и токенизатора
model_name = "ai-forever/rugpt3small_based_on_gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Чтение данных из Excel
df = pd.read_excel("L_proceed.xlsx")  # замените на ваш файл

# Подготовка данных в формат "вход -> выход"
df['text'] = df.apply(
    lambda row: f"Заявка: {row['A']}\nГруппа: {row['B']}\nЗадача: {row['C']}\nКритичность: {row['D']}\n",
    axis=1
)

# Преобразование в Dataset
dataset = Dataset.from_pandas(df[['text']])
eval_dataset = Dataset.from_pandas(df[['text']])

# Настройка LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["c_attn", "c_proj", "wte", "mlp.c_proj"]
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Параметры обучения
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    save_steps=500,
    logging_steps=100,
    learning_rate=2e-4,
    fp16=True,
    warmup_ratio=0.1,
    optim="adamw_torch",
    report_to="none"
)
# Тренировочный цикл
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Запуск обучения
trainer.train()

# Сохранение модели
model.save_pretrained("./fine_tuned_model_small")
tokenizer.save_pretrained("./fine_tuned_model_small")