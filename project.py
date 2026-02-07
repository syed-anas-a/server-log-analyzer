import re, sys
import sys
from tabulate import tabulate
import argparse
import json
import csv

def main():

    args = parse_arguments()
    data = regex(args.file_dir, int(args.n))
    arg_analysis(data, args)

#parsing CL arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description = "Log request analyzer => (the analysis has been limited to initial 1000 requests)")

    #default functionality
    parser.add_argument("file_dir", help="log file location")
    parser.add_argument("n", nargs="?", type=int, default=1000, help="parses and displays n logs (default=1000)")

    #top Ns
    parser.add_argument("--top-ips", type=int, help="Displays N IPs with most visits")
    parser.add_argument("--top-urls", type=int, help="Displays N URLs with most requests")
    parser.add_argument("--top-days", type=int, help="Displays N days with most traffic")
    parser.add_argument("--top-hours", type=int, help="Displays N hours with most traffic")

    #bytes/bandwidth
    parser.add_argument("--top-bytes-by-url", type=int, help="Show top N URLS by total bytes transferred")
    parser.add_argument("--top-bytes-by-ip", type=int, help="Show top N IPs by total bytes transferred")

    #methods & status
    parser.add_argument("--methods", action="store_true", help="Displays counts of each method type")
    parser.add_argument("--status", action="store_true", help="Displays counts of success and failed statuses")

    #export results
    parser.add_argument("--export", nargs="?", type=str, default=None, help="exports results to given filename & format (json or csv). Note: export supports only one request at once if multiple requests most recent one is handled.")

    #parsing CL argument
    return parser.parse_args()

#analysis of argument requests
def arg_analysis(data, args):

        default_view = True

        if args.top_ips:
            limit = args.top_ips
            result = top_ips(data, limit)
            header = ["IP", "NO. OF REQUESTS"]
            if args.export:
                export_file(result[:limit], args.export, header)
            else:
                print(tabulate(result[:limit], headers=header, tablefmt = "grid"))
            default_view = False

        if args.top_urls:
            limit = args.top_urls
            result = top_urls(data, limit)
            header = ["URL", "NO. OF REQUESTS"]
            if args.export:
                export_file(result[:limit], args.export, header)
            else:
                print(tabulate(result[:limit], headers=header, tablefmt = "grid"))
            default_view = False

        if args.top_days:
            limit = args.top_days
            result = top_days(data, limit)
            header = ["DAY", "NO. OF REQUESTS"]
            if args.export:
                export_file(result[:limit], args.export, header)
            else:
                print(tabulate(result[:limit], headers=header, tablefmt = "grid"))
            default_view = False

        if args.top_hours:
            limit = args.top_hours
            result = top_hours(data, limit)
            header = ["HOUR", "NO. OF REQUESTS"]
            if args.export:
                export_file(result[:limit], args.export, header)
            else:
                print(tabulate(result[:limit], headers=header, tablefmt = "grid"))
            default_view = False

        if args.top_bytes_by_ip:
            limit = args.top_bytes_by_ip
            result = bytes_by_ip(data, limit)
            header = ["IP", "BYTES TRANSFERRED"]
            if args.export:
                export_file(result[:limit], args.export, header)
            else:
                print(tabulate(result[:limit], headers=header, tablefmt = "grid"))
            default_view = False

        if args.top_bytes_by_url:
            limit = args.top_bytes_by_url
            result = bytes_by_url(data, limit)
            header = ["URL", "BYTES TRANSFERRED"]
            if args.export:
                export_file(result[:limit], args.export, header)
            else:
                print(tabulate(result[:limit], headers=header, tablefmt = "grid"))
            default_view = False

        if args.methods:
            result = method_counts(data)
            header = ["METHOD", "COUNT"]
            if args.export:
                export_file(result, args.export, header)
            else:
                print(tabulate(result, headers=header, tablefmt = "grid"))
            default_view = False

        if args.status:
            result = status_counts(data)
            header = ["STATUS CODE", "COUNT"]
            if args.export:
                export_file(result, args.export, header)
            else:
                print(tabulate(result, headers=header, tablefmt = "grid"))
            default_view = False

        if default_view:
            if args.export:
                    if args.export.endswith(".csv"):
                        fieldnames = ["ip","date","time","utc","method","path","prot","status","size"]
                        with open(args.export, "w", newline="", encoding="utf-8") as line:
                            writer = csv.DictWriter(line, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(data)
                            print(f"exported results to {args.export}!!")
                    else:
                        with open(args.export, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4)
                            print(f"exported results to {args.export}!!")
            else:
                print(tabulate(data[:args.n], headers = "keys", tablefmt = "grid"))

def export_file(result, filename, header):
    if filename.endswith(".json"):
        with open(filename, 'w', encoding="utf-8") as obj:
            json.dump(result, obj, indent=2)
            print(f"exported results to {filename}!!")
            return
    elif filename.endswith(".csv"):
        with open(filename, 'w', newline="", encoding="utf-8") as line:
            writer = csv.writer(line)
            writer.writerow(header)
            writer.writerows(result)
            print(f"exported results to {filename}!!")
            return
    else:
        print("Unsupperted export file format!!")
        sys.exit()

# regex parsing the raw fille
def regex(file, n):
    with open(file, 'r', encoding = "utf-8") as f:
        count = 0
        logs = []
        for line in f:
            count += 1
            line = line.strip()
            if query := re.search(r"""
                    ^(?P<ip>\S+)\s-\s-\s
                    \[
                        (?P<date>\d{2}/[a-zA-Z]+/\d{4})
                        :
                        (?P<time>\d{2}:\d{2}:\d{2})\s+
                        (?P<utc>[+-]\d{4})
                    \]\s+
                    "
                        (?P<method>[A-Z]+)\s+
                        (?P<path>\S+)[\s+|"]?
                        (?P<prot>HTTP/\d+\.\d)?
                    "\s+
                        (?P<status>\d{3})\s+
                        (?P<size>\d+|-)
                    $
            """, line, re.VERBOSE):

                logs.append(query.groupdict())

            else:
                print("Pattern Error at line ", count)
                sys.exit()

            if (count == n):
                return logs

#counts path/url visits
def top_urls(data, n):
    counts = {}
    for entry in data:
        key = entry["path"]
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:n]

#counts top ips
def top_ips(data, n):
    counts = {}
    c = 0
    for entry in data:
        key = entry["ip"]
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:n]

#counts top days
def top_days(data, n):
    counts = {}
    c = 0
    for entry in data:
        key = entry["date"]
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:n]

#counts traffic by top hours
def top_hours(data, n):
    counts = {}
    c = 0
    for entry in data:
        key = (entry["time"].split(":"))[0]
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:n]

#counts bytes transferred by url/path
def bytes_by_url(data, n):
    bytesUrl = {}
    c = 0
    for entry in data:
        value = entry["size"]
        try:
            value = int(value)
        except ValueError:
            value = 0

        key = entry["path"]
        if key in bytesUrl:
            bytesUrl[key] = value + bytesUrl[key]
        else:
            bytesUrl[key] = value
    sorted_counts = sorted(bytesUrl.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:n]

#counts bytes transferred by ip
def bytes_by_ip(data, n):
    bytesIp = {}
    c = 0
    for entry in data:
        value = entry["size"]
        try:
            value = int(value)
        except ValueError:
            value = 0

        key = entry["ip"]
        if key in bytesIp:
            bytesIp[key] = value + bytesIp[key]
        else:
            bytesIp[key] = value
    sorted_counts = sorted(bytesIp.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:n]

#counts each status
def status_counts(data):
    counts = {}
    for entry in data:
        key = entry["status"]
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts

#counts each method type
def method_counts(data):
    counts = {}
    for entry in data:
        key = entry["method"]
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts



if __name__ == "__main__":
    main()
