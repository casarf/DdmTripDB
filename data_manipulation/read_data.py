from db_connection.mongo_connect import create_connection, close_connection
from geopy.distance import geodesic
from datetime import datetime


def db_find_one(query):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    document = collection.find_one(query)
    close_connection(client)

    return document


def db_find_many(query, order='', value_limit=''):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    documents = []
    
    if (order != '') and (value_limit != ''):
        documents = list(collection.find(query).sort(order).limit(value_limit))
    elif value_limit != '':
        documents = list(collection.find(query).limit(value_limit))
    elif order != '':
        documents = list(collection.find(query).sort(order))
    else:
        documents = list(collection.find(query))
    
    close_connection(client)
    
    return documents
    
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

    restaurant = collection.find_one(
        {'restaurant_link': restaurant_link}, {'rating': 1})

    return restaurant

# Query 1 - Find restaurant by latitude and longitude
def find_restaurants_nearby(country, region, user_location, max_distance_km=10):

    # MongoDB query to filter by country and region
    query = {
        'location.country': country,
        'location.region': region
    }

    # Fetch restaurants in the specified country and region from the database (first filter)
    filtered_restaurants = db_find_many(query)

    # Filter restaurants based on distance
    nearby_restaurants = []
    for restaurant in filtered_restaurants:
        # Extract the latitude and longitude of the restaurant
        restaurant_location = (
            restaurant['location']['latitude'],
            restaurant['location']['longitude']
        )

        # Calculate the distance from the user's location
        distance = geodesic(user_location, restaurant_location).kilometers

        # Check if the restaurant is within the specified maximum distance
        if distance <= max_distance_km:
            nearby_restaurants.append((restaurant, distance))

    # Return the filtered list of nearby restaurants with distance
    return nearby_restaurants

# Query 2 - Top Five Vegan Restaurants in Milan
def top_vegan_restaurant_in(city):

    query = {
        'location.city': city,
        'food_specification.vegetarian_friendly': True
    }
    order = {
        'rating.avg_rating': -1
    }
    value_limit = 5

    restaurants = db_find_many(query, order, value_limit)

    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['restaurant_name']}")

# Query 3 - Accessibility in different countries
def compute_percentage_wheelchair_accessible_by_country():
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    # Aggregation pipeline for MongoDB query
    pipeline = [
        {
            "$group": {
                "_id": "$location.country",
                "total": {"$sum": 1},
                "wheelchair_accessible_count": {
                    "$sum": {
                        "$cond": [{"$in": ["Wheelchair Accessible", "$availability.features"]}, 1, 0]
                    }
                }
            }
        },
        {
            "$project": {
                "country": "$_id",
                "percentage_wheelchair_accessible": {
                    "$cond": [
                        {"$eq": ["$total", 0]},
                        0,
                        {"$multiply": [
                            {"$divide": ["$wheelchair_accessible_count", "$total"]}, 100]}
                    ]
                }
            }
        },
        {"$sort": {"percentage_wheelchair_accessible": -1}}
    ]

    # Execute aggregation query
    result = collection.aggregate(pipeline)

    # Formatting the results
    percentages_by_country = {}
    for item in result:
        country = item["_id"]
        percentage = item["percentage_wheelchair_accessible"]
        percentages_by_country[country] = round(percentage, 2)

    return percentages_by_country

# Query 4 - Top Five Vegan Restaurants in Milan
def currently_open_restaurants_in(city):

    now = datetime.datetime.now()

    current_day = now.strftime('%A')[:3]
    print('Current Day Name:', current_day)
    current_time = now.strftime("%H:%M")
    print("Current Time =", current_time)

    query = {
        'location.city': city,
        'availability.original_open_hours': {'$ne': ""}
    }
    value_limit = 100

    restaurants = db_find_many(query=query, value_limit=value_limit)

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

    start_time, end_time = range.split("-")
    start_time = start_time.split(':')
    end_time = end_time.split(':')

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M").split(":")

    start = datetime.time(int(start_time[0]), int(start_time[0]))
    end = datetime.time(int(end_time[0]), int(end_time[0]))
    current = datetime.time(int(current_time[0]), int(current_time[0]))

    return start <= current <= end

# Query 5 - Average rating of the certified restaurant
def compute_average_rating_and_reviews_of_certified_restaurants():
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']
    current_year = 2020 # datetime.now().year

    # Aggregation pipeline
    pipeline = [
        {
            "$match": {
                "awards": {
                    "$elemMatch": {
                        "$regex": f"Certificate of Excellence {current_year - 2}|{current_year - 1}"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "average_rating": {"$avg": "$rating.avg_rating"},
                "average_reviews_count": {"$avg": "$rating.total_reviews_count"}
            }
        }
    ]

    # Execute the aggregation query
    result = collection.aggregate(pipeline)

    # Extracting the average rating and average number of reviews from the aggregation result
    for item in result:
        average_rating = item.get("average_rating", 0)
        average_reviews_count = item.get("average_reviews_count", 0)
        return (round(average_rating, 2), round(average_reviews_count, 0))

# Query 6 - Top Five Resturant respecting a budget in Milan
def top_resturant_respecting_the_budget(city, budget):
    query = {
        'location.city': city,
        'food_specification.vegetarian_friendly': True,
        'price_range.0': {'$lte': budget}
    }

    order = {
        'rating.avg_rating': -1
    }

    value_limit = 5

    restaurants = db_find_many(
        query=query, order=order, value_limit=value_limit)

    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['_id']} {el['restaurant_name']}")


# Query 8 - Best Pizza in Rome!
def find_by_tags_and_rating_in(city, tags):

    query = {
        'location.city': city,
        'top_tags': {'$in': tags},
        'rating.food': {'$gte': 4.5},
        'rating.avg_rating': {'$gte': 4.5}
    }

    order = {
        'rating.avg_rating': -1
    }

    value_limit = 5

    restaurants = db_find_many(
        query=query, order=order, value_limit=value_limit)

    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['_id']} {el['restaurant_name']}")

# Query 10 - Breakfast in Paris with Free Wifi!


def find_meal_type_and_features_in(city, meal_type, features):

    query = {
        'location.city': city,
        'availability.meals': {'$in': meal_type},
        'availability.features': {'$in': features},
    }

    order = {
        'rating.avg_rating': -1
    }

    value_limit = 5

    restaurants = db_find_many(
        query=query, order=order, value_limit=value_limit)

    for index, el in enumerate(restaurants, start=1):
        print(f"Restaurant #{index}: {el['_id']} {el['restaurant_name']}")


# Example usage
if __name__ == "__main__":
    # query = {'restaurant_link': 'g187079-d1234567'} # 'La Bonne Fourchette'
    # find_and_print_data(query)

    # Query 1 run sample
    # country = 'France'
    # region_name = 'Pays de la Loire'
    # user_location = (47.72043, -0.70911) # lat. & long.
    # max_dist = 12 # km
    # result = find_restaurants_nearby(country, region_name, user_location, max_dist)
    # for rest in result:
    #     print(rest[0]['restaurant_name'] + ': ' + str(round(rest[1],2)) + 'km')

    # Query 2 run sample
    # city = 'Milan'
    # top_vegan_restaurant_in(city)

    # Query 3 run sample
    # result = compute_percentage_wheelchair_accessible_by_country()
    # print(result)

    # Query 4 run sample
    # city = 'Milan'
    # currently_open_restaurants_in(city)
    
    # Query 5 certified restaurant metric
    print(compute_average_rating_and_reviews_of_certified_restaurants())

    # Query 6 run sample
    # city = 'Milan'
    # budget = 30
    # top_resturant_respecting_the_budget(city,budget)

    # Query 8 run sample
    # city = 'Rome'
    # tags = ['Pizza']
    # find_by_tags_and_rating_in(city, tags)

    # Query 10 run sample
    # city = 'Paris'
    # features = ['Free Wifi']
    # meal_type = ['Breakfast']
    # find_meal_type_and_features_in(city,meal_type,features)
