# Importando as bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Configurando o estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Leitura do arquivo CSV gerado no outro código

df_vendas = pd.read_csv("df_vendas.csv")

# Primeiras linhas
df_vendas.head()

# Últimas linhas
df_vendas.tail()


# Verificando as informações gerais do DataFrame
print("\n--- Informações Gerais do DataFrame (df_vendas.info()) ---\n")
df_vendas.info()

print("\n--- Verificando valores ausentes ---\n")
print(df_vendas.isna().sum())

print("\n--- Verificando a presença de registros duplicados ---\n")
print(f"Número de linhas duplicadas: {df_vendas.duplicated().sum()}")

print("\n--- Estatísticas descritivas para colunas numéricas ---\n")
print(df_vendas.describe())

print("\n--- Estatísticas descritivas para colunas categóricas ---\n")
print(df_vendas.describe(include = [object]))

# Verificando as informações gerais do DataFrame
print("\n--- Tipos de dados ---\n")
df_vendas.dtypes

# Passo 3 - Limpeza e Pré-Processamento dos Dados


# Copiando o DataFrame para manter o original intacto
df_limpo = df_vendas.copy()

# --- 1. Corrigindo Tipos de Dados ---
print("Corrigindo tipos de dados...")
# Convertendo 'Preco_Unitario' para numérico, tratando erros
# errors='coerce' transformará valores inválidos (como 'valor_invalido') em NaN
df_limpo['Preco_Unitario'] = pd.to_numeric(df_limpo['Preco_Unitario'], errors = 'coerce')

# Convertendo 'Cliente_ID' para numérico, tratando erros
df_limpo['Cliente_ID'] = pd.to_numeric(df_limpo['Cliente_ID'], errors = 'coerce').astype('Int64') # Usamos Int64 para permitir NaN

df_limpo.dtypes

"""**A coluna 'Data_Compra' já está no formato correto (datetime64)!**"""

# --- 2. Tratando Valores Ausentes (NaN) ---
print("Tratando valores ausentes...")
# Para 'Quantidade', vamos preencher com a mediana, que é mais robusta a outliers
mediana_qtd = df_limpo['Quantidade'].median()
df_limpo.fillna({'Quantidade': mediana_qtd}, inplace = True)

# Para 'Status_Entrega', podemos preencher com o valor mais frequente (moda)
moda_status = df_limpo['Status_Entrega'].mode()[0]
df_limpo['Status_Entrega'] = df_limpo['Status_Entrega'].fillna(moda_status)

# Para 'Preco_Unitario' e 'Cliente_ID', onde o NaN foi gerado por erro ou falta de informação,
# a melhor abordagem é remover as linhas, pois não podemos inferir esses dados.
df_limpo.dropna(subset = ['Preco_Unitario', 'Cliente_ID'], inplace = True)

# --- 3. Removendo Duplicatas ---
print("Removendo registros duplicados...")
df_limpo.drop_duplicates(inplace = True)

# --- 4. Tratando Outliers ---
# Vamos visualizar o outlier na coluna 'Quantidade'
print("Tratando outliers...")
sns.boxplot(x = df_limpo['Quantidade'])
plt.title('Boxplot de Quantidade (Antes de tratar outlier)')
plt.show()

# Vamos remover valores de 'Quantidade' que estão muito distantes da média.
# Uma abordagem comum é remover valores que estão além de 3 desvios padrão da média.
limite_superior = df_limpo['Quantidade'].mean() + 3 * df_limpo['Quantidade'].std()
df_limpo = df_limpo[df_limpo['Quantidade'] < limite_superior]

# Verificando o resultado
sns.boxplot(x = df_limpo['Quantidade'])
plt.title('Boxplot de Quantidade (Depois de tratar outlier)')
plt.show()

# --- Verificação Final ---
print("\n--- Verificação Final Pós-Limpeza ---\n")
df_limpo.info()
print("\nValores ausentes restantes:\n", df_limpo.isna().sum())
print(f"\nLinhas duplicadas restantes: {df_limpo.duplicated().sum()}")

# Convertendo 'Data_Compra' de texto para formato de data
df_limpo['Data_Compra'] = pd.to_datetime(df_limpo['Data_Compra'])

# Passo 4 - Engenharia de Atributos e Extração de Insights


df_limpo.head()

# --- Feature Engineering: Criando uma nova coluna 'Total_Venda' ---
df_limpo['Total_Venda'] = df_limpo['Quantidade'] * df_limpo['Preco_Unitario']

df_limpo.head()

# 1. Qual o total de receita?
receita_total = df_limpo['Total_Venda'].sum()
print(f"A receita total da loja foi de: R$ {receita_total:,.2f}")

# 2. Qual a receita total por categoria de produto?
receita_por_categoria = df_limpo.groupby('Categoria')['Total_Venda'].sum().sort_values(ascending = False)
print("\n--- Receita Total por Categoria ---\n")
print(receita_por_categoria)

# 3. Qual o produto mais vendido em quantidade?
produto_mais_vendido = df_limpo.groupby('Produto')['Quantidade'].sum().sort_values(ascending = False)
print("\n--- Total de Unidades Vendidas por Produto ---\n")
print(produto_mais_vendido)

# 4. Análise de vendas ao longo do tempo
# Agrupando as vendas por dia
vendas_por_dia = df_limpo.set_index('Data_Compra').resample('D')['Total_Venda'].sum()
print("\n--- Resumo de Vendas por Dia (Primeiros 5 dias) ---\n")
print(vendas_por_dia.head())

"""## Passo 5 - Visualização dos Dados e Análise



Gráficos são essenciais para comunicar os resultados da análise.
"""

import os

# Cria a pasta 'graficos' se ela ainda não existir
if not os.path.exists('graficos'):
    os.makedirs('graficos')

# Gráfico 1: Receita por Categoria
receita_por_categoria.plot(kind = 'bar', color = 'skyblue')
plt.title('Receita Total Por Categoria de Produto')
plt.ylabel('Receita (R$)')
plt.xlabel('Categoria')
plt.xticks(rotation = 0)
plt.savefig('graficos/1_receita_por_categoria.png', dpi=300)
plt.show()

# Gráfico 2: Quantidade Vendida por Produto
produto_mais_vendido.plot(kind = 'barh', color = 'salmon')
plt.title('Quantidade de Unidades Vendidas Por Produto')
plt.ylabel('Produto')
plt.xlabel('Quantidade Vendida')
plt.gca().invert_yaxis() # Inverte o eixo para o maior valor ficar no topo
plt.savefig('graficos/2_quantidade_por_produto.png', dpi=300)
plt.show()

# Gráfico 3: Tendência de Vendas ao Longo do Tempo
vendas_por_dia.plot(kind = 'line', marker = '.', linestyle = '-')
plt.title('Tendência de Vendas Diárias')
plt.ylabel('Receita (R$)')
plt.xlabel('Data da Compra')
plt.grid(True)
plt.savefig('graficos/3_tendencia_vendas_diarias.png', dpi=300)
plt.show()

# Gráfico 4: Distribuição do Status de Entrega

# Conta quantas vezes aparece cada status de entrega
status_counts = df_limpo['Status_Entrega'].value_counts()

plt.pie(
    status_counts,                 # Valores numéricos para cada fatia (quantidade de cada status)
    labels = status_counts.index,  # Rótulos de cada fatia (labels dos status)
    autopct = '%1.1f%%',           # Mostra o percentual em cada fatia com 1 casa decimal
    startangle = 180,              # Ângulo inicial para "girar" o gráfico e escolher onde começa a primeira fatia
    colors = ['lightgreen',        # Cor da primeira fatia
              'orange',            # Cor da segunda fatia
              'lightcoral']        # Cor da terceira fatia
)

plt.title('\nDistribuição do Status de Entrega')  # Título do gráfico
plt.savefig('graficos/5_1status_entrega_destaque.png', dpi=300)
plt.show()                                         # Exibe o gráfico na tela

# Gráfico 4: Distribuição do Status de Entrega no formato 3D

# Conta quantas vezes aparece cada status de entrega
status_counts = df_limpo['Status_Entrega'].value_counts()

# Descobre a posição (índice) da fatia com maior valor para destacá-la
maior_idx = status_counts.argmax()

# Cria a lista explode: desloca 0.1 para a maior fatia e 0 para as outras
explode = [0.1 if i == maior_idx else 0 for i in range(len(status_counts))]

# Define o tamanho da figura (6x6 polegadas)
plt.figure(figsize = (6,6))

plt.pie(
    status_counts,                 # Valores numéricos para cada fatia (quantidade de cada status)
    labels = status_counts.index,  # Rótulos de cada fatia (nomes dos status)
    autopct = '%1.1f%%',           # Mostra o percentual em cada fatia com 1 casa decimal
    startangle = 180,              # Ângulo inicial para "girar" o gráfico e definir onde começa a primeira fatia
    colors = ['lightgreen',        # Cor da primeira fatia
              'orange',            # Cor da segunda fatia
              'lightcoral'],       # Cor da terceira fatia
    explode = explode,             # Desloca a maior fatia para destacá-la visualmente
    shadow = True                  # Adiciona sombra para criar um efeito 3D simples
)

plt.title('\nDistribuição do Status de Entrega\n')  # Define o título do gráfico
plt.axis('equal')                                   # Mantém o formato circular (sem deformações)
plt.savefig('graficos/5_2status_entrega_destaque.png', dpi=300)
plt.show()                                          # Exibe o gráfico

# Gráfico 4: Distribuição dos Status de Entrega com gráfico interativo usando o Plotly

# Importa o pacote Plotly Express para gráficos interativos
import plotly.express as px

# Cria o gráfico de pizza interativo
dsa_fig = px.pie(
    values = status_counts,        # Valores numéricos para cada fatia (quantidade de cada status)
    names = status_counts.index,   # Rótulos de cada fatia (nomes dos status)
    hole = 0,                      # Define o tamanho do "furo" no centro (0 = pizza completa, >0 cria gráfico do tipo donut)
    title = 'Distribuição do Status de Entrega'  # Título exibido no gráfico
)

# Ajusta o destaque das fatias (pull desloca as fatias para fora)
dsa_fig.update_traces(
    pull = [0.05 if i == maior_idx else 0 for i in range(len(status_counts))]
    # Cria uma lista onde a maior fatia é deslocada 0.05 e as outras ficam sem deslocamento
)

# Mostra o gráfico interativo na tela
plt.savefig('graficos/5_3status_entrega_destaque.png', dpi=300)
dsa_fig.show()

