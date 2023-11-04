from db_connection.mongo_connect import create_connection

def find_data(query):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    documents = collection.find(query)
    
    for document in documents:
        print(document)

# Example usage
if __name__ == "__main__":
    query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
    find_data(query)
