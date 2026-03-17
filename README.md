# Conversational AI Dashboard for Business Intelligence

## Overview

This project is a simple prototype that allows users to generate data dashboards using plain English queries.
Instead of writing SQL queries or using complex BI tools, a user can just type a question like:

"Show views by category"
or
"Which region has the highest engagement?"

The system processes the question, retrieves the relevant data from the dataset, and automatically generates charts and insights.

The goal of this project is to make data analysis easier for non-technical users such as managers, analysts, or business executives.

---

## Problem Statement

In many companies, large amounts of data are stored in databases but accessing that information requires technical knowledge such as SQL or advanced BI tools.

Because of this:

* Non-technical users cannot easily explore the data
* Data teams receive many repetitive requests for simple reports
* Important insights take longer to access

This project tries to solve that problem by building a conversational interface that can generate dashboards automatically.

---

## Features

* Ask questions in natural language
* Automatically analyze the dataset
* Generate charts dynamically
* Display insights in a simple dashboard
* Interactive visualizations

Example queries:

* Show views by category
* Top 10 videos by views
* Compare likes and comments by region
* Show engagement by language
* Views trend over time

---

## Tech Stack

Frontend
Streamlit

Backend
Python

Visualization
Plotly

AI Integration
Google Gemini API

Data Source
CSV dataset

---

## Project Structure

```
project-folder
│
├── app.py
├── dataset_loader.py
├── query_processor.py
├── chart_generator.py
├── insights_generator.py
├── requirements.txt
├── README.md
└── dataset.csv
```

---

## How It Works

The system follows a simple pipeline:

User Question
↓
AI interprets the question
↓
Query is generated to extract relevant data
↓
Data is processed using pandas
↓
Charts are generated using Plotly
↓
Interactive dashboard is displayed

---

## Deployment link:
https://ai-dashboard-6hy2.onrender.com/

---
## Running the Project

Clone the repository

```
git clone <your-repository-link>
```

Go to the project folder

```
cd project-folder
```

Install dependencies

```
pip install -r requirements.txt
```

Run the application

```
streamlit run app.py
```

---

## Future Improvements

Some improvements that can be added in the future:

* Support for uploading custom datasets
* Better query understanding
* Multiple charts in a single dashboard
* Follow-up conversational queries
* Export dashboards as reports

---

## Conclusion

This project demonstrates how conversational AI can simplify the way people interact with data. By combining natural language processing with data visualization, it becomes possible for anyone to explore insights without technical knowledge.

The prototype shows the potential of AI-driven dashboards for faster and more accessible business intelligence.
