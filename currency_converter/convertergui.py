def get_converter_content():
    """
    Generate HTML content for currency converter page
    """
    return """
    <head>
        <link rel="stylesheet" href="/static/css/style1.css">
    </head>
    <body>
        <div class="converter-container">
            <div class="header">
                <h1>Currency Converter</h1>
                <p>Convert currencies with real-time exchange rates</p>
            </div>

            <div class="mode-selector">
                <button class="mode-btn active" onclick="switchMode('flexible')">
                    🌐 Flexible Mode
                </button>
                <button class="mode-btn" onclick="switchMode('quick')">
                    ⚡ Quick Menu
                </button>
            </div>

        <div class="converter-modes">
            <!-- Flexible Mode -->
            <div class="mode-content active" id="flexible-mode">
                <div class="converter-card">
                    <h3>🌐 Flexible Converter</h3>
                    <div class="converter-form">
                        <div class="form-group">
                            <label for="amount">Amount</label>
                            <input type="number" id="amount" step="0.01" min="0" />
                        </div>
                          
                        <div class="form-row">
                            <div class="form-group">
                                <label for="from-currency">From Currency</label>
                                <select id="from-currency">
                                    <option value="USD">USD - US Dollar</option>
                                    <option value="EUR">EUR - Euro</option>
                                    <option value="IDR">IDR - Indonesian Rupiah</option>
                                    <option value="JPY">JPY - Japanese Yen</option>
                                    <option value="GBP">GBP - British Pound</option>
                                    <option value="AUD">AUD - Australian Dollar</option>
                                    <option value="CAD">CAD - Canadian Dollar</option>
                                    <option value="CHF">CHF - Swiss Franc</option>
                                    <option value="CNY">CNY - Chinese Yuan</option>
                                    <option value="SGD">SGD - Singapore Dollar</option>
                                </select>
                            </div>
                              
                            <div class="form-group">
                                <label for="to-currency">To Currency</label>
                                <select id="to-currency">
                                    <option value="IDR">IDR - Indonesian Rupiah</option>
                                    <option value="USD">USD - US Dollar</option>
                                    <option value="EUR">EUR - Euro</option>
                                    <option value="JPY">JPY - Japanese Yen</option>
                                    <option value="GBP">GBP - British Pound</option>
                                    <option value="AUD">AUD - Australian Dollar</option>
                                    <option value="CAD">CAD - Canadian Dollar</option>
                                    <option value="CHF">CHF - Swiss Franc</option>
                                    <option value="CNY">CNY - Chinese Yuan</option>
                                    <option value="SGD">SGD - Singapore Dollar</option>
                                </select>
                            </div>
                        </div>

                        <div class="form-group">
                            <label>
                                <input type="checkbox" id="show-all" style="width: auto; margin-right: 10px;" />
                                Show conversions to all currencies
                            </label>
                        </div>
                          
                        <button class="convert-btn" onclick="convertCurrency()">
                            Convert Currency 💱
                         </button>
                    </div>
                </div>
            </div>

            <!-- Quick Menu Mode -->
            <div class="mode-content" id="quick-mode">
                <div class="converter-card">
                    <h3>⚡ Quick Convert</h3>
                    <div class="form-group">
                        <label for="quick-amount">Amount</label>
                        <input type="number" id="quick-amount" step="0.01" min="0" value="100" />
                    </div>
                    <br>
                    <div class="quick-menu" id="quick-menu">
                        <div class="quick-menu">
                            <div class="quick-option" onclick="quickConvert('USD', 'EUR')">
                                <h4>💵 USD to EUR</h4>
                                <p>US Dollar to Euro</p>
                            </div>
                            <div class="quick-option" onclick="quickConvert('USD', 'IDR')">
                                <h4>💵 USD to IDR</h4>
                                <p>US Dollar to Indonesian Rupiah</p>
                            </div>
                            <div class="quick-option" onclick="quickConvert('USD', 'JPY')">
                                <h4>💵 USD to JPY</h4>
                                <p>US Dollar to Japanese Yen</p>
                            </div>
                            <div class="quick-option" onclick="quickConvert('IDR', 'USD')">
                                <h4>🇮🇩 IDR to USD</h4>
                                <p>Indonesian Rupiah to US Dollar</p>
                            </div>
                            <div class="quick-option" onclick="quickConvert('EUR', 'USD')">
                                <h4>🇪🇺 EUR to USD</h4>
                                <p>Euro to US Dollar</p>
                            </div>
                            <div class="quick-option" onclick="showAllFromIDR()">
                                <h4>🇮🇩 All from IDR</h4>
                                <p>Indonesian Rupiah to all currencies</p>
                            </div>
                        <!-- Quick options populated dynamically -->
                    </div>
                </div>
            </div>
        </div>
                      
        <div class="loading" id="loading">
            <p>🔄 Converting currency...</p>
        </div>

        <div class="error-message" id="error-message"></div>

        <div class="error-message" id="error-message"></div>
            <div class="result-section" id="result-section">
            <div class="result-title" id="result-title"></div>
            <div id="result-content"></div>
            </div>
        </div>
    </body>
    <script>
    // Sample exchange rates
        const exchangeRates = {
            USD: { EUR: 0.85, IDR: 15000, JPY: 110, GBP: 0.73, AUD: 1.35, CAD: 1.25, CHF: 0.92, CNY: 6.45, SGD: 1.35 },
            EUR: { USD: 1.18, IDR: 17650, JPY: 129.5, GBP: 0.86, AUD: 1.59, CAD: 1.47, CHF: 1.08, CNY: 7.6, SGD: 1.59 },
            IDR: { USD: 0.000067, EUR: 0.000057, JPY: 0.0073, GBP: 0.000049, AUD: 0.00009, CAD: 0.000083, CHF: 0.000061, CNY: 0.00043, SGD: 0.00009 },
            JPY: { USD: 0.0091, EUR: 0.0077, IDR: 136.4, GBP: 0.0066, AUD: 0.012, CAD: 0.011, CHF: 0.0084, CNY: 0.059, SGD: 0.012 },
            GBP: { USD: 1.37, EUR: 1.16, IDR: 20550, JPY: 150.7, AUD: 1.85, CAD: 1.71, CHF: 1.26, CNY: 8.84, SGD: 1.85 },
            AUD: { USD: 0.74, EUR: 0.63, IDR: 11100, JPY: 81.5, GBP: 0.54, CAD: 0.93, CHF: 0.68, CNY: 4.78, SGD: 1.0 },
            CAD: { USD: 0.8, EUR: 0.68, IDR: 12000, JPY: 88, GBP: 0.58, AUD: 1.08, CHF: 0.74, CNY: 5.16, SGD: 1.08 },
            CHF: { USD: 1.09, EUR: 0.93, IDR: 16350, JPY: 119.6, GBP: 0.79, AUD: 1.47, CAD: 1.36, CNY: 7.03, SGD: 1.47 },
            CNY: { USD: 0.155, EUR: 0.132, IDR: 2325, JPY: 17.05, GBP: 0.113, AUD: 0.209, CAD: 0.194, CHF: 0.142, SGD: 0.209 },
            SGD: { USD: 0.74, EUR: 0.63, IDR: 11100, JPY: 81.5, GBP: 0.54, AUD: 1.0, CAD: 0.93, CHF: 0.68, CNY: 4.78 }
        };
        
        function switchMode(mode) {
            // Update buttons
            document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            // Update content
            document.querySelectorAll('.mode-content').forEach(content => content.classList.remove('active'));
            document.getElementById(mode + '-mode').classList.add('active');

            // Hide results
            hideResults();
        }

    </script>
    """