from project import regex, bytes_by_ip, status_counts, top_urls

#sample data to test functions which expects a list of dicts
data = [
    {"ip": "127.0.0.1", "date": "01/Jan/2025", "time": "10:00:00", "utc": "-0400",
     "method": "GET", "path": "/index.html", "prot": "HTTP/1.1",
     "status": "200", "size": "500"},

    {"ip": "192.168.0.1", "date": "01/Jan/2025", "time": "10:05:00", "utc": "-0400",
     "method": "POST", "path": "/login", "prot": "HTTP/1.1",
     "status": "401", "size": "300"},

    {"ip": "127.0.0.1", "date": "01/Jan/2025", "time": "11:00:00", "utc": "-0400",
     "method": "GET", "path": "/about.html", "prot": "HTTP/1.1",
     "status": "200", "size": "700"},

    {"ip": "10.0.0.5", "date": "02/Jan/2025", "time": "09:30:00", "utc": "-0400",
     "method": "GET", "path": "/index.html", "prot": "HTTP/1.1",
     "status": "404", "size": "250"},

    {"ip": "192.168.0.1", "date": "02/Jan/2025", "time": "09:45:00", "utc": "-0400",
     "method": "GET", "path": "/dashboard", "prot": "HTTP/1.1",
     "status": "200", "size": "1200"},
]

#testing regex function using the main log file
def test_regex():
    assert regex("access.log", 3) == [{'ip': 'in24.inetnebr.com', 'date': '01/Aug/1995', 'time': '00:00:01', 'utc': '-0400', 'method': 'GET', 'path': '/shuttle/missions/sts-68/news/sts-68-mcc-05.txt', 'prot': 'HTTP/1.0', 'status': '200', 'size': '1839'}, {'ip': 'uplherc.upl.com', 'date': '01/Aug/1995', 'time': '00:00:07', 'utc': '-0400', 'method': 'GET', 'path': '/', 'prot': 'HTTP/1.0', 'status': '304', 'size': '0'}, {'ip': 'uplherc.upl.com', 'date': '01/Aug/1995', 'time': '00:00:08', 'utc': '-0400', 'method': 'GET', 'path': '/images/ksclogo-medium.gif', 'prot': 'HTTP/1.0', 'status': '304', 'size': '0'}]

# testing other functionalities using sample data above
def test_top_urls():
    assert top_urls(data, 2) == [('/index.html', 2), ('/login', 1)]

def test_bytes_by_ip():
    assert bytes_by_ip(data, 3) == [("192.168.0.1", 1500), ("127.0.0.1", 1200), ("10.0.0.5", 250)]

def test_status_counts():
    assert status_counts(data, 3) == [("200", 3), ("401", 1), ("404", 1)]


