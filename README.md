# 💼 Dream Job Finder – Terminal Job Search with CSV Export

## Overview  
This project is a terminal-based job search tool that leverages the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/) to fetch real-time job listings based on user-defined criteria. It also saves search results in CSV format for future reference.

## Features  
- 🔍 Search for jobs by role and location  
- 🌍 Filter by remote jobs  
- 💰 Filter by minimum salary  
- ⏰ Filter by job type (Full-time, Part-time, Contract, etc.)  
- 📝 Save search results in CSV files (timestamped)  
- 🖥️ CLI-based interface, ideal for automation or personal workflows

## How It Works  
1. The user inputs job role, location, and preferences (remote, salary, job type).  
2. The tool calls the JSearch API and fetches results across multiple pages.  
3. Results are shown in the terminal and saved as a CSV file named with role, location, and timestamp.

## Technologies Used  
- Python  
- Requests  
- JSearch API via RapidAPI  
- CSV for result export

## Usage Instructions

### 1. Install Required Package
```bash
pip install requests
```
### 2. Replace the API Key
Replace "your_api_key" in the script with your RapidAPI JSearch key.
### 3. Run the Script
```bash
python dream_job_finder.py
```
### 4. Input Parameters
The program will ask for:
- Role/Keyword (e.g., "Data Analyst")
- Location (e.g., "Dallas, TX")
- Remote-only? (y/n)
- Minimum salary (optional)
- Job Type filter (optional)
- Number of jobs (up to ~200)
### 5. View Results
Jobs will be printed in the terminal and saved in job_searches/<role>_<location>_<timestamp>.csv
