from db_connection.mongo_connect import create_connection
import datetime

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

# Query 2 - Top Five Vegan Restaurants in Milan
def top_vegan_restaurant_in(city):
    
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    
    restaurants = collection.find(
    {
        'location.city': city,
        'food_specification.vegetarian_friendly': True
    }).sort(
    {
        'rating.avg_rating': -1
    }).limit(5)
    
    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['restaurant_name']}")

# Query 4 - Top Five Vegan Restaurants in Milan
def currently_open_restaurants_in(city):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    

    now = datetime.datetime.now()

    # get weekday name
    current_day = now.strftime('%A')[:3]
    print('Current Day Name:', current_day)

    current_time = now.strftime("%H:%M")
    print("Current Time =", current_time)
    
    
    restaurants = collection.find(
    {
        'location.city': city,
        'availability.original_open_hours': {'$ne': ""}
    }).limit(100)
    
    open_restaurants = []
    
    for el in restaurants:
        
        open_hours = el["availability"]["original_open_hours"]
        
        if len(open_hours[current_day]) == 0:
            continue
        else:
            for r in open_hours[current_day]:
                if (is_current_time_in_range(r)):
                    open_restaurants.append(el)
                    break
                    
    if (len(open_restaurants) == 0):    
        print("\nNo open restaurants")
        return
    
    print("\nOpen restaurants:")
    
    
    for index, el in enumerate(open_restaurants, start=1):
        print(f"Restaurant #{index}: {el['_id']} {el['restaurant_name']}")
        
# helper function for query #4
def is_current_time_in_range(range):
    #'09:00-15:00'
    start_time, end_time = range.split("-")
    start_time = start_time.split(':')
    end_time = end_time.split(':')
    
    now = datetime.datetime.now()
    current_time = current_time = now.strftime("%H:%M").split(":")

    start = datetime.time(int(start_time[0]),int(start_time[0]))
    end = datetime.time(int(end_time[0]),int(end_time[0]))
    current = datetime.time(int(current_time[0]),int(current_time[0]))
    # current = datetime.time(3,0,0)
    
    return start  <= current <= end
    
#Query 6 - Top Five Resturant respecting a budget in Milan
def top_resturant_respecting_the_budget(city, budget):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    
    restaurants = collection.find(
    {
        'location.city': city,
        'food_specification.vegetarian_friendly': True,
        'price_range.0': {'$lte':budget}
    }).sort(
    {
        'rating.avg_rating': -1
    }).limit(5)
    
    print('Done')
    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['_id']} {el['restaurant_name']}")


# Query 8 - Best Pizza in Rome!
def find_by_tags_and_rating_in(city, tags):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    restaurants = collection.find(
    {
        'location.city': city,
        'top_tags': {'$in': tags},
        'rating.food': { '$gte': 4.5 },
        'rating.avg_rating': { '$gte': 4.5 }
    }).sort(
    {
        'rating.avg_rating': -1
    }).limit(5)
    
    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['_id']} {el['restaurant_name']}")
        
# Query 10 - Breakfast in Paris with Free Wifi!
def find_meal_type_and_features_in(city, meal_type, features):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    
    restaurants = collection.find(
    {
        'location.city': city,
        'availability.meals': {'$in': meal_type},
        'availability.features': {'$in': features},
    }).sort(
    {
        'rating.avg_rating': -1
    }).limit(5)
    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['_id']} {el['restaurant_name']}")


# Example usage
if __name__ == "__main__":
    # query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
    # find_and_print_data(query)
    
    # Query 2 run sample
    # city = 'Milan'
    # top_vegan_restaurant_in(city)
    
    # Query 4 run sample
    # city = 'Milan'
    # currently_open_restaurants_in(city)
    
    # Query 6 run sample
    # city = 'Milan'
    # budget = 30
    # top_resturant_respecting_the_budget(city,budget)
    
    # Query 8 run sample
    # city = 'Rome'
    # tags = ['Pizza']
    # find_by_tags_and_rating_in(city, tags)
    
    # Query 10 run sample
    
    city = 'Paris'
    features = ['Free Wifi']
    meal_type = ['Breakfast']
    find_meal_type_and_features_in(city,meal_type,features)
    