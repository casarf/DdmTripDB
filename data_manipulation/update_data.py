from data_manipulation.read_data import find_restaurant_by_link
from db_connection.mongo_connect import create_connection
from bson.decimal128 import Decimal128

def db_update_one(query, new_values):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    update_result = collection.update_one(query, {'$set': new_values})
    print(f'Updated {update_result.modified_count} documents.')

def db_update_many(query, new_values):
    client = create_connection()
    db = client['TripAdvisor']
    collection = db['EuropeanRestaurants']

    update_result = collection.update_many(query, {'$set': new_values})
    print(f'Updated {update_result.modified_count} documents.')

def update_open_hours_multiple_days(restaurant_link, days, time_ranges):
    """
    Update the opening hours for specific days for a restaurant.

    :param restaurant_link: The unique identifier for the restaurant.
    :param days: A list of days to update the hours for.
    :param time_ranges: A list of strings containing the new time ranges for the days.
    """
    query = {'restaurant_link': restaurant_link}
    # The time_ranges list is assumed to be the same for all days to be updated.
    # Convert the list of time ranges into a format that is a list of strings, which each day will use.
    time_ranges_str = time_ranges
    
    new_values = {f'availability.original_open_hours.{day}': time_ranges_str for day in days}
    
    # Execute the update operation.
    db_update_one(query, new_values)


def update_ratings(restaurant_link, rating_update):
    # Retrieve the current rating details
    restaurant = find_restaurant_by_link(restaurant_link)

    if restaurant and 'rating' in restaurant:
        current_ratings = restaurant['rating']

        # Calculate the new total reviews count and update the specific rating.
        total_reviews_count = current_ratings.get('total_reviews_count', Decimal128('0')).to_decimal() + 1
        current_ratings[rating_update] = current_ratings.get(rating_update, Decimal128('0')).to_decimal() + 1

        # Recalculate the average rating.
        ratings_weight = {'excellent': 5, 'very_good': 4, 'average': 3, 'poor': 2, 'terrible': 1}
        total_rating_score = sum(ratings_weight[key] * current_ratings.get(key, Decimal128('0')).to_decimal() for key in ratings_weight)
        avg_rating = total_rating_score / total_reviews_count

        # Prepare the new values for updating the document.
        new_values = {
            'rating.total_reviews_count': Decimal128(str(total_reviews_count)),
            'rating.avg_rating': Decimal128(str(avg_rating)),
            f'rating.{rating_update}': Decimal128(str(current_ratings[rating_update]))
        }

        db_update_one({'restaurant_link': restaurant_link}, new_values)

    else:
        # Handle the case where the restaurant is not found or has no ratings.
        return 'Restaurant not found or has no ratings yet.'


def todo():
    # {"availability.meals": { '$exists': true},"availability.meals": [], 'availability.original_open_hours': {$ne: []}}
    return 0
# Example usage: update_ratings
# if __name__ == "__main__":
#     # Example to increment the 'excellent' rating
#     update_ratings('g1005749-d14139205', 'excellent')


# Example usage: update_open_hours_multiple_days
if __name__ == "__main__":
    # Update the hours for Monday, Tuesday, and Friday to '08:00-14:00' and '17:00-22:30'.
    update_open_hours_multiple_days('g187079-d1234567', ['Mon', 'Tue', 'Fri'], ['08:00-14:00', '17:00-22:30'])