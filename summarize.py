from database import get_db_connection

def generate_summary(parameter, country_name):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            select_query = """
                SELECT name, gdp, population, tourists, currency, surface_area, imports, exports, pop_density, sex_ratio, gdp_growth 
                FROM extended_country_details WHERE name = %s
            """
            cursor.execute(select_query, (country_name,))
            row = cursor.fetchone()

            if row:
                name, gdp, population, tourists, currency, surface_area, imports, exports, pop_density, sex_ratio, gdp_growth = row
                
                # Convert large values to millions
                gdp_million = gdp / 1_000_000
                population_million = population / 1_000_000
                tourists_million = tourists / 1_000_000
                imports_million = imports / 1_000_000
                exports_million = exports / 1_000_000
                
                if parameter == "population":
                    summary = f"{name} has a population of approximately {population_million:.2f} million people, with a population density of {pop_density} people per square kilometer."
                elif parameter == "tourists":
                    summary = f"{name} attracts around {tourists_million:.2f} million tourists annually."
                elif parameter == "import_export":
                    summary = f"{name} has imports valued at approximately {imports_million:.2f} million {currency} and exports worth about {exports_million:.2f} million {currency}."
                else:
                    summary = "Invalid parameter for summary."

                return {'status': 'success', 'summary': summary}
            else:
                return {'status': 'error', 'message': 'Country not found in database'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            connection.close()
    else:
        return {'status': 'error', 'message': 'Database connection failed'}
