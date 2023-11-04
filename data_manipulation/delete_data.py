from db_connection.mongo_connect import create_connection

def delete_data(query):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    delete_result = collection.delete_many(query)
    print(f"Deleted {delete_result.deleted_count} documents.")

# Example usage
if __name__ == "__main__":
    query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
    delete_data(query)
