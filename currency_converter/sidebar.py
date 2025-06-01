from flask import Flask, render_template_string
from landing_page import get_landing_content
from all_currencies import get_all_currencies_content
from convertergui import get_converter_content
from config import get_supported_currencies
from history import get_history_content
app = Flask(__name__)

# Template HTML dengan sidebar dan footer
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currency Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            height: 100vh;
            overflow: hidden;
        }

        .container {
            display: flex;
            height: 100vh;
        }

        .sidebar {
            width: 280px;
            background: linear-gradient(180deg, #16213e 0%, #0f3460 100%);
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }

        .sidebar-header {
            padding: 30px 20px;
            text-align: center;
            border-bottom: 1px solid rgba(233, 69, 96, 0.2);
        }

        .sidebar-header h1 {
            font-size: 24px;
            color: #e94560;
            margin-bottom: 5px;
        }

        .sidebar-header p {
            font-size: 14px;
            color: #888;
        }

        .nav-menu {
            padding: 20px 0;
        }

        .nav-item {
            margin: 8px 0;
        }

        .nav-link {
            display: flex;
            align-items: center;
            padding: 15px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }

        .nav-link:hover {
            background: rgba(233, 69, 96, 0.1);
            border-left-color: #e94560;
            transform: translateX(5px);
        }

        .nav-link.active {
            background: rgba(233, 69, 96, 0.2);
            border-left-color: #e94560;
        }

        .nav-link .icon {
            font-size: 20px;
            margin-right: 15px;
            width: 25px;
            text-align: center;
        }

        .nav-link .text {
            font-size: 16px;
            font-weight: 500;
        }

        .main-content {
            flex: 1;
            background: #1a1a2e;
            overflow-y: auto;
            position: relative;
        }

        .content-header {
            background: rgba(15, 52, 96, 0.5);
            padding: 20px 30px;
            border-bottom: 1px solid rgba(233, 69, 96, 0.2);
            backdrop-filter: blur(10px);
        }

        .content-body {
            padding: 30px;
            padding-bottom: 100px; /* Space for footer */
            min-height: calc(100vh - 80px);
        }

        .page-content {
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            background: rgba(15, 52, 96, 0.3);
            padding: 25px;
            border-radius: 15px;
            border-left: 4px solid #e94560;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }

        .card h3 {
            color: #e94560;
            margin-bottom: 15px;
            font-size: 24px;
        }

        .card p {
            color: #ccc;
            line-height: 1.6;
            font-size: 16px;
        }

        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            left: 280px; /* Start after sidebar */
            background: linear-gradient(180deg, #0f3460 0%, #16213e 100%);
            border-top: 1px solid rgba(233, 69, 96, 0.2);
            padding: 15px 30px;
            z-index: 100;
            backdrop-filter: blur(10px);
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .footer-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .footer-logo {
            font-size: 20px;
            color: #e94560;
            font-weight: bold;
        }

        .footer-text {
            color: #888;
            font-size: 14px;
        }

        .footer-links {
            display: flex;
            gap: 25px;
        }

        .footer-link {
            color: #ccc;
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s ease;
        }

        .footer-link:hover {
            color: #e94560;
        }

        .footer-social {
            display: flex;
            gap: 15px;
        }

        .social-link {
            color: #888;
            font-size: 18px;
            text-decoration: none;
            transition: all 0.3s ease;
            padding: 8px;
            border-radius: 50%;
            background: rgba(233, 69, 96, 0.1);
        }

        .social-link:hover {
            color: #e94560;
            background: rgba(233, 69, 96, 0.2);
            transform: translateY(-2px);
        }

        .mobile-toggle {
            display: none;
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            cursor: pointer;
        }

        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                height: 100vh;
                z-index: 999;
                transform: translateX(-100%);
            }

            .sidebar.open {
                transform: translateX(0);
            }

            .main-content {
                width: 100%;
            }

            .mobile-toggle {
                display: block;
            }

            .content-header {
                padding-left: 80px;
            }

            .footer {
                left: 0; /* Full width on mobile */
            }

            .footer-content {
                flex-direction: column;
                text-align: center;
                gap: 10px;
            }

            .footer-links {
                justify-content: center;
            }

            .footer-social {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>

        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h1>💰 Currency Hub</h1>
                <p>Your financial companion</p>
            </div>
            
            <nav class="nav-menu">
                <div class="nav-item">
                    <a href="/" class="nav-link {{ 'active' if page == 'home' else '' }}">
                        <span class="icon">🏠</span>
                        <span class="text">Home</span>
                    </a>
                </div>
                <div class="nav-item">
                    <a href="/currencies" class="nav-link {{ 'active' if page == 'currencies' else '' }}">
                        <span class="icon">🌍</span>
                        <span class="text">All Currencies</span>
                    </a>
                </div>
                <div class="nav-item">
                    <a href="/converter" class="nav-link {{ 'active' if page == 'converter' else '' }}">
                        <span class="icon">🔄</span>
                        <span class="text">Converter</span>
                    </a>
                </div>
                <div class="nav-item">
                    <a href="/history" class="nav-link {{ 'active' if page == 'history' else '' }}">
                        <span class="icon">📊</span>
                        <span class="text">History</span>
                    </a>
                </div>
            </nav>
        </div>

        <div class="main-content">
            <div class="content-header">
                <h2>{{ title }}</h2>
            </div>
            
            <div class="content-body">
                <div class="page-content">
                    {{ content | safe }}
                </div>
            </div>

            <footer class="footer">
                <div class="footer-content">
                    <div class="footer-left">
                        <div class="footer-logo">💰 Currency Hub</div>
                        <div class="footer-text">© 2024 All rights reserved</div>
                    </div>
                    
                    <div class="footer-links">
                        <a href="#" class="footer-link">About</a>
                        <a href="#" class="footer-link">Privacy</a>
                        <a href="#" class="footer-link">Terms</a>
                        <a href="#" class="footer-link">Contact</a>
                    </div>
                    
                    <div class="footer-social">
                        <a href="#" class="social-link" title="Twitter">🐦</a>
                        <a href="#" class="social-link" title="LinkedIn">💼</a>
                        <a href="#" class="social-link" title="GitHub">🐙</a>
                        <a href="#" class="social-link" title="Email">📧</a>
                    </div>
                </div>
            </footer>
        </div>
    </div>

    <script>
        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
        }

        document.addEventListener('click', function(event) {
            if (window.innerWidth <= 768) {
                const sidebar = document.getElementById('sidebar');
                const toggleBtn = document.querySelector('.mobile-toggle');
                
                if (!sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
                    sidebar.classList.remove('open');
                }
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    content = get_landing_content()
    return render_template_string(template, 
                                title="Welcome to Currency Hub", 
                                content=content, 
                                page="home")

@app.route('/currencies')
def currencies():
    content = get_all_currencies_content()
    return render_template_string(template, 
                                title="All Currencies", 
                                content=content, 
                                page="currencies")

@app.route('/converter')
def converter():
    content = get_converter_content()
    return render_template_string(template, 
                                title="Currency Converter", 
                                content=content, 
                                page="converter")

@app.route('/history')
def history():
    content = get_history_content()
    return render_template_string(template, 
                                title="Conversion History", 
                                content=content, 
                                page="history")

if __name__ == '__main__':
    print("🚀 Starting Currency Hub...")
    print("📱 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
