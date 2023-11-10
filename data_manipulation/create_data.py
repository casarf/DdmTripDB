from db_connection.mongo_connect import create_connection, close_connection
from bson import ObjectId

def db_insert_data(data):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    
    # Insert a single document
    insertion_result = collection.insert_one(data)
    print(f'Inserted document with id: {insertion_result.inserted_id}')
    close_connection(client)
    return insertion_result.inserted_id

# Example usage
if __name__ == '__main__':
    sample_data = {
        '_id': ObjectId(),  # Generating a new ObjectId
        'restaurant_link': 'g187079-d1234567',
        'restaurant_name': 'La Bonne Fourchette',
        'location': {
            'country': 'Italy',
            'region': 'Lombardy',
            'province': 'Milan',
            'city': 'Milan',
            'address': '123 Via Bella, 20121, Milan Italy',
            'latitude': 45.464664,
            'longitude': 9.188540
        },
        'claimed': True,
        'awards': ['Certificate of Excellence 2019'],
        'popularity_detailed': '#20 of 50 Coffee & Tea in Milan',
        'popularity_generic': '#150 of 3000 places to eat in Milan',
        'top_tags': ['Family', 'Dessert', 'Italian'],
        'price_level': ['€€-€€€'],
        'price_range': ['€15', '€30'],
        'food_specification': {
            'cuisines': ['Italian', 'Cafe'],
            'special_diets': ['Vegetarian Friendly', 'Vegan Options'],
            'vegetarian_friendly': True,
            'vegan_options': True,
            'gluten_free': True
        },
        'availability': {
            'meals': ['Breakfast', 'Lunch', 'Dinner'],
            'features': ['Reservations', 'Seating', 'Wheelchair Accessible'],
            'original_open_hours': {
                'Mon': ['08:00-20:00'],
                'Tue': ['08:00-20:00'],
                'Wed': ['08:00-20:00'],
                'Thu': ['08:00-20:00'],
                'Fri': ['08:00-22:00'],
                'Sat': ['08:00-22:00'],
                'Sun': ['10:00-18:00']
            },
            'open_days_per_week': 7,
            'open_hours_per_week': 74,
            'working_shifts_per_week': 14
        },
        'rating': {
            'avg_rating': 4.5,
            'total_reviews_count': 320,
            'default_language': 'Italian',
            'reviews_count_in_default_language': 280,
            'excellent': 250,
            'very_good': 50,
            'average': 10,
            'poor': 5,
            'terrible': 5,
            'food': 4.5,
            'service': 4.5,
            'value': 4.0,
            'atmosphere': 4.0,
            'keywords': ['cozy', 'family-friendly', 'traditional']
        }
    }
    db_insert_data(sample_data)
