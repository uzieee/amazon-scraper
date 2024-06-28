from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/scrape', methods=['POST'])
def scrape():
    print("Scrape")
    keywords = request.json.get('keywords', [])
    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400
    print(keywords)
    results = {}
    for keyword in keywords:        
        # Define the filename for each keyword
        filename = f'{keyword}.json'
        
        # Remove the existing file if it exists
        if os.path.exists(filename):
            os.remove(filename)

        # Run the Scrapy spider
        process = subprocess.Popen(
            ['scrapy', 'crawl', 'amazonSpider', '-a', f'keywords={keyword}'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        # Handle potential errors in the Scrapy process
        if process.returncode != 0:
            return jsonify({'error': stderr.decode('utf-8')}), 500

        # Read results from the file
        if os.path.exists(filename):
            with open(filename) as f:
                results[keyword] = json.load(f)
        else:
            results[keyword] = []

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

#second
