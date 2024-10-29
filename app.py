from flask import Flask, request, jsonify
from country import fetch_and_store_country
from summarize import generate_summary
from chat_history import store_chat_history, fetch_chat_history, create_chat_history_table

app = Flask(__name__)

# Initialize chat history table
create_chat_history_table()

@app.route('/fetch-country', methods=['GET'])
def fetch_country():
    country_name = request.args.get('name')
    if not country_name:
        return jsonify({'error': 'Country name is required'}), 400
    return fetch_and_store_country(country_name)

@app.route('/generate-summary/<string:parameter>', methods=['GET'])
def summary(parameter):
    country_name = request.args.get('name')
    if not country_name:
        return jsonify({'error': 'Country name is required'}), 400

    summary_result = generate_summary(parameter, country_name)
    if summary_result['status'] == 'success':
        summary = summary_result['summary']
        
        # Store the chat history with the country name
        store_chat_history(query=f"{parameter} summary for {country_name}", summary=summary, name=country_name)
        
        return jsonify({
            'message': f"{parameter.capitalize()} summary for {country_name} generated successfully.",
            'data': summary
        }), 200
    else:
        return jsonify({'error': summary_result['message']}), 500

@app.route('/chat-history', methods=['GET'])
def get_chat_history():
    history = fetch_chat_history()
    return jsonify({
        'status': 'success',
        'data': history,
        'message': 'Chat history retrieved successfully'
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

