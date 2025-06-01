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
    """