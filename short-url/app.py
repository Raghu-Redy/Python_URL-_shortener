from flask import Flask, render_template, request, redirect
import hashlib

app = Flask(__name__)

# Dictionary to store original URLs and their corresponding short URLs
url_mapping = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form['url']
    # Create a unique hash for the URL
    hash = hashlib.sha1(url.encode()).hexdigest()[:6]
    # Store the URL and hash in the url_mapping dictionary
    url_mapping[hash] = url
    return render_template('shorten.html', short_url=hash)

@app.route('/<short_url>')
def redirect_url(short_url):
    # Lookup the original URL corresponding to the short URL in the url_mapping dictionary
    original_url = url_mapping.get(short_url)
    if original_url:
        try:
            return redirect(original_url)
        except Exception as e:
            print(f'Error: {e}')
            return 'Error: Unable to redirect'
    else:
        return "URL not found"

if __name__ == '__main__':
    app.run(debug=True)
