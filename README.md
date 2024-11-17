# Data Query Dashboard

## Project Description

The **Data Query Dashboard** is a web application that allows users to:

- Upload and process CSV files or retrieve data from Google Sheets.
- Perform web searches based on custom queries using the SerpAPI.
- Extract key information, such as email addresses, from search results using Groq AI.
- Visualize and export processed data to CSV.

This project comprises two components:

1. A **backend Flask API** (`app/app.py`) to handle data processing, API integration, and Groq processing.
2. A **Streamlit-based frontend** (`dashboard/dashboard.py`) for an interactive dashboard interface.

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Pip (Python package installer)

### Step 1: Clone the Repository

Clone the repository and navigate into the project directory:

```bash
git clone <repository_url>
cd <repository_name>
