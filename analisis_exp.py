import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados do arquivo CSV
df = pd.read_csv('mercadolivre_items_details.csv')

# Quantidade de modelos por marca
model_count_by_brand = df.groupby('brand')['model'].nunique().sort_values(ascending=False)

# Preço médio por modelo
average_price_by_model = df.groupby('model')['price'].mean().sort_values(ascending=False)

# Exibir tabela de preço médio por modelo
print("Preço Médio por Modelo:")
print(average_price_by_model)
print()

# Variedade de modelos por marca
plt.figure(figsize=(12, 6))
model_count_by_brand.plot(kind='bar')
plt.title('Quantidade de Modelos por Marca')
plt.xlabel('Marca')
plt.ylabel('Quantidade de Modelos')
plt.xticks(rotation=45)

# Adicionar rótulos de dados
for i in range(len(model_count_by_brand)):
    plt.text(i, model_count_by_brand.iloc[i] * 1.02, model_count_by_brand.iloc[i], ha='center')

plt.show()

# Três modelos mais comuns (maior disponibilidade)
top_common_models = df.groupby(['brand', 'model'])['initial_quantity'].sum().nlargest(3)

# Três modelos mais baratos com suas marcas e preços
top_cheapest_models = df.groupby(['brand', 'model'])['price'].mean().nsmallest(3)

# Quantidade de itens por modelo dividido por marca
plt.figure(figsize=(16, 8))

# Loop sobre as marcas
for i, brand in enumerate(df['brand'].unique()):
    plt.subplot(2, 2, i+1)
    data = df[df['brand'] == brand]
    item_count_by_model = data.groupby('model')['initial_quantity'].sum().sort_values(ascending=False)
    item_count_by_model.plot(kind='bar')
    plt.title(f'Quantidade Disponível por Modelo - {brand}')
    plt.xlabel('Modelo')
    plt.ylabel('Quantidade Disponível')
    plt.xticks(rotation=45)

    # Adicionar rótulos de dados
    for j in range(len(item_count_by_model)):
        plt.text(j, item_count_by_model.iloc[j] * 1.02, item_count_by_model.iloc[j], ha='center')

plt.tight_layout()
plt.show()

# Imprimir os resultados
print("Três Modelos Mais Comuns (Maior Disponibilidade):")
print(top_common_models)
print()

print("Três Modelos Mais Baratos e Suas Marcas (Média de Preço por Modelo):")
print(top_cheapest_models)
print()
