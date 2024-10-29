def get_population_prompt(country_data):
    population_in_millions = country_data['population'] / 1_000_000 if 'population' in country_data and country_data['population'] else 0
    pop_density = country_data.get('pop_density', 'N/A')
    sex_ratio = country_data.get('sex_ratio', 'N/A')

    prompt = f"""
    The country {country_data['name']} has a population of approximately {population_in_millions:.2f} million people. 
    The population density is around {pop_density} individuals per square kilometer, with a sex ratio close to {sex_ratio}. 
    This summary provides insights into the demographic distribution based on available data.
    """
    return prompt

def get_tourists_prompt(country_data):
    tourists_in_millions = country_data['tourists'] / 1_000_000 if 'tourists' in country_data and country_data['tourists'] else 0

    prompt = f"""
    In recent years, {country_data['name']} has hosted around {tourists_in_millions:.2f} million tourists. 
    This figure reflects the level of international interest and tourism attraction for {country_data['name']} based on observed data.
    """
    return prompt

def get_import_export_prompt(country_data):
    imports_in_millions = country_data['imports'] / 1_000_000 if 'imports' in country_data and country_data['imports'] else 0
    exports_in_millions = country_data['exports'] / 1_000_000 if 'exports' in country_data and country_data['exports'] else 0

    prompt = f"""
    The trade overview for {country_data['name']} indicates imports valued at approximately {imports_in_millions:.2f} million USD, while exports are estimated at {exports_in_millions:.2f} million USD. 
    This summary provides a concise look at the country’s trade flow based on available data.
    """
    return prompt
