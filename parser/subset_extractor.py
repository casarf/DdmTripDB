import json

def extract_first_100_elements(input_json_path, output_json_path):
    # Open the input JSON file for reading
    with open(input_json_path, 'r', encoding='utf-8') as file:
        # Load the data from the file
        data = json.load(file)

    # Check if the data is a list and has at least 100 elements
    if isinstance(data, list) and len(data) >= 100:
        # Extract the first 100 elements
        first_100_elements = data[:100]
    else:
        print("The JSON file does not contain a list with at least 100 elements.")
        return

    # Open the output JSON file for writing
    with open(output_json_path, 'w', encoding='utf-8') as file:
        # Write the first 100 elements to the file
        json.dump(first_100_elements, file, indent=4)

    print(f"The first 100 elements have been extracted to {output_json_path}")

# Paths for the input and output JSON files
input_json_path = 'tripadvisor_european_restaurants.json'
output_json_path = 'tripadvisor_european_restaurants_100.json'

# Call the function with the specified paths
extract_first_100_elements(input_json_path, output_json_path)
