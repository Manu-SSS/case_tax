import requests
import pandas as pd

# Definir os termos de busca
search_terms = ['Xiaomi Chromecast', 'Google Home', 'Apple TV', 'Amazon Fire TV']

# Token de autorização
auth_token = 'TEST-6489612012985364-052415-a8cbe516bf2af6c109b5d36c4dac6d71-790512386'

# Lista para armazenar todos os IDs de itens
item_ids = []

# Função para buscar itens de um termo
def fetch_search_results(search_term, limit=50, offset=0):
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={search_term}&limit={limit}&offset={offset}"
    response = requests.get(url)
    response.raise_for_status()  # Levanta um erro se a requisição falhar
    return response.json()

# Iterar sobre os termos de busca para coletar IDs
for term in search_terms:
    offset = 0
    while True:
        results = fetch_search_results(term, limit=50, offset=offset)
        if results and 'results' in results:
            for item in results['results']:
                item_ids.append(item['id'])
            offset += 50
            if len(results['results']) < 50:
                break
        else:
            break

print(f"Total de IDs coletados: {len(item_ids)}")

# Função para obter detalhes de um item
def fetch_item_details(item_id, token):
    url = f'https://api.mercadolibre.com/items/{item_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
    return response.json()

# Lista para armazenar todos os detalhes dos itens
all_items_details = []

# Iterar sobre todos os IDs de itens coletados
for item_id in item_ids:
    item_details = fetch_item_details(item_id, auth_token)
    
    # Extrair apenas os campos desejados
    desired_fields = {
        'id': item_details['id'],
        'site_id': item_details['site_id'],
        'title': item_details['title'],
        'seller_id': item_details['seller_id'],
        'category_id': item_details['category_id'],
        'price': item_details['price'],
        'initial_quantity': item_details['initial_quantity'],
        'condition': item_details['condition'],
        'base_price': item_details['base_price']
    }
    
    # Extrair informações dos atributos
    attributes = item_details.get('attributes', [])
    for attribute in attributes:
        if attribute['id'] in ['BRAND', 'GENERATION', 'MODEL']:
            attr_name = attribute.get('value_name', '')
            if isinstance(attr_name, str):
                desired_fields[attribute['id'].lower()] = attr_name.lower()
            else:
                desired_fields[attribute['id'].lower()] = attr_name

    all_items_details.append(desired_fields)

print(f"Total de detalhes de itens coletados: {len(all_items_details)}")

# Criar DataFrame com os dados coletados
df = pd.DataFrame(all_items_details)

# Salvar em um arquivo CSV para análise posterior
output_file = 'mercadolivre_items_details.csv'
df.to_csv(output_file, index=False)

print(f"Dados salvos em '{output_file}'")
