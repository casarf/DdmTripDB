# TripAdvisor & MongoDB

This repository contains essential scripts for interacting with a database and performing Create, Read, Update, and Delete (CRUD) operations. Each script in the `data_manipulation` directory is an example implementation of one of the CRUD operations.

## Folders Overview

The repository is organized into two main directories:

- `data_manipulation`: Contains scripts that exemplify each of the CRUD operations on the database.
- `db_connection`: Provides the necessary functionality to connect to the database.

### `data_manipulation`

The `data_manipulation` directory holds four scripts that cover the spectrum of CRUD operations:

- `create_data.py`: Demonstrates how to insert new data into the database.
- `read_data.py`: Shows how to query and retrieve data from the database.
- `update_data.py`: Provides an example of how to update existing data within the database.
- `delete_data.py`: Illustrates how to remove data from the database.

Each script is standalone and can be run to perform the respective operation against a preconfigured database.

### `db_connection`

This directory contains modules that manage the connection to the database. It ensures that the CRUD scripts can interface with the database seamlessly. Key components include:

- `mongo_connect.py`: A module that facilitates connections to a MongoDB server.

## Getting Started

To execute the CRUD operation scripts, follow these steps:

1. **Environment Setup:**
   - Make sure Python is installed on your machine.
   - Install the required dependencies using `pip install -r requirements.txt`.

2. **Database Configuration:**
   - Within the `db_connection` directory, adjust `mongo_connect.py` to include your database details.

3. **Perform CRUD Operations:**
   - Navigate to the `data_manipulation` folder.
   - Run the desired script to perform a specific operation on the database.

## Prerequisites

Before running the scripts, ensure the following are installed:

- Python 3.x
- A running instance of MongoDB or the relevant database system
