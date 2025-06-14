from flask import Flask, render_template
from landing_page import get_landing_content
from all_currencies import get_all_currencies_content
from convertergui import get_converter_content
from history import get_history_content

app = Flask(__name__)

def render_page(title, content, page):
    """
    Helper function to render pages with consistent template structure
    """
    return render_template("sidebar.html", title=title, content=content, page=page)

@app.route('/')
def home():
    return render_page("Welcome to Currency Hub", get_landing_content(), "home")

@app.route('/currencies')
def currencies():
    return render_page("All Currencies", get_all_currencies_content(), "currencies")

@app.route('/converter')
def converter():
    return render_page("Currency Converter", get_converter_content(), "converter")

@app.route('/history')
def history():
    return render_page("Conversion History", get_history_content(), "history")

if __name__ == '__main__':
    print("\U0001F680 Starting Currency Hub...")
    print("\U0001F4F1 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
