import json
from bs4 import BeautifulSoup

# Load the HTML content
with open('html_source/doordash_taku_sando_order_online_page_source.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract JSON-LD (menu items) from the script tag
script_tags = soup.find_all('script', type='application/ld+json')
menu_list = []

for script in script_tags:
    try:
        data = json.loads(script.string)
        # If the data is a Menu type, extract the items
        if data.get('@type') == 'Menu':
            for section in data.get('hasMenuSection', []):
                if isinstance(section, dict):
                    for item in section.get('hasMenuItem', []):
                        menu_item = {
                            'name': item.get('name', 'No name'),
                            'description': item.get('description', 'No description'),
                            'price': item.get('offers', {}).get('price', 'No price')
                        }
                        menu_list.append(menu_item)
                elif isinstance(section, list):
                    for subsection in section:
                        for item in subsection.get('hasMenuItem', []):
                            menu_item = {
                                'name': item.get('name', 'No name'),
                                'description': item.get('description', 'No description'),
                                'price': item.get('offers', {}).get('price', 'No price')
                            }
                            menu_list.append(menu_item)
    except json.JSONDecodeError:
        continue

# Print the extracted menu items
print(f"Extracted {len(menu_list)} menu items:")
for menu_item in menu_list:
    print(f"Name: {menu_item['name']}")
    print(f"Description: {menu_item['description']}")
    print(f"Price: {menu_item['price']}")
    print('---')