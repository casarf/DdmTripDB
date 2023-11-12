from db_connection.mongo_connect import create_connection, close_connection
from data_manipulation.read_data import db_find_many
from bson import ObjectId

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

# Command #5 - Delete a duplicated restaurant
def delete_duplicated_restaurant():
    
    query = {
        "location.city" : 'Milan',
    }
    
    restaurants = db_find_many(query)
    
    duplicated = []
    
    for i in range(len(restaurants)):
        temp = []
        
        first = restaurants[i]
        temp.append(first["_id"])
        
        for j in range(i+1,len(restaurants)):
            second = restaurants[j]
            if (first["restaurant_name"] == second["restaurant_name"]) and (first["location"]["address"] == second["location"]["address"]):
                temp.append(second["_id"])
        
        if len(temp) != 1:
            duplicated.append(temp)
    
    for el in duplicated:
        for i in range(1,len(el)):
            query = {
                "_id": ObjectId(el[i])
            }
            db_delete_one(query)
  
    

# Example usage
if __name__ == "__main__":
    delete_duplicated_restaurant()