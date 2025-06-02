def get_converter_content():
    """
    Generate HTML content for currency converter page
    """
    return """
    <head>
        <style>
            .converter-container {
                animation: fadeIn 0.8s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .mode-selector {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 40px;
            }
            
            .mode-btn {
            padding: 15px 30px;
            background: linear-gradient(145deg, #0f3460 0%, #16213e 100%);
            border: 2px solid transparent;
            border-radius: 15px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
            font-weight: 600;
            }
            
            .mode-btn:hover {
                border-color: #e94560;
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3);
            }

            .mode-btn.active {
                background: linear-gradient(145deg, #e94560 0%, #d63447 100%);
                border-color: #e94560;
                box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4);
            }
            
            .converter-modes {
            display: grid;
            gap: 30px;
            }

            .mode-content {
                display: none;
                animation: slideIn 0.5s ease;
            }

            .mode-content.active {
                display: block;
            }
            
            @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
            }

            .converter-form {
                display: grid;
                gap: 20px;
            }

            .form-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            
            label {
            font-weight: 600;
            color: #ccc;
            font-size: 1rem;
            }

            input, select {
                padding: 15px;
                background: rgba(26, 26, 46, 0.8);
                border: 2px solid rgba(233, 69, 96, 0.3);
                border-radius: 10px;
                color: white;
                font-size: 1rem;
                transition: all 0.3s ease;
            }

            input:focus, select:focus {
                outline: none;
                border-color: #e94560;
                box-shadow: 0 0 15px rgba(233, 69, 96, 0.3);
            }
            
            .convert-btn {
            padding: 18px 40px;
            background: linear-gradient(145deg, #e94560 0%, #d63447 100%);
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            }

            .convert-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(233, 69, 96, 0.4);
            }

            .convert-btn:active {
                transform: translateY(0);
            }
            
            .result-section {
            margin-top: 30px;
            padding: 20px;
            background: rgba(26, 26, 46, 0.5);
            border-radius: 15px;
            border-left: 4px solid #e94560;
            display: none;
            }

            .result-section.show {
                display: block;
                animation: slideUp 0.5s ease;
            }

            @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .result-title {
                color: #e94560;
                font-size: 1.3rem;
                margin-bottom: 15px;
                font-weight: 600;
            }

            .result-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 0;
                border-bottom: 1px solid rgba(233, 69, 96, 0.1);
            }

            .result-item:last-child {
                border-bottom: none;
            }
            
            .currency-code {
            font-weight: 600;
            color: #e94560;
            }

            .currency-value {
                font-size: 1.1rem;
                color: white;
            }
            
            .quick-menu {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            }

            .quick-option {
                background: rgba(26, 26, 46, 0.6);
                border: 2px solid rgba(233, 69, 96, 0.2);
                border-radius: 15px;
                padding: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .quick-option:hover {
                border-color: #e94560;
                background: rgba(233, 69, 96, 0.1);
                transform: translateY(-3px);
            }

            .quick-option h4 {
                color: #e94560;
                font-size: 1.2rem;
                margin-bottom: 10px;
            }
            
            .quick-option p {
            color: #ccc;
            font-size: 0.9rem;
            }
            
            .loading {
                display: none;
                text-align: center;
                color: #e94560;
                font-size: 1.1rem;
                margin-top: 20px;
            }

            .loading.show {
                display: block;
            }
            
            .error-message {
            background: rgba(220, 53, 69, 0.2);
            border: 1px solid #dc3545;
            color: #ff6b7a;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
            }

            .error-message.show {
                display: block;
                animation: shake 0.5s ease;
            }
        </style>
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
        
        function convertCurrency() {
            const amount = parseFloat(document.getElementById('amount').value);
            const fromCurrency = document.getElementById('from-currency').value;
            const toCurrency = document.getElementById('to-currency').value;
            const showAll = document.getElementById('show-all').checked;

            if (!amount || amount <= 0) {
                showError('Please enter a valid amount');
                return;
            }

            showLoading();

            setTimeout(() => {
                try {
                    if (showAll) {
                        showAllConversions(amount, fromCurrency);
                    } else {
                        const result = performConversion(amount, fromCurrency, toCurrency);
                        showSingleResult(amount, fromCurrency, toCurrency, result);
                    }
                } catch (error) {
                    showError('Conversion failed: ' + error.message);
                }
                hideLoading();
            }, 800);
        }
        
        function quickConvert(from, to) {
            const amount = parseFloat(document.getElementById('quick-amount').value) || 100;
            
            showLoading();

            setTimeout(() => {
                try {
                    const result = performConversion(amount, from, to);
                    showSingleResult(amount, from, to, result);
                } catch (error) {
                    showError('Conversion failed: ' + error.message);
                }
                hideLoading();
            }, 800);
        }
        
        function showAllFromIDR() {
            const amount = parseFloat(document.getElementById('quick-amount').value) || 100;
            
            showLoading();

            setTimeout(() => {
                try {
                    showAllConversions(amount, 'IDR');
                } catch (error) {
                    showError('Conversion failed: ' + error.message);
                }
                hideLoading();
            }, 800);
        }
        
        function performConversion(amount, from, to) {
            if (from === to) {
                return amount;
            }

            if (!exchangeRates[from] || !exchangeRates[from][to]) {
                throw new Error(Conversion from ${from} to ${to} not supported);
            }

            return amount * exchangeRates[from][to];
        }
        
        function showSingleResult(amount, from, to, result) {
            const resultSection = document.getElementById('result-section');
            const resultTitle = document.getElementById('result-title');
            const resultContent = document.getElementById('result-content');

            resultTitle.textContent = 💱 Conversion Result;
            resultContent.innerHTML = `
                <div class="result-item">
                    <span class="currency-code">${amount} ${from}</span>
                    <span class="currency-value">${result.toLocaleString(undefined, {maximumFractionDigits: 2})} ${to}</span>
                </div>
            `;

            resultSection.classList.add('show');
            hideError();
        }
        
        function showAllConversions(amount, from) {
            const resultSection = document.getElementById('result-section');
            const resultTitle = document.getElementById('result-title');
            const resultContent = document.getElementById('result-content');

            resultTitle.textContent = 📊 ${amount} ${from} to all currencies;

            let html = '';
            const currencies = Object.keys(exchangeRates);
            
            currencies.forEach(currency => {
                if (currency !== from) {
                    try {
                        const result = performConversion(amount, from, currency);
                        html += `
                            <div class="result-item">
                                <span class="currency-code">${currency}</span>
                                <span class="currency-value">${result.toLocaleString(undefined, {maximumFractionDigits: 2})}</span>
                            </div>
                        `;
                    } catch (error) {
                        // Skip unsupported conversions
                    }
                }
            });

            resultContent.innerHTML = html;
            resultSection.classList.add('show');
            hideError();
        }
        
        function showLoading() {
            document.getElementById('loading').classList.add('show');
            hideResults();
            hideError();
        }
        
        function hideLoading() {
            document.getElementById('loading').classList.remove('show');
        }
        
        function showError(message) {
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = '❌ ' + message;
            errorElement.classList.add('show');
            hideResults();
        }
        
        function hideError() {
            document.getElementById('error-message').classList.remove('show');
        }
        
        function hideResults() {
            document.getElementById('result-section').classList.remove('show');
        }

    </script>
    """
    
# Currency conversion logic
class CurrencyConverter:
    def _init_(self):
        # Sample exchange rates (in production, fetch from API)
        self.exchange_rates = {
            'USD': {'EUR': 0.85, 'IDR': 15000, 'JPY': 110, 'GBP': 0.73, 'AUD': 1.35, 'CAD': 1.25, 'CHF': 0.92, 'CNY': 6.45, 'SGD': 1.35},
            'EUR': {'USD': 1.18, 'IDR': 17650, 'JPY': 129.5, 'GBP': 0.86, 'AUD': 1.59, 'CAD': 1.47, 'CHF': 1.08, 'CNY': 7.6, 'SGD': 1.59},
            'IDR': {'USD': 0.000067, 'EUR': 0.000057, 'JPY': 0.0073, 'GBP': 0.000049, 'AUD': 0.00009, 'CAD': 0.000083, 'CHF': 0.000061, 'CNY': 0.00043, 'SGD': 0.00009},
            'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'IDR': 136.4, 'GBP': 0.0066, 'AUD': 0.012, 'CAD': 0.011, 'CHF': 0.0084, 'CNY': 0.059, 'SGD': 0.012},
            'GBP': {'USD': 1.37, 'EUR': 1.16, 'IDR': 20550, 'JPY': 150.7, 'AUD': 1.85, 'CAD': 1.71, 'CHF': 1.26, 'CNY': 8.84, 'SGD': 1.85},
            'AUD': {'USD': 0.74, 'EUR': 0.63, 'IDR': 11100, 'JPY': 81.5, 'GBP': 0.54, 'CAD': 0.93, 'CHF': 0.68, 'CNY': 4.78, 'SGD': 1.0},
            'CAD': {'USD': 0.8, 'EUR': 0.68, 'IDR': 12000, 'JPY': 88, 'GBP': 0.58, 'AUD': 1.08, 'CHF': 0.74, 'CNY': 5.16, 'SGD': 1.08},
            'CHF': {'USD': 1.09, 'EUR': 0.93, 'IDR': 16350, 'JPY': 119.6, 'GBP': 0.79, 'AUD': 1.47, 'CAD': 1.36, 'CNY': 7.03, 'SGD': 1.47},
            'CNY': {'USD': 0.155, 'EUR': 0.132, 'IDR': 2325, 'JPY': 17.05, 'GBP': 0.113, 'AUD': 0.209, 'CAD': 0.194, 'CHF': 0.142, 'SGD': 0.209},
            'SGD': {'USD': 0.74, 'EUR': 0.63, 'IDR': 11100, 'JPY': 81.5, 'GBP': 0.54, 'AUD': 1.0, 'CAD': 0.93, 'CHF': 0.68, 'CNY': 4.78}
        }
        
        self.currency_names = {
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'IDR': 'Indonesian Rupiah',
            'JPY': 'Japanese Yen',
            'GBP': 'British Pound',
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'SGD': 'Singapore Dollar'
        }
        
    def convert(self, amount, from_currency, to_currency):
        """Convert amount from one currency to another"""
        if from_currency == to_currency:
            return amount
        
        if from_currency not in self.exchange_rates:
            raise ValueError(f"Currency {from_currency} not supported")
        
        if to_currency not in self.exchange_rates[from_currency]:
            raise ValueError(f"Conversion from {from_currency} to {to_currency} not supported")
        
        rate = self.exchange_rates[from_currency][to_currency]
        return amount * rate
    
    def convert_to_all(self, amount, from_currency):
        """Convert amount to all available currencies"""
        results = {}
        
        if from_currency not in self.exchange_rates:
            raise ValueError(f"Currency {from_currency} not supported")
        
        for to_currency in self.exchange_rates[from_currency]:
            rate = self.exchange_rates[from_currency][to_currency]
            results[to_currency] = {
                'amount': amount * rate,
                'name': self.currency_names.get(to_currency, to_currency)
            }
        
        return results
    
    def get_supported_currencies(self):
        """Get list of supported currencies"""
        return list(self.currency_names.keys())
    
    def get_currency_name(self, currency_code):
        """Get full name of currency"""
        return self.currency_names.get(currency_code, currency_code)
    
    # Initialize converter instance
converter = CurrencyConverter()


def format_currency(amount, currency_code):
    """Format currency amount for display"""
    if currency_code == 'IDR':
        return f"Rp {amount:,.0f}"
    elif currency_code == 'JPY':
        return f"¥{amount:,.0f}"
    elif currency_code == 'USD':
        return f"${amount:,.2f}"
    elif currency_code == 'EUR':
        return f"€{amount:,.2f}"
    elif currency_code == 'GBP':
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency_code}"