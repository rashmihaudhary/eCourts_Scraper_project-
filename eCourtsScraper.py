import requests
import datetime
import argparse
from bs4 import BeautifulSoup
import json

# Function to get case details from eCourts
def get_case_details(cnr, case_type, case_number, year):
    url = f"https://services.ecourts.gov.in/ecourtindia_v6/case_details"  # This is a placeholder URL
    params = {
        "cnr": cnr,
        "case_type": case_type,
        "case_number": case_number,
        "year": year
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract details like court name and serial number
    court_name = soup.find("court_name").text
    serial_number = soup.find("serial_number").text
    case_date = soup.find("case_date").text

    return court_name, serial_number, case_date

# Function to check if the case is listed today or tomorrow
def is_case_listed(case_date):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # Extract date from case details
    case_date = datetime.datetime.strptime(case_date, '%Y-%m-%d').date()

    if case_date == today:
        return "Today"
    elif case_date == tomorrow:
        return "Tomorrow"
    else:
        return "Not Listed"

# Function to download the case PDF (if available)
def download_pdf(pdf_url):
    response = requests.get(pdf_url)
    with open('case_pdf.pdf', 'wb') as f:
        f.write(response.content)

# Function to download the entire cause list for today
def download_cause_list():
    url = "https://services.ecourts.gov.in/causelist"  # Placeholder URL
    response = requests.get(url)
    cause_list = response.json()

    with open('cause_list.json', 'w') as file:
        json.dump(cause_list, file)

# Function to save results in JSON format
def save_results(data):
    with open('results.json', 'w') as file:
        json.dump(data, file)

# Command-line interface parsing
def parse_args():
    parser = argparse.ArgumentParser(description="eCourts Scraper")
    parser.add_argument('--today', action='store_true', help='Fetch cases listed today')
    parser.add_argument('--tomorrow', action='store_true', help='Fetch cases listed tomorrow')
    parser.add_argument('--causelist', action='store_true', help='Download the entire cause list')
    parser.add_argument('--cnr', type=str, help="Case Number (CNR)")
    parser.add_argument('--case_type', type=str, help="Case Type")
    parser.add_argument('--case_number', type=str, help="Case Number")
    parser.add_argument('--year', type=str, help="Year of Case")
    return parser.parse_args()

def main():
    args = parse_args()

    # If 'today' or 'tomorrow' flag is set, fetch the cause list
    if args.causelist:
        download_cause_list()
        print("Cause list for today downloaded successfully.")

    # If case details are provided, fetch those
    if args.cnr and args.case_type and args.case_number and args.year:
        court_name, serial_number, case_date = get_case_details(
            args.cnr, args.case_type, args.case_number, args.year
        )

        # Check if the case is listed today or tomorrow
        case_status = is_case_listed(case_date)

        # Prepare the results
        case_info = {
            "case_number": args.case_number,
            "court_name": court_name,
            "serial_number": serial_number,
            "status": case_status
        }

        print(f"Case Status: {case_status}")
        print(f"Court: {court_name}")
        print(f"Serial Number: {serial_number}")

        # Optionally, save results
        save_results(case_info)

if __name__ == "__main__":
    main()
