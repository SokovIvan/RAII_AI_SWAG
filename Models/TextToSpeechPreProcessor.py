import pandas as pd
# Чтение Excel-файла
file_path = "L_proceed.xlsx"
df = pd.read_excel(file_path)

# Если столбец 'А'
if 'A' in df.columns:
    for i in df['A']:
        print(i)