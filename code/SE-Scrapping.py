import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.glassdoor.com/Job/software-engineer-jobs.htm"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs_data = []
    job_cards = soup.find_all('div', class_='jobCard')

    for card in job_cards:
        try:
            company = card.find('div', class_='jobCardCompany').text.strip()
        except AttributeError:
            company = "N/A"

        try:
            company_score = card.find('span', class_='ratingNumber').text.strip()
        except AttributeError:
            company_score = "N/A"

        try:
            job_title = card.find('a', class_='jobTitle').text.strip()
        except AttributeError:
            job_title = "N/A"

        try:
            location = card.find('span', class_='jobLocation').text.strip()
        except AttributeError:
            location = "N/A"

        try:
            date = card.find('div', class_='jobDate').text.strip()
        except AttributeError:
            date = "N/A"

        try:
            salary = card.find('span', class_='salary').text.strip()
        except AttributeError:
            salary = "N/A"

        jobs_data.append({
            "Company": company,
            "Company Score": company_score,
            "Job Title": job_title,
            "Location": location,
            "Date": date,
            "Salary": salary
        })

    csv_file = "software_engineer_jobs.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Company", "Company Score", "Job Title", "Location", "Date", "Salary"])
        writer.writeheader()
        writer.writerows(jobs_data)

    print(f"Data saved to {csv_file}")

else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
