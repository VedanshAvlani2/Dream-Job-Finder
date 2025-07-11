import requests
import csv
import os
from datetime import datetime
import time

# ---------------------
# CONFIG
# ---------------------
RAPIDAPI_KEY = "your_api_key"
API_URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}


# ---------------------
# BACKEND: API Query
# ---------------------
def query_jobs(role, location, remote=False, total_results=10, min_salary=None, job_type=None):
    results = []
    jobs_per_page = 10
    max_pages = min((total_results // jobs_per_page) + 1, 20) 

    for page in range(1, max_pages + 1):
        params = {
            "query": role,
            "location": location,
            "remote": "true" if remote else "false",
            "num_pages": 1,
            "page": page
        }
        time.sleep(0.5)

        try:
            response = requests.get(API_URL, headers=HEADERS, params=params, timeout=30)
            response.raise_for_status()
            page_data = response.json().get("data", [])
            
            for job in page_data:
                if len(results) >= total_results:
                    break
                if min_salary and (not job.get("job_min_salary") or job["job_min_salary"] < min_salary):
                    continue
                if job_type and (job.get("job_employment_type", "").lower() != job_type.lower()):
                    continue
                results.append(job)
        except requests.exceptions.RequestException as e:
            print(f"❌ API error on page {page}: {e}")
            break

        if len(results) >= total_results:
            break

    return results

def save_to_csv(jobs, role, location):
    if not jobs:
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{role.replace(' ', '_')}_{location.replace(' ', '_')}_{timestamp}.csv"
    folder = "job_searches"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Job Title", "Company", "Location", "Employment Type", "Remote", 
            "Min Salary", "Max Salary", "Apply Link", "Description"
        ])
        for job in jobs:
            writer.writerow([
                job.get("job_title", "N/A"),
                job.get("employer_name", "N/A"),
                f"{job.get('job_city', '')}, {job.get('job_country', '')}",
                job.get("job_employment_type", "N/A"),
                "Yes" if job.get("job_is_remote") else "No",
                job.get("job_min_salary", ""),
                job.get("job_max_salary", ""),
                job.get("job_apply_link", ""),
                job.get("job_description", "")[:200]
            ])

    print(f"\n✅ Results saved to: {filepath}")

if __name__ == "__main__":
    print("🔍 Dream Job Finder (Terminal Version)")
    role = input("Enter job role or keywords: ")
    location = input("Enter location (e.g. Dallas, TX): ")
    remote_only = input("Remote only? (y/n): ").strip().lower() == 'y'
    num = int(input("Number of jobs to fetch (e.g. 5, 10): "))
    
    try:
        salary_filter = input("Minimum salary? (leave blank to skip): ")
        min_salary = int(salary_filter) if salary_filter.strip().isdigit() else None
    except:
        min_salary = None
    
    job_type = input("Filter by job type (Full-time, Part-time, Contract, etc. - leave blank to skip): ").strip()

    print("\n🔄 Searching for jobs...\n")
    results = query_jobs(role, location, remote_only, num, min_salary, job_type)

    if not results:
        print("❌ No jobs found with the given criteria.")
    else:
        for idx, job in enumerate(results, 1):
            print(f"\n{idx}. {job.get('job_title')} at {job.get('employer_name')}")
            print(f"📍 {job.get('job_city')}, {job.get('job_country')} | Remote: {'Yes' if job.get('job_is_remote') else 'No'}")
            print(f"💼 Type: {job.get('job_employment_type', 'N/A')} | 💰 ${job.get('job_min_salary', '')} - ${job.get('job_max_salary', '')}")
            print(f"🔗 Apply: {job.get('job_apply_link')}")
            print(f"📝 {job.get('job_description', '')[:300]}...\n")
            print("-" * 80)

        save_to_csv(results, role, location)
