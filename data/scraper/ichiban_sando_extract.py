import psycopg2
from bs4 import BeautifulSoup
from contextlib import contextmanager


class FoodItem:
    """
    Represents a food item with a title, description, and price.
    """
    def __init__(self, title, description, price):
        self.title = title.strip() if title else None
        self.description = description.strip() if description else None
        self.price = price.strip() if price else None

    def __repr__(self):
        return f"FoodItem(title={self.title}, " \
               f"description={self.description}, " \
               f"price={self.price})"
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'price': self.price
        }


class HTMLDataExtractor:

    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_food_item(self, item):
        """
        Extracts title, description, and price of a food item.
        """
        title = item.select_one('.item__title p')
        description = item.select_one('.item__description')
        price = item.select_one('.product-price__wrapper span')
        return FoodItem(title.text if title else None, description.text if description else None, price.text if price else None)

    def extract_food_items(self):
        """
        Extracts food items data from the HTML content.
        """
        food_items = self.soup.select('.item__card')
        return [self.extract_food_item(item) for item in food_items]

@contextmanager
def get_postgres_connection(db_config):
    """
    Context manager to handle PostgreSQL connection.
    """
    conn = psycopg2.connect(**db_config)
    try:
        yield conn
    finally:
        conn.close()

class PostgresDataLoader:
    def __init__(self, db_config):
        self.db_config = db_config

    def insert_data(self, data, table_name):
        """
        Inserts extracted data into PostgreSQL database.
        """
        with get_postgres_connection(self.db_config) as conn:
            with conn.cursor() as cursor:
                for record in data:
                    columns = record.keys()
                    values = [record[column] for column in columns]
                    insert_statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
                    cursor.execute(insert_statement, values)
            conn.commit()


def clean_data(data):
    """
    Helper method to clean extracted data.
    """
    return [
        {key: (value.replace('\t', '') if value else value) for key, value in record.to_dict().items()}
        for record in data
    ]

if __name__ == "__main__":
    file_path = 'html_source/ichiban_sando_order_online_page_source.html'
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        
    extractor = HTMLDataExtractor(html_content)
    extracted_data = extractor.extract_food_items()
    cleaned_data = clean_data(extracted_data)
    # db_config = {
    #     'dbname': 'your_dbname',
    #     'user': 'your_username',
    #     'password': 'your_password',
    #     'host': 'your_host',
    #     'port': 'your_port'
    # }
    
    # data_loader = PostgresDataLoader(db_config)
    # data_loader.insert_data(cleaned_data, 'your_table')