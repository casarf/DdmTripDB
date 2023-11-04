import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    json_list = []

    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Convert 'awards', 'top_tags', 'features', 'meals', 'cuisines', and 'special_diets' from comma separated to arrays
            row['awards'] = [award.strip() for award in row['awards'].split(',')] if row['awards'] else []
            row['top_tags'] = [tag.strip() for tag in row['top_tags'].split(',')] if row['top_tags'] else []
            row['features'] = [feature.strip() for feature in row['features'].split(',')] if row['features'] else []
            row['meals'] = [meal.strip() for meal in row['meals'].split(',')] if row['meals'] else []
            row['cuisines'] = [cuisine.strip() for cuisine in row['cuisines'].split(',')] if row['cuisines'] else []
            row['special_diets'] = [diet.strip() for diet in row['special_diets'].split(',')] if row['special_diets'] else []
            row['keywords'] = [keyword.strip() for keyword in row['keywords'].split(',')] if row['keywords'] else []

            # Convert 'latitude' and 'longitude' to float or default to 0.0 if empty
            latitude = row.get('latitude', '0.0').strip()
            longitude = row.get('longitude', '0.0').strip()
            latitude = float(latitude) if latitude else 0.0
            longitude = float(longitude) if longitude else 0.0

            # Process price levels and ranges
            row['price_level'] = row['price_level'].split('-') if row['price_level'] else []
            row['price_range'] = row['price_range'].split('-') if row['price_range'] else []

            # Convert 'claimed' status to boolean
            row['claimed'] = row['claimed'] == "Claimed"

            # Convert dietary options to boolean
            row['vegetarian_friendly'] = row['vegetarian_friendly'] == 'Y'
            row['vegan_options'] = row['vegan_options'] == 'Y'
            row['gluten_free'] = row['gluten_free'] == 'Y'

            # Convert ratings to float or default to 0.0 if empty
            avg_rating = row.get('', '0.0').strip()
            total_reviews_count = row.get('', '0.0').strip()
            reviews_count_in_default_language = row.get('', '0.0').strip()
            excellent = row.get('', '0.0').strip()
            very_good = row.get('', '0.0').strip()
            average = row.get('', '0.0').strip()
            poor = row.get('', '0.0').strip()
            terrible = row.get('', '0.0').strip()
            food = row.get('', '0.0').strip()
            service = row.get('', '0.0').strip()
            value = row.get('', '0.0').strip()
            atmosphere = row.get('', '0.0').strip()
            
            open_days_per_week = row.get('', '0.0').strip()
            open_hours_per_week = row.get('', '0.0').strip()
            working_shifts_per_week = row.get('', '0.0').strip()

            avg_rating = float(avg_rating) if avg_rating else ""
            total_reviews_count = float(total_reviews_count) if total_reviews_count else ""
            reviews_count_in_default_language = float(reviews_count_in_default_language) if reviews_count_in_default_language else ""
            excellent = float(excellent) if excellent else ""
            very_good = float(very_good) if very_good else ""
            average = float(average) if average else ""
            poor = float(poor) if poor else ""
            terrible = float(terrible) if terrible else ""
            food = float(food) if food else ""
            service = float(service) if service else ""
            value = float(value) if value else ""
            atmosphere = float(atmosphere) if atmosphere else ""

            open_days_per_week = float(open_days_per_week) if open_days_per_week else ""
            open_hours_per_week = float(open_hours_per_week) if open_hours_per_week else ""
            working_shifts_per_week = float(working_shifts_per_week) if working_shifts_per_week else ""

            # Handle JSON fields within the CSV
            for json_field in ['original_location', 'original_open_hours']:
                if row[json_field]:
                    try:
                        row[json_field] = json.loads(row[json_field].replace('\'', '\"'))
                    except json.JSONDecodeError:
                        row[json_field] = None  # or some sensible default

            # Create the structured document
            document = {
                "restaurant_link": row['restaurant_link'],
                "restaurant_name": row['restaurant_name'],
                "location": {
                    "country": row['country'],
                    "region": row['region'],
                    "province": row['province'],
                    "city": row['city'],
                    "address": row['address'],
                    "latitude": latitude,
                    "longitude": longitude
                },
                "claimed": row['claimed'],
                "awards": row['awards'],
                "popularity_detailed": row['popularity_detailed'],
                "popularity_generic": row['popularity_generic'],
                "top_tags": row['top_tags'],
                "price_level": row['price_level'],
                "price_range": row['price_range'],
                "food_specification": {
                    "cuisines": row['cuisines'],
                    "special_diets": row['special_diets'],
                    "vegetarian_friendly": row['vegetarian_friendly'],
                    "vegan_options": row['vegan_options'],
                    "gluten_free": row['gluten_free']
                },
                "availability": {
                    "meals": row['meals'],
                    "features": row['features'],
                    "original_open_hours": row['original_open_hours'],
                    "open_days_per_week": open_days_per_week,
                    "open_hours_per_week": open_hours_per_week,
                    "working_shifts_per_week": working_shifts_per_week
                },
                "rating": {
                    "avg_rating": avg_rating,
                    "total_reviews_count": total_reviews_count,
                    "default_language": row.get('default_language', ''),
                    "reviews_count_in_default_language": reviews_count_in_default_language,
                    "excellent": excellent,
                    "very_good": very_good,
                    "average": average,
                    "poor": poor,
                    "terrible": terrible,
                    "food": food,
                    "service": service,
                    "value": value,
                    "atmosphere": atmosphere,
                    "keywords": row['keywords']
                }
            }

            json_list.append(document)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_list, json_file, indent=4, ensure_ascii=False)

csv_file_path = 'tripadvisor_european_restaurants.csv'
json_file_path = 'tripadvisor_european_restaurants.json'
csv_to_json(csv_file_path, json_file_path)
print('Done!')
