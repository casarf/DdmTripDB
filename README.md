# CSV to JSON Parser for TripAdvisor European Restaurants

This script provides a Python-based utility to convert the "TripAdvisor European restaurants" dataset from CSV format to a structured JSON format. The conversion process involves parsing each row of the CSV file, transforming specific fields to ensure they are in the appropriate JSON format, and writing the resulting JSON objects to an output file.

## Dataset

The dataset can be found on Kaggle under the name ["TripAdvisor European restaurants"](https://www.kaggle.com/datasets/stefanoleone992/tripadvisor-european-restaurants). It encompasses a comprehensive list of restaurants across Europe with a multitude of attributes, from location details to user reviews and ratings.

## Features

- Conversion of comma-separated values in certain columns to arrays
- Casting of geographical coordinates to floating-point numbers
- Parsing and splitting price levels and ranges
- Transformation of Boolean-like strings to actual Boolean values
- Transformation of numeric strings to floats where applicable
- Handling of JSON fields present within the CSV

## Prerequisites

Before running this script, ensure you have Python installed on your machine. This script was developed with Python 3.x in mind.

Additionally, install the required packages using the following command:

```bash
pip install csv json
```

## Usage

1. Download the CSV dataset from the Kaggle link provided above.
2. Place the script in the same directory as the CSV file or update the `csv_file_path` variable with the appropriate file path.
3. Execute the script using the following command:

```bash
python csv_to_json_parser.py
```

4. Upon successful execution, the JSON file named `tripadvisor_european_restaurants.json` will be generated in the same directory.

## Script Example

```python
import csv
import json

# Function to convert CSV to JSON
def csv_to_json(csv_file_path, json_file_path):
    # Your existing code implementation

# Set the path to your CSV file
csv_file_path = 'tripadvisor_european_restaurants.csv'

# Set the path for the resulting JSON file
json_file_path = 'tripadvisor_european_restaurants.json'

# Call the conversion function
csv_to_json(csv_file_path, json_file_path)

# Notify the user of completion
print('Conversion to JSON completed!')
```

Ensure that you have the correct file paths set for both `csv_file_path` and `json_file_path` before running the script.