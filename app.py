from flask import Flask,render_template,request
import requests,os
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["Content-Length"] = "0"
MAX_FILE_SIZE = 1024 * 1024 + 1
api_url = 'https://patw1h5276.execute-api.eu-west-1.amazonaws.com/beta/upload'

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}
    if request.method == "POST":
        file = request.files["file"]

        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/json"
            file.stream.seek(0)
            content = file.read()
            files = {'file': content}
            if(args["file_size_error"] == False):
                resp =requests.post(api_url,headers=headers, files=files,verify =False)
                args["response_status_code"] = resp.status_code
             
            args["method"] = "POST"
    return render_template("upload.html", args=args)
