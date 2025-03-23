from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API URL for country information
RESTCOUNTRIES_URL = "https://restcountries.com/v3.1/name/{name}"

@app.route('/api/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query')
    country_name = extract_country_name(user_query)
    
    if not country_name:
        return jsonify({"response": "Please specify a country."})

    # Get country info
    country_info = get_country_data(country_name)
    
    if not country_info:
        return jsonify({"response": "Sorry, I couldn't find information about that country."})
    
    # Format the country information
    response = format_country_info(country_info)
    
    return jsonify({"response": response})

def extract_country_name(query):
    """Extract country name from query."""
    # Fetch all country names from the RestCountries API
    response = requests.get('https://restcountries.com/v3.1/all')
    if response.status_code == 200:
        countries = response.json()
        country_names = [country['name']['common'].lower() for country in countries]
        
        # Check if any country name is in the query
        for country_name in country_names:
            if country_name in query.lower():
                return country_name.capitalize()  # Return the capitalized country name
    
    return None

def get_country_data(country_name):
    """Get country info from RestCountries API."""
    response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}')
    
    if response.status_code == 200:
        data = response.json()
        return data[0] if len(data) > 0 else None
    
    return None

def format_country_info(country_info):
    """Format country information into a readable response."""
    name = country_info['name']['common']
    capital = country_info['capital'][0]
    population = country_info['population']
    currency = list(country_info['currencies'].keys())[0]
    
    response = (
        f"Here are some facts about {name}:\n"
        f"- Capital: {capital}\n"
        f"- Population: {population}\n"
        f"- Currency: {currency}\n"
    )
    
    return response

if __name__ == '__main__':
    app.run(debug=True)