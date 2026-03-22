# PROJECT TITLE : "Server Log Analyzer"

## Personal Details:
Name : SYED ANAS ALI
GitHub username : syed-anas-a
edX username : syed_anas86
city, country : Bengaluru, India
Date recorded : 19th September 2025

## Description
This project is a Server Log Analyzer built in Python as my final project for CS50P. Its purpose is to parse and analyze server access logs stored in the standard format called the Common Log Format (CLF), also known as the NCSA Common Log Format, and extracts key information such as IP addresses, dates, methods, URLs, status codes, and bytes transferred. The program organizes this data and provides structured insights into web traffic.

With features like identifying top IPs, URLs, and traffic by day, counting status codes, and calculating bandwidth usage, the analyzer demonstrates Python concepts including regex, file I/O, data structures, argparse, and tabulate. Results can be displayed in clean tables or exported to CSV/JSON for further use.

#### Log file details:
- 📂 File name: access.log
- 📊 Source: NASA Kennedy Space Center (collected in August 1995)
- 📍 Hosted on Kaggle as: NASA HTTP Access Logs

### Functionality / Features of the program:
1. Top N IPs by number of requests
2. Top N URLs (paths) by frequency of visits
3. Top N days and N hours by traffic volume
4. Status code counts, distinguishing successful, failed, and error requests
5. Bandwidth usage: bytes transferred grouped by IP or by URL
6. Additionally, the user can optionally export the results into a seperate file in either .json or .csv type file_format in a command format  filename.file_format (ex: output.csv).
7. I have also implemented 4 test functions in a file called test_project.py in the “root” of my project with the same name as my custom functions, prepended with test_ (test_custom_function). The test functions tests the fundamental functions of the program and any redundant or highly similar functions are skipped for testing.

### Notes:
1. The program can handle multiple functionality to display comprehensive view of key elements like ips, urls, traffic by days, hours, etc.
2. The program though can only handle exporting functionality for one request at once. For example : if user requests top IPS and top URLS it can very well display the data in taular view but can only export one at a time.
3. If user requests export of results the program reads the most latest request and export the result.
Ex: python project.py access.log --top-ips 20 --top-urls 20 --export output.csv
The program will only export results for top-urls (top 20)

- - For demonstration, a trimmed access.log file (first 1000 lines) is included in the project root. This ensures the project is lightweight while still showcasing all functionality. The program works equally well with larger log files if provided by the user.

### Python Concepts used in project:
1. Data Handling : File parsing and handling structured/unstructured text
2. Regular expressions : searching pattern for extracting data
3. Data Structures : Dictionaries, Lists, Tuples for grouping, storing and counting data
4. Sorting functions with lambdas
5. Argparse : Command-line argument parsing with argparse
6. Data Visualisation : Pretty-printing tables with the third-party tabulate library
7. File I/O : JSON and CSV export functionality for saving results

## File Architecture:
1. project.py : Main program file containing all functions (regex, top_ips, top_urls, status_counts, etc.) and the main function.
2. test_project.py : Contains pytest unit tests for key functions like regex, top_urls, and bytes_by_ip, redundant function tests are avoided in test_project.py
3. requirements.txt : Specifies external libraries required. For this project: pytest==8.4.2, tabulate==0.9.0
4. access.log : A trimmed sample log file (1000 lines) included for demonstration and testing. The analyzer works with any larger or different log file when provided the log file has a NCSA Common Log Format.
5. README.md : This file. Provides project documentation.

### Usage:
Run the program with:
```bash
python project.py access.log [optional_arguments]
Available options:
    -   N : Display N rows of log data (default=1000)
    -   --top-ips N  : Show top N IP addresses by request count
    -	--top-urls N : Show top N requested URLs
    -	--top-days N : Show top N days by traffic volume
    -	--status     : Show counts of HTTP status codes
    -	--methods    : Show counts of HTTP methods
    -	--top-bytes-by-ip      : Show top N IPS by total bytes transferred
    -	--top-bytes-by-url     : Show top N URLS by total bytes transferred
    -	--export filename.csv/json : Export results to file (CSV or JSON)
```
### Testing:
```bash
pytest test_project.py
```
