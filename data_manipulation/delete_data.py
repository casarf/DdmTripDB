from db_connection.mongo_connect import create_connection, close_connection

def db_delete_many(query):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    delete_result = collection.delete_many(query)
    print(f"Deleted {delete_result.deleted_count} documents.")
    
    close_connection(client)
    
def db_delete_one(query):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    delete_result = collection.delete_one(query)
    print(f"Deleted {delete_result} documents.")
    
    close_connection(client)

# Example usage
# if __name__ == "__main__":
#     query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
#     db_delete_many(query)

# Command #5 - Delete a failed restaurant
def delete_failed_restaurant():
    query = {
        "location.city" : 'Milan',
        "price_range.0" : {'$gte' : 50},
        "rating.avg_rating": {'$lte' : 3}
    }
    db_delete_one(query)

# Example usage
if __name__ == "__main__":
    delete_failed_restaurant()