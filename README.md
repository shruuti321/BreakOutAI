# Data Query Dashboard
## Project Video
[Watch the video](https://drive.google.com/file/d/12__LLMAdtEc7bFWDvEa8OXXDDXn0w5Dv/view?usp=sharing)

## Project Description

The **Data Query Dashboard** is a web application that allows users to:
- Upload and process CSV files or retrieve data from Google Sheets
- Perform web searches based on custom queries using the SerpAPI
- Extract key information, such as email addresses, from search results using Groq AI
- Visualize and export processed data to CSV


This project comprises two components:
1. A **backend Flask API** (`app/app.py`) to handle data processing, API integration, and Groq processing
2. A **Streamlit-based frontend** (`dashboard/dashboard.py`) for an interactive dashboard interface


## Setup Instructions

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- Pip (Python package installer)


### Step 1: Clone the Repository

Clone the repository and navigate into the project directory:
```bash
git clone 
cd 
```


### Step 2: Install Dependencies

For the Backend, navigate to the app directory and install the dependencies:
```bash
cd app
pip install -r requirements.txt
```

For the Dashboard, navigate to the dashboard directory and install the dependencies:
```bash
cd ../dashboard
pip install -r requirements.txt
```


### Step 3: Configure API Keys and Environment Variables

**SERPAPI Key:**
- Obtain an API key from SerpAPI and add it to the SERP_API_KEY variable in `app/app.py`


**Groq API Key:**
- Obtain an API key from Groq and set it in your environment variables:
```bash
export GROQ_API_KEY='your_groq_api_key'
```

Alternatively, you can hardcode the key into `app/app.py` under the `os.environ["GROQ_API_KEY"]` variable.


### Step 4: Run the Backend Flask Server

Navigate to the app directory and start the Flask server:
```bash
cd app
python app.py
```

The server will be available at:
http://127.0.0.1:5000


### Step 5: Launch the Streamlit Dashboard

In a separate terminal, navigate to the dashboard directory and run the Streamlit app:
```bash
cd dashboard
streamlit run dashboard.py
```

The dashboard will be available at:
http://localhost:8501

## Usage Guide

### Upload CSV or Link Google Sheet

* **Upload a CSV File**: Use the "Upload a CSV File" section to upload your dataset. Select the main column to extract entities and create queries.
* **Link a Google Sheet**: Enter the Google Sheet ID in the "Link Google Sheet" section. Ensure the sheet is publicly accessible (anyone with the link can view).


### Define and Run Custom Queries

* Enter a query template (e.g., `Get me the email address of {company}`) to generate queries dynamically based on the main column data.
* Click **Perform Web Search for Queries** to fetch search results.


### Process Data with Groq

* Use the search results and prompt templates to process data with Groq AI.
* Extract key information (e.g., emails) and download it as a CSV.


### API Keys and Environment Variables

* **SERP_API_KEY**: Used to fetch web search results via SerpAPI. Add this key to the `SERP_API_KEY` variable in `app.py`.
* **GROQ_API_KEY**: Used for AI processing via Groq. Set this key in your environment as `GROQ_API_KEY` or directly in `app.py`.
