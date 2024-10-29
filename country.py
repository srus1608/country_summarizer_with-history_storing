from flask import jsonify, request
import requests
from database import get_db_connection  
import os

API_KEY = os.getenv("API_KEY")

def fetch_country_data(country_name):
    api_url = f"https://api.api-ninjas.com/v1/country?name={country_name}"
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            return {
                'name': data[0]['name'],
                'gdp': data[0].get('gdp', 0),
                'population': data[0]['population'],
                'tourists': data[0].get('tourists', 0),
                'currency': data[0]['currency']['code'],
                'surface_area': data[0].get('surface_area', 0),
                'imports': data[0].get('imports', 0),
                'exports': data[0].get('exports', 0),
                'pop_density': data[0].get('pop_density', 0),
                'sex_ratio': data[0].get('sex_ratio', 0),
                'gdp_growth': data[0].get('gdp_growth', 0)
            }
    return None

def store_country_data(country_data):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO extended_country_details 
            (name, gdp, population, tourists, currency, surface_area, imports, exports, pop_density, sex_ratio, gdp_growth)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            country_data['name'],
            country_data['gdp'],
            country_data['population'],
            country_data['tourists'],
            country_data['currency'],
            country_data['surface_area'],
            country_data['imports'],
            country_data['exports'],
            country_data['pop_density'],
            country_data['sex_ratio'],
            country_data['gdp_growth']
        ))
        connection.commit()
        cursor.close()
        connection.close()

def fetch_and_store_country(country_name):
    country_data = fetch_country_data(country_name)
    if country_data:
        store_country_data(country_data)
        return jsonify({
            'message': f"Data for {country_name} fetched and stored successfully.",
            'data': country_data
        }), 200
    else:
        return jsonify({'error': 'Failed to fetch country data'}), 500
