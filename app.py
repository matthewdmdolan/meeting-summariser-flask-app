from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    current_app
)
import urllib.request
from urllib.parse import urlparse, urljoin
from summarizer import Summarizer
from summarizer.sbert import SBertSummarizer
from bs4 import BeautifulSoup
from static import *
import requests, validators, uuid, pathlib, os
import werkzeug.utils
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os

# Using an instance of SBERT to create the model
model = SBertSummarizer('paraphrase-MiniLM-L6-v2')

app = Flask(__name__)

@app.route("/")
def msg():
    return render_template('index.html')

@app.route('/getfile', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':
        file = request.files['myfile']
        filename = secure_filename(file.filename)
        file.save(os.path.join("/Users/mattdolan/PycharmProjects/python/flask-app/textfiles", filename))

        with open(os.path.join("/Users/mattdolan/PycharmProjects/python/flask-app/textfiles", filename), 'rb') as f:
            file_content_bytes = f.read()

        try:
            file_content = file_content_bytes.decode('utf-8-sig')
        except UnicodeDecodeError:
            try:
                file_content = file_content_bytes.decode('ISO-8859-1')
            except UnicodeDecodeError:
                file_content = "The uploaded file contains characters that could not be decoded."

        # Parse the HTML
        soup = BeautifulSoup(file_content_bytes, 'html.parser')
        # Find all paragraph elements
        paragraphs = soup.find_all('p')
        # Create a list to store the lines
        lines = []
        # Loop over each paragraph
        for para in paragraphs:
            # Get the text of the paragraph
            text = para.get_text(strip=True)

            # Only add to the list if the text is not empty
            if text:
                # Replace '**' with '' in the string (to remove bold formatting)
                text = text.replace('**', '')
                # Add to the list
                lines.append(text)

        # Print each line
        for line in lines:
            print(line)

        lines_string = str(lines)
        result = model(lines_string, num_sentences=10)
        print(result)

        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
