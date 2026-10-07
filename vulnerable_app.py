"""
INTENTIONALLY VULNERABLE CODE - for testing SonarQube / SAST pipelines only.
Do NOT deploy. All credentials below are fake.
"""
import hashlib
import os
import pickle
import random
import sqlite3
import subprocess
import xml.etree.ElementTree as ET

import requests
import yaml
from flask import Flask, request, make_response

app = Flask(__name__)

# [Hotspot/Vuln] Hard-coded credentials & secrets
DB_PASSWORD = "admin123"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
API_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"


# [Vuln] SQL Injection (string concatenation / f-string in query)
@app.route("/user")
def get_user():
    username = request.args.get("name")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return str(cursor.fetchall())


# [Vuln] OS Command Injection
@app.route("/ping")
def ping():
    host = request.args.get("host")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


# [Vuln] Code Injection via eval()
@app.route("/calc")
def calc():
    expr = request.args.get("expr")
    return str(eval(expr))


# [Vuln] Path Traversal
@app.route("/read")
def read_file():
    filename = request.args.get("file")
    with open("/var/data/" + filename, "r") as f:
        return f.read()


# [Vuln] Reflected XSS
@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return make_response("<h1>Hello " + name + "</h1>")


# [Vuln] Insecure deserialization (pickle)
@app.route("/load", methods=["POST"])
def load_data():
    data = request.get_data()
    obj = pickle.loads(data)
    return str(obj)


# [Vuln] Unsafe YAML load
def parse_config(text):
    return yaml.load(text)


# [Vuln] XML External Entity (XXE) / untrusted XML parsing
def parse_xml(xml_string):
    return ET.fromstring(xml_string)


# [Vuln] Weak hashing algorithms (MD5 / SHA1) for passwords
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def hash_token(token):
    return hashlib.sha1(token.encode()).hexdigest()


# [Hotspot] Insecure randomness for security-sensitive value
def generate_session_token():
    return str(random.random())


# [Vuln] SSL certificate verification disabled
def fetch_external(url):
    return requests.get(url, verify=False).text


# [Vuln] Insecure temp file / world-writable permissions
def save_report(data):
    path = "/tmp/report.txt"
    with open(path, "w") as f:
        f.write(data)
    os.chmod(path, 0o777)


# [Code Smell] Bare except, swallowed exception
def risky():
    try:
        return 1 / 0
    except:
        pass


# [Code Smell] Duplicate code / unused variable / empty function
def unused_example():
    unused_var = 42


if __name__ == "__main__":
    # [Hotspot] Debug mode enabled & binding to all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
