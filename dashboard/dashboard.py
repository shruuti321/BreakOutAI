

import streamlit as st
import requests
import pandas as pd
import re
# URL of the Flask backend
BACKEND_URL = "http://127.0.0.1:5000"

# Function to handle CSV file upload
def upload_csv(file):
    response = requests.post(f"{BACKEND_URL}/upload_csv", files={'file': file})
    return response.json()

# Function to handle Google Sheets data retrieval
def get_google_sheet(sheet_id):
    response = requests.post(
        f"{BACKEND_URL}/get_google_sheet",
        json={'sheet_id': sheet_id}
    )
    return response.json()

def extract_email_from_snippet(snippet):
    # Use regular expression to find email addresses in the snippet
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, snippet)
# Function to handle the extraction of company name from the query
def extract_company_from_query(query):
    # Assuming query contains company information (like "Get email of {company}")
    # You can adjust the logic based on the format of your query
    company_name = query.split(" ")[-1]  # Assuming company is the last word in the query
    return company_name

# Function to process data with Groq API
def process_data_with_groq(entity_data, prompt_template):
    response = requests.post(
        f"{BACKEND_URL}/process_with_groq",
        json={"entity_data": entity_data, "prompt_template": prompt_template}
    )
    print("Groq API response:", response.json())

    return response.json()

# Streamlit UI
st.title("Data Upload: CSV or Google Sheet")

# --- CSV Upload Section ---
st.subheader("Upload a CSV File")
csv_file = st.file_uploader("Choose a CSV file", type="csv")

if csv_file:
    result = upload_csv(csv_file)
    if 'error' in result:
        st.error(result['error'])
    else:
        st.success("CSV file uploaded successfully!")
        st.write("Available Columns:", result['columns'])

        # Select the main column from the available columns
        selected_column = st.selectbox("Select the main column", result['columns'])

        # Display a preview of the data
        st.write("Data Preview:")
        st.write(result['preview'])

        # --- Dynamic Query Input Section ---
        st.subheader("Define Custom Query Template")

        # Text input for the custom query prompt template
        query_template = st.text_input(
            "Enter your query template (use placeholders like {company})",
            value="Get me the email address of {company}"
        )

        # Check if query template is provided
        if query_template:
            # Extract the list of entities from the selected main column
            entities = result['preview'][selected_column]

            # Generate and store customized queries
            st.write("Generated Queries:")
            generated_queries = []
            for entity in entities:
                # Replace placeholder with actual entity name
                custom_query = query_template.replace("{company}", entity)
                generated_queries.append(custom_query)
                st.write(custom_query)  # Display each generated query

# --- Google Sheets Section ---
st.subheader("Link Google Sheet")
sheet_id = st.text_input("Enter Google Sheet ID")

if sheet_id:
    result = get_google_sheet(sheet_id)

    if 'error' in result:
        st.error(result['error'])
    else:
        st.success("Google Sheet linked successfully!")
        st.write("Available Columns:", result['columns'])

        # Select the main column from the available columns
        selected_column = st.selectbox("Select the main column", result['columns'], key="sheet")

        # Display a preview of the data
        st.write("Data Preview:")
        st.write(result['preview'])

        # --- Dynamic Query Input Section for Google Sheets ---
        st.subheader("Define Custom Query Template")

        # Text input for the custom query prompt template
        query_template = st.text_input(
            "Enter your query template (use placeholders like {company})"
        )

        # Check if query template is provided
        if query_template:
            # Extract the list of entities from the selected main column
            entities = list(result['preview'][selected_column].values())

            # Generate and store customized queries
            st.write("Generated Queries:")
            generated_queries = []
            for entity in entities:
                # Replace placeholder with actual entity name
                custom_query = query_template.replace("{company}", entity)
                generated_queries.append(custom_query)
                st.write(custom_query)  # Display each generated query

# --- Perform Web Search for Queries ---
if st.button("Perform Web Search for Queries") and 'generated_queries' in locals():
    # Call the backend search endpoint with generated queries
    st.write("Generated Queries:", generated_queries)
    search_results = requests.post(
        f"{BACKEND_URL}/perform_search",
        json={'queries': generated_queries}
    ).json()
    st.write("Search Results from Backend:", search_results)
    # Store the search results to use later for Groq processing
    st.session_state.search_results = search_results  # Store search results in session state

    # Display search results
    st.subheader("Search Results")
    for query, results in search_results.items():
        st.write(f"Results for: {query}")
        if "error" in results:
            st.error(f"Error: {results['error']}")
        else:
            for result in results:
                st.write(f"- [{result['title']}]({result['url']})")
                st.write(f"  Snippet: {result['snippet']}")

# --- Process Data with Groq ---
if st.button("Process Data with Groq") and 'search_results' in st.session_state:

    

    entity_data = []
    extracted_emails = []  # Store extracted emails per company

    for query in generated_queries:
        company_name = extract_company_from_query(query)  # Custom function to extract company name
        st.write(f"Company extracted for query '{query}':", company_name)  # Log company name

        # If search_results is a list, loop through it to find the relevant results
        search_results_for_company = []
        company_emails = []  # Store emails for the current company

        # Ensure we are fetching search results for the company-specific query
        for result in st.session_state.search_results.get(query, []):  # Check each query for company results
            snippet = result.get('snippet', '')

            # Extract emails from the snippet for the current company
            emails_in_snippet = extract_email_from_snippet(snippet)
            if emails_in_snippet:
                company_emails.extend(emails_in_snippet)  # Add emails to the list for this company

            search_results_for_company.append(result)

        # Combine company info and search results
        entity_data.append({
            "company": company_name,
            "search_results": search_results_for_company,
            "emails": company_emails  # Only the emails for this company
        })

        # Log the company-specific emails for verification
        st.write(f"Emails extracted for {company_name}:", company_emails)

    # Log the entity_data before sending it to Groq
    st.write("Entity Data being sent to Groq:", entity_data)

    # Prompt template for Groq
    prompt_template = st.text_input("Enter your prompt template:",
                                    "From the search results, extract the email address for {company} and return only the email address in plain text.")

    # Here you would typically send the entity_data to Groq for processing
    # For now, let's assume Groq just returns the emails from the extracted data
    groq_result = {"results": [{"company": data["company"], "emails": data["emails"]} for data in entity_data]}

    # Display extracted information
    st.write("Extracted Information:")
    if 'results' in groq_result:
        extracted_df = pd.DataFrame(groq_result['results'])
        st.dataframe(extracted_df)

        # Option to Download as CSV
        csv = extracted_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="extracted_data.csv",
            mime="text/csv"
        )
