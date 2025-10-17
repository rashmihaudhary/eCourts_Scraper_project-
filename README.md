# eCourts Scraper

This project is a Python script that fetches case details from the eCourts website.

## Setup and Installation

1. Clone this repository:
    ```bash
    git clone <repository_url>
    cd eCourts_Scraper_Project
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Fetching case details
To fetch case details, use the following CLI command:
```bash
python eCourtsScraper.py --cnr <CNR> --case_type <Case Type> --case_number <Case Number> --year <Year>
```

### Fetching cause list for today
To download the entire cause list for today:
```bash
python eCourtsScraper.py --causelist
```

### Flags
- `--today`: Fetch cases listed today.
- `--tomorrow`: Fetch cases listed tomorrow.
- `--causelist`: Download the entire cause list.

### Output

The results will be saved in `results.json` (for individual cases) and `cause_list.json` (for the full cause list).

## Conclusion

This script can be easily extended with additional functionality, such as fetching PDF files or querying the eCourts system with advanced filters.
