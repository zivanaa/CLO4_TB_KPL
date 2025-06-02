from converter import generate_currency_options

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


    async function convertCurrency() {
      const amount = parseFloat(document.getElementById("amount").value);
      const from = document.getElementById("from-currency").value;
      const to = document.getElementById("to-currency").value;
      const showAll = document.getElementById("show-all").checked;

      if (!amount || amount <= 0) return showError("Enter valid amount");

      showLoading();

      try {
        if (showAll) {
          await showAllConversionsAPI(amount, from);
        } else {
          const result = await getConversionRate(from, to);
          showSingleResult(amount, from, to, amount * result);
        }
      } catch (e) {
        showError(e.message);
      }

      hideLoading();
    }

    async function quickConvert(from, to) {
      const amount = parseFloat(document.getElementById("quick-amount").value || 100);
      showLoading();

      try {
        const rate = await getConversionRate(from, to);
        showSingleResult(amount, from, to, amount * rate);
      } catch (e) {
        showError(e.message);
      }

      hideLoading();
    }

    function showAllFromIDR() {
        const amount = parseFloat(document.getElementById("quick-amount").value || 100);
        showLoading();

        showAllConversionsAPI(amount, "IDR", ["USD", "EUR", "JPY"])
            .then(() => hideLoading())
            .catch(error => {
            showError("Conversion failed: " + error.message);
            hideLoading();
            });
    }


    async function showAllConversionsAPI(amount, from, targetCurrencies = null) {
        const response = await fetch(`https://v6.exchangerate-api.com/v6/${API_KEY}/latest/${from}`);
        const data = await response.json();

        if (data.result !== "success") {
            throw new Error("Failed to fetch conversion data.");
        }

        const rates = data.conversion_rates;

        const html = Object.entries(rates)
            .filter(([code]) => {
            if (code === from) return false;
            return targetCurrencies ? targetCurrencies.includes(code) : true;
            })
            .map(([code, rate]) => `
            <div class="result-item">
                <span class="currency-code">${code}</span>
                <span class="currency-value">${(rate * amount).toLocaleString(undefined, { maximumFractionDigits: 2 })}</span>
            </div>
            `).join("");

        document.getElementById("result-title").textContent =
            targetCurrencies ? `${amount} ${from} to selected currencies` : `${amount} ${from} to all currencies`;

        document.getElementById("result-content").innerHTML = html;
        showResults();
        hideError();
    }


    async function getConversionRate(from, to) {
      if (from === to) return 1;
      const response = await fetch(`https://v6.exchangerate-api.com/v6/${API_KEY}/pair/${from}/${to}`);
      const data = await response.json();
      if (data.result !== "success") throw new Error(`Cannot convert ${from} to ${to}`);
      return data.conversion_rate;
    }

    function showSingleResult(amount, from, to, result) {
      document.getElementById("result-title").textContent = "Conversion Result";
      document.getElementById("result-content").innerHTML = `
        <div class="result-item">
          <span class="currency-code">${amount} ${from}</span>
          <span class="currency-value">${result.toLocaleString(undefined, { maximumFractionDigits: 2 })} ${to}</span>
        </div>`;
      showResults();
    }

    function switchMode(mode) {
      document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');

      document.querySelectorAll('.mode-content').forEach(content => content.classList.remove('active'));
      document.getElementById(mode + "-mode").classList.add("active");

      hideResults();
    }

    function showError(message) {
      const el = document.getElementById("error-message");
      el.textContent = message;
      el.classList.add("show");
      hideResults();
    }

    function showLoading() {
      document.getElementById("loading").classList.add("show");
      hideError();
    }

    function hideLoading() {
      document.getElementById("loading").classList.remove("show");
    }

    function hideError() {
      document.getElementById("error-message").classList.remove("show");
    }

    function showResults() {
      document.getElementById("result-section").classList.add("show");
    }

    function hideResults() {
      document.getElementById("result-section").classList.remove("show");
    }

    document.addEventListener("DOMContentLoaded", () => {
        document.getElementById("amount").value = 100;
        populateCurrencyOptions(); // Memuat <select>
        populateQuickMenu();       // Memuat Quick Menu khusus
    });
    </script>
    """