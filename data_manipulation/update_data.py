from db_connection.mongo_connect import create_connection

def update_data(query, new_values):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    
    update_result = collection.update_many(query, {'$set': new_values})
    print(f'Updated {update_result.modified_count} documents.')

# Example usage
if __name__ == "__main__":
    query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
    new_values = {
        'availability.original_open_hours.Mon': ['08:00-22:30'],
        'availability.original_open_hours.Tue': ['08:00-22:30'],
        'availability.original_open_hours.Wed': ['08:00-22:30'],
        'availability.original_open_hours.Thu': ['08:00-22:30'],
        'availability.original_open_hours.Fri': ['08:00-22:30'],
        'availability.original_open_hours.Sat': ['08:00-22:30'],
    }
    
    update_data(query, new_values)
