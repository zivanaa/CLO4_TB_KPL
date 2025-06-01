from flask import Flask, render_template
from landing_page import get_landing_content
from all_currencies import get_all_currencies_content
from convertergui import get_converter_content
from history import get_history_content

app = Flask(__name__)

@app.route('/')
def home():
    content = get_landing_content()
    return render_template("sidebar.html", 
                           title="Welcome to Currency Hub", 
                           content=content, 
                           page="home")

@app.route('/currencies')
def currencies():
    content = get_all_currencies_content()
    return render_template("sidebar.html", 
                           title="All Currencies", 
                           content=content, 
                           page="currencies")

@app.route('/converter')
def converter():
    content = get_converter_content()
    return render_template("sidebar.html", 
                           title="Currency Converter", 
                           content=content, 
                           page="converter")

@app.route('/history')
def history():
    content = get_history_content()
    return render_template("sidebar.html", 
                           title="Conversion History", 
                           content=content, 
                           page="history")

if __name__ == '__main__':
    print("🚀 Starting Currency Hub...")
    print("📱 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
