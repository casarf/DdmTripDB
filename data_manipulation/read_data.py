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

def top_vegan_restaurant_in(city):
    
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    
    restaurants = collection.find(
    {
        'location.city': 'Milan',
        'food_specification.vegetarian_friendly': True
    }).sort(
    {
        'rating.avg_rating': -1
    }).limit(5)
    
    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['restaurant_name']}")


# Example usage
if __name__ == "__main__":
    # query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
    # find_and_print_data(query)
    
    city = 'Milan'
    top_vegan_restaurant_in(city)

