# Pizza Restaurant API - Code Challenge

This repository contains a Flask API implementation for a pizza restaurant system. The goal was to develop an API to manage restaurants, pizzas, and their relationships, while adhering to specific requirements such as data validation and proper handling of relational data.

## Features and Functionality

### Flask API
- **Models**: The system uses three key models: `Restaurant`, `Pizza`, and `RestaurantPizza`.
  - A `Restaurant` can have multiple `Pizza`s through the `RestaurantPizza` join table.
  - A `Pizza` can belong to multiple `Restaurant`s through the same join table.
  - The `RestaurantPizza` model links the two and includes a `price` attribute that is validated to be between 1 and 30.

### Routes Implemented
- **GET /restaurants**: Fetch a list of all restaurants.
- **GET /restaurants/<id>**: Fetch detailed information about a specific restaurant, including the pizzas it offers.
- **DELETE /restaurants/<id>**: Delete a restaurant along with its associated `RestaurantPizza` records.
- **GET /pizzas**: Fetch a list of all available pizzas.
- **POST /restaurant_pizzas**: Create a new `RestaurantPizza` record linking a restaurant to a pizza, with a valid price.

### Database
- **SQLAlchemy** was used for ORM-based modeling and handling database interactions.
- **Cascading Deletes**: Ensured that when a restaurant is deleted, all associated `RestaurantPizza` records are also removed.
- **Data Validation**: The `price` in the `RestaurantPizza` model must fall between 1 and 30.

### Frontend
- A **React frontend** is included in the project to interact with the API. It’s pre-built and provided to help test the API, but no modifications were required to the frontend.

## Setup Instructions

### Prerequisites
- **Python 3.7+**: Ensure Python is installed.
- **Node.js**: For running the React frontend.

### Installation

1. **Clone the Repository**:
   
   git clone `<repo_url>`
   cd `<repo_name>`

2. **Install Backend Dependencies**:
    
    pipenv install
    pipenv shell

3. **Install Frontend Dependencies**:
   

   `npm install --prefix client`

4. **Setup the Database**:

  * Initialize the Flask app:

   `export FLASK_APP=server/app.py`
  
  * Run database migrations:

    flask db init
    flask db migrate
    flask db upgrade `head`

  * Seed the database with initial data:

    `python server/seed.py`

5. **Run the Flask API**:

   `python server/app.py`

   The API will be available at http://localhost:5555.

6. **Run the React Frontend**:

  * `npm start --prefix client`
   The frontend will be available at http://localhost:4000.

**Testing**

**Unit Tests: To run the provided tests**:
 `pytest -x`

**Postman**: You can import the provided challenge-1-pizzas.postman_collection.json file into Postman to test the API endpoints interactively.

### Conclusion

This project involved implementing a RESTful API with Flask to handle restaurant and pizza management. I set up proper database relationships, validation, and routes to meet the project requirements. The React frontend was included to test the functionality, but no changes were necessary for it.

Feel free to explore the code and run tests to validate the implementation.