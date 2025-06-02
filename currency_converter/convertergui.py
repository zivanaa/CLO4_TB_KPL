def get_converter_content():
    """
    Generate HTML content for currency converter page
    """
    return """
    <head>
        <link rel="stylesheet" href="/static/style_converter.css">
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
                                    <select id="from-currency"></select>
                                </div>
                              
                            <div class="form-group">
                                <label for="to-currency">To Currency</label>
                                <select id="to-currency"></select>
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

            !-- Quick Menu Mode -->
            <div class="mode-content" id="quick-mode">
                <div class="converter-card">
                    <h3>⚡ Quick Convert</h3>
                    <div class="form-group">
                        <label for="quick-amount">Amount</label>
                        <input type="number" id="quick-amount" step="0.01" min="0" value="100" />
                    </div>
                    <br>
                    <div class="quick-menu" id="quick-menu">
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
    const API_KEY = "99af1e52e8b504f480478eda";
    
    const QUICK_CONVERSIONS = {
        "1": { desc: "USD to EUR", from: "USD", to: "EUR" },
        "2": { desc: "USD to IDR", from: "USD", to: "IDR" },
        "3": { desc: "USD to JPY", from: "USD", to: "JPY" },
        "4": { desc: "IDR to USD", from: "IDR", to: "USD" },
        "5": { desc: "EUR to USD", from: "EUR", to: "USD" },
        "6": { desc: "Show all from IDR", from: "IDR", to: null },
        };
    
    async function populateCurrencyOptions() {
      try {
        const response = await fetch(`https://v6.exchangerate-api.com/v6/${API_KEY}/codes`);
        const data = await response.json();
        if (data.result !== "success") throw new Error("API failed");

        const options = data.supported_codes.map(
          ([code, name]) => `<option value="${code}">${code} - ${name}</option>`
        ).join("");

        document.getElementById('from-currency').innerHTML = options;
        document.getElementById('to-currency').innerHTML = options;

        populateQuickMenu(data.supported_codes.slice(0, 6)); // First 6 pairs
      } catch (error) {
        showError("Failed to load currency list.");
        console.error(error);
      }
    }
    
    function populateQuickMenu() {
        const menu = document.getElementById("quick-menu");
        let html = "";

        Object.entries(QUICK_CONVERSIONS).forEach(([id, { desc, from, to }]) => {
            html += `
            <div class="quick-option" onclick="${to ? `quickConvert('${from}', '${to}')` : `showAllFromIDR()`}">
                <h4>${desc}</h4>
                <p>${from}${to ? ` to ${to}` : ' to all currencies'}</p>
            </div>
            `;
        });

        menu.innerHTML = html;
    }
    
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