from db_connection.mongo_connect import create_connection

def find_and_print_data(query):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    documents = collection.find(query)
    
    for document in documents:
        print(document)

def find_restaurant_by_link(restaurant_link):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    restaurant = collection.find_one({'restaurant_link': restaurant_link}, {'rating': 1})
    return restaurant

# Example usage
if __name__ == "__main__":
    query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
    find_and_print_data(query)
