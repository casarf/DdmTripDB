from db_connection.mongo_connect import create_connection

def update_data(query, new_values):
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
    update_data(query, new_values)

# Example usage
if __name__ == "__main__":
    # Update the hours for Monday, Tuesday, and Friday to '08:00-14:00' and '17:00-22:30'.
    update_open_hours_multiple_days('g187079-d1234567', ['Mon', 'Tue', 'Fri'], ['08:00-14:00', '17:00-22:30'])