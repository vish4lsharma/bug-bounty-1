# app.py
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

app = Flask(__name__)

s = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
s.mount('http://', adapter)
s.mount('https://', adapter)

def get_all_forms(url):
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    try:
        response_content = response.content.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError while processing response: {e}")
        response_content = None

    if response_content:
        response_content = response_content.lower()
        for error in errors:
            if error in response_content:
                return True

    return False

def scan_sql_injection(url):
    for c in "\"'":
        new_url = f"{url}{c}"
        print("[!] Trying", new_url)
        res = s.get(new_url)
        if is_vulnerable(res):
            filepath = 'C:/workspace/Vulnerability_Scanner/Project/media/Vulscan.txt'
            f = open(filepath, "a+")
            forms = get_all_forms(url)
            len_form = len(forms)
            f.write("\n [+]  SQL Injection vulnerability detected, link: " + url )
            f.write("\n [+] Detected " + str(len_form) + " forms on " + url)
            f.close()
            return
        else:
            filepath = 'C:/workspace/Vulnerability_Scanner/Project/media/Vulscan.txt'
            f = open(filepath, "a+")
            forms = get_all_forms(url)
            len_form = len(forms)
            f.write("\n [+]  SQL Injection vulnerability not detected, link: " + url )
            f.write("\n [+] Detected " + str(len_form) + " forms on " + url)
            f.close()

    forms = get_all_forms(url)
    len_form = len(forms)
    print(f"[+] Detected {len_form} forms on {url}.")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{c}"
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            if is_vulnerable(res):
                print("[+] SQL Injection vulnerability detected, link:", url)
                print("[+] Form:", form_details)
                filepath = 'C:/workspace/Vulnerability_Scanner/Project/media/Vulscan.txt'
                f = open(filepath, "a+")
                f.write("\n [+]  SQL Injection vulnerability detected, link: " + url )
                f.write("\n [*] Form details:" + str(form_details))
                f.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target')
    scan_sql_injection(target)
    return render_template('thank_you.html', target=target)

if __name__ == "__main__":
    app.run(debug=True)
