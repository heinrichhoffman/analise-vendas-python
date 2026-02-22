import numpy as np
import pandas as pd

# --- Geração de Dados Fictícios Coerentes ---
print("\nGerando conjunto de dados fictícios...")

# Define a semente para resultados reproduzíveis
np.random.seed(42)

# Criando um dicionário de dados
data = {
    'ID_Pedido': range(1001, 1101),
    'Data_Compra': pd.to_datetime(pd.date_range(start = '2026-07-01', periods = 100, freq ='D')) - pd.to_timedelta(np.random.randint(0, 30, size = 100), unit = 'd'),
    'Cliente_ID': np.random.randint(100, 150, size = 100),
    'Produto': np.random.choice(['Smartphone', 'Notebook', 'Fone de Ouvido', 'Smartwatch', 'Teclado Mecânico'], size = 100),
    'Categoria': ['Eletrônicos', 'Eletrônicos', 'Acessórios', 'Acessórios', 'Acessórios'] * 20,
    'Quantidade': np.random.randint(1, 5, size = 100),
    'Preco_Unitario': [5999.90, 8500.00, 799.50, 2100.00, 850.00] * 20,
    'Status_Entrega': np.random.choice(['Entregue', 'Pendente', 'Cancelado'], size = 100, p = [0.8, 0.15, 0.05])
}

# Criando o dataframe a partir do dicionário
df_vendas = pd.DataFrame(data)

# --- Introduzindo Problemas nos Dados para o Exercício ---
print("\nIntroduzindo problemas nos dados para a limpeza...\n")

# 1. Valores Ausentes (NaN)
df_vendas.loc[5:10, 'Quantidade'] = np.nan
df_vendas.loc[20:22, 'Status_Entrega'] = np.nan
df_vendas.loc[30, 'Cliente_ID'] = np.nan

# 2. Dados Duplicados
df_vendas = pd.concat([df_vendas, df_vendas.head(3)], ignore_index = True)

# 3. Tipos de Dados Incorretos
df_vendas['Preco_Unitario'] = df_vendas['Preco_Unitario'].astype(str)
df_vendas.loc[15, 'Preco_Unitario'] = 'valor_invalido'                   # Simulando um erro de digitação
df_vendas['Cliente_ID'] = df_vendas['Cliente_ID'].astype(str)

# 4. Outliers
df_vendas.loc[50, 'Quantidade'] = 50 # Um valor claramente fora do padrão

print("Dados gerados com sucesso!\n")

df_vendas.to_csv("df_vendas.csv", index=False)
