# analise-vendas-python
Análise Exploratória de Dados (EDA) de uma loja varejista utilizando Pandas, Matplotlib, Seaborn e Plotly.

# 📊 Análise Exploratória de Dados de Vendas com Python

Um pipeline completo de Análise de Dados desenvolvido em Python, passando pelas etapas de extração, limpeza, engenharia de atributos (Feature Engineering) e visualização interativa. Este projeto tem como objetivo extrair *insights* valiosos de um conjunto de dados de vendas de uma loja varejista.

## 🚀 O que este projeto faz?

O script `mini_projeto_4.py` executa as seguintes etapas:
1. **Importação de Dados:** Leitura de dados transacionais a partir de um arquivo CSV.
2. **Análise Exploratória Inicial (EDA):** Verificação de tipos de dados, informações gerais e estatísticas descritivas.
3. **Limpeza e Pré-processamento:**
   - Correção de tipos de dados (conversão para numérico e datetime).
   - Tratamento de valores ausentes (imputação pela mediana e moda).
   - Remoção de registros duplicados e dados nulos não recuperáveis.
   - Identificação e tratamento de *outliers* na quantidade de produtos usando a Regra Empírica (3 desvios padrões).
4. **Engenharia de Atributos:** Criação da variável `Total_Venda` (Quantidade x Preço Unitário).
5. **Geração de Insights:** - Cálculo de receita total.
   - Produtos mais vendidos.
   - Tendência de vendas diárias.
6. **Visualização de Dados:** Geração de gráficos estáticos e interativos exportados automaticamente para a pasta `/graficos`.

## 🛠️ Tecnologias e Bibliotecas Utilizadas

- **[Python 3.x](https://www.python.org/)**
- **[Pandas](https://pandas.pydata.org/)** (Manipulação e Análise de Dados)
- **[NumPy](https://numpy.org/)** (Computação Numérica)
- **[Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/)** (Visualizações Estáticas)
- **[Plotly Express](https://plotly.com/python/)** (Visualizações Interativas)

## 📈 Gráficos Gerados

O script gera e salva automaticamente os seguintes gráficos na pasta `graficos/`:
- `1_receita_por_categoria.png`: Gráfico de barras da receita total por categoria.
- `2_quantidade_por_produto.png`: Gráfico de barras horizontais dos produtos mais vendidos.
- `3_tendencia_vendas_diarias.png`: Gráfico de linhas da evolução da receita diária.
- `5_2status_entrega_destaque.png`: Gráfico de pizza (com efeito 3D) do status de entrega.
- `5_3status_entrega_interativo.html`: Gráfico interativo exportado via Plotly.

## ⚙️ Como executar na sua máquina

1. Clone este repositório:
   ```bash
   git clone [https://github.com/heinrichhoffman/analise-vendas-python.git](https://github.com/heinrichhoffman/analise-vendas-python.git)
   cd analise-vendas-python
   pip install pandas numpy matplotlib seaborn plotly
   python mini_projeto_4.py
