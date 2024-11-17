from flask import Flask, request, jsonify
import pandas as pd
import requests
from io import StringIO  # <-- Import StringIO from io
from serpapi import GoogleSearch
import os
from groq import Groq
SERP_API_KEY = ""

os.environ["GROQ_API_KEY"] = ""

app = Flask(__name__)


# Basic route to test if Flask is working
@app.route('/')
def home():
    return "Flask server is running!"


# Route to handle CSV upload
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        columns = df.columns.tolist()
        preview = df.head().to_dict()
        return jsonify({'columns': columns, 'preview': preview})
    else:
        return jsonify({'error': 'File is not a CSV'}), 400


# Route to handle Google Sheets data retrieval via public CSV export
@app.route('/get_google_sheet', methods=['POST'])
def get_google_sheet():
    data = request.get_json()
    sheet_id = data.get('sheet_id')

    if not sheet_id:
        return jsonify({'error': 'Sheet ID not provided'}), 400

    # Generate Google Sheets CSV export URL
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    try:
        response = requests.get(sheet_url)
        response.raise_for_status()  # Raise an error for bad responses
        df = pd.read_csv(StringIO(response.text))  # <-- Use StringIO here

        columns = df.columns.tolist()
        preview = df.head().to_dict()
        return jsonify({'columns': columns, 'preview': preview})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/perform_search', methods=['POST'])
def perform_search():
    data = request.get_json()
    queries = data.get('queries')

    if not queries:
        return jsonify({'error': 'No queries provided'}), 400

    results = {}

    for query in queries:
        try:
            params = {
                "q": query,
                "api_key": SERP_API_KEY,
                "num": 5
            }
            search = GoogleSearch(params)
            search_results = search.get_dict().get("organic_results", [])

            formatted_results = [
                {"title": result.get("title"), "url": result.get("link"), "snippet": result.get("snippet")}
                for result in search_results
            ]
            results[query] = formatted_results if formatted_results else {"error": "No results found."}

        except Exception as e:
            results[query] = {"error": str(e)}

    # Debugging log
    # print("Search Results:", results)
    return jsonify(results)




@app.route('/process_with_groq', methods=['POST'])
def process_with_groq():
    data = request.get_json()
    entity_data = data.get('entity_data')  # List of entities with search results
    prompt_template = data.get('prompt_template')

    # Initialize Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    results = []
    for entity in entity_data:
        company = entity.get("company", "Unknown Company")
        search_results = entity.get("search_results", [])

        # If no search results, append a result indicating failure and continue
        if not search_results:
            results.append({
                "entity": entity,
                "extracted_info": f"There are no search results for {company}. I cannot extract the required information."
            })
            continue

        # Combine prompt with actual search results
        formatted_search_results = "\n".join(
            f"- {result['title']} ({result['url']}): {result['snippet']}"
            for result in search_results
        )
        full_prompt = f"{prompt_template.format(company=company)}\n\nSearch results:\n{formatted_search_results}"
        messages = [{"role": "user", "content": full_prompt}]

        try:
            # Send request to Groq API with search results included
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192"  # Use the appropriate model as needed
            )
            # Extract response from Groq API
            extracted_info = chat_completion.choices[0].message.content.strip()
            results.append({"entity": entity, "extracted_info": extracted_info})

        except Exception as e:
            print(f"Error processing {company}: {e}")
            results.append({"entity": entity, "extracted_info": "Error"})

    return jsonify({"results": results})


if __name__ == '__main__':
    app.run(debug=True)
