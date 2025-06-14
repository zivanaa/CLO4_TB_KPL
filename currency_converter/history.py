import json
import requests
import os
import datetime
from currency_data import load_currency_data, load_currency_history

HISTORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "currency_history.json")
RATE_HISTORY_FILE = os.path.join(os.path.dirname(__file__), "rate_history.json")

def save_history_to_file(data):
    """
    Menyimpan data konversi ke file JSON dengan timestamp.
    """
    history = {}
    if os.path.exists(HISTORY_FILE_PATH):
        try:
            with open(HISTORY_FILE_PATH, "r") as f:
                history = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load existing history: {e}")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history[timestamp] = data

    try:
        with open(HISTORY_FILE_PATH, "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to save history: {e}")

def load_history_from_file():
    """
    Memuat riwayat konversi dari file JSON.
    """
    if os.path.exists(HISTORY_FILE_PATH):
        try:
            with open(HISTORY_FILE_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load history file: {e}")
    return {}


def fetch_and_store_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        if response.status_code == 200 and "rates" in data:
            rates = data["rates"]
            history_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "base": data.get("base", "USD"),
                "rates": rates
            }

            filename = "rate_history.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    existing = json.load(f)
            else:
                existing = []

            existing.append(history_entry)

            with open(filename, "w") as f:
                json.dump(existing, f, indent=4)
            print("[INFO] Rates updated and saved.")
        else:
            print("[ERROR] Invalid response from API")
    except Exception as e:
        print(f"[ERROR] Failed to fetch rates: {e}")

def get_hourly_exchange_data(from_currency="USD", to_currency="IDR", amount=1):
    """
    Mengambil data perubahan kurs per jam untuk 24 jam terakhir.
    """
    currency_history = load_currency_history()
    if not currency_history:
        return []

    hourly_changes = list(currency_history.items())[-24:]
    results = []
    previous_rate = None

    for timestamp, rates in hourly_changes:
        if from_currency not in rates or to_currency not in rates:
            continue
        
        try:
            rate = rates[to_currency] / rates[from_currency]
            converted = rate * amount
            
            # Hitung perubahan dari sebelumnya
            change = 0
            change_percent = 0
            if previous_rate is not None:
                change = rate - previous_rate
                change_percent = (change / previous_rate) * 100 if previous_rate != 0 else 0
            
            results.append({
                'timestamp': timestamp,
                'rate': rate,
                'converted_amount': converted,
                'change': change,
                'change_percent': change_percent,
                'trend': 'up' if change > 0 else 'down' if change < 0 else 'stable',
                'from_currency': from_currency,
                'to_currency': to_currency,
                'amount': amount
            })
            
            previous_rate = rate
        except Exception as e:
            continue

    return results

def load_all_available_rates():
    """
    Load unique list of currencies from the last entry in rate_history.json
    """
    if not os.path.exists(RATE_HISTORY_FILE):
        return []
    try:
        with open(RATE_HISTORY_FILE, "r") as f:
            raw = json.load(f)
            if isinstance(raw, dict):
                last_entry = list(raw.values())[-1]
            elif isinstance(raw, list):
                last_entry = raw[-1]
            else:
                return []
            return sorted(list(last_entry.get("rates", {}).keys()))
    except Exception as e:
        print("[ERROR] Failed to load available currencies:", e)
        return []


def get_conversion_history():
    """
    Mengambil riwayat konversi yang telah disimpan.
    """
    history = load_history_from_file()
    formatted_history = []
    
    for timestamp, record in history.items():
        try:
            formatted_record = {
                'timestamp': timestamp,
                'amount': record.get("amount", "N/A"),
                'from_currency': record.get("from", "N/A"),
                'to_currency': record.get("to", "N/A"),
                'result': record.get("result", "N/A"),
                'rate': record.get("result", 0) / record.get("amount", 1) if record.get("amount", 0) != 0 else 0
            }
            formatted_history.append(formatted_record)
        except Exception as e:
            continue
    
    # Urutkan berdasarkan timestamp terbaru
    formatted_history.sort(key=lambda x: x['timestamp'], reverse=True)
    return formatted_history

def clear_conversion_history():
    """
    Menghapus semua riwayat konversi.
    """
    try:
        if os.path.exists(HISTORY_FILE_PATH):
            os.remove(HISTORY_FILE_PATH)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to clear history: {e}")
        return False

def get_history_stats():
    """
    Mendapatkan statistik dari riwayat konversi.
    """
    history = get_conversion_history()
    
    if not history:
        return {
            'total_conversions': 0,
            'most_used_from': 'N/A',
            'most_used_to': 'N/A',
            'total_amount_converted': 0
        }
    
    from_currencies = {}
    to_currencies = {}
    total_amount = 0
    
    for record in history:
        from_curr = record['from_currency']
        to_curr = record['to_currency']
        amount = record['amount']
        
        if from_curr != 'N/A':
            from_currencies[from_curr] = from_currencies.get(from_curr, 0) + 1
        if to_curr != 'N/A':
            to_currencies[to_curr] = to_currencies.get(to_curr, 0) + 1
        if isinstance(amount, (int, float)):
            total_amount += amount
    
    most_used_from = max(from_currencies.items(), key=lambda x: x[1])[0] if from_currencies else 'N/A'
    most_used_to = max(to_currencies.items(), key=lambda x: x[1])[0] if to_currencies else 'N/A'
    
    return {
        'total_conversions': len(history),
        'most_used_from': most_used_from,
        'most_used_to': most_used_to,
        'total_amount_converted': total_amount
    }
def get_hourly_rates():
    """
    Mengambil data kurs mata uang terbaru dari API exchangerate.host
    dan mengembalikan dictionary berisi base, rates, dan timestamp.
    """
    try:
        response = requests.get("https://api.exchangerate.host/latest")
        response.raise_for_status()
        data = response.json()
        return {
            "base": data.get("base", ""),
            "rates": data.get("rates", {}),
            "timestamp": data.get("timestamp", "")
        }
    except requests.RequestException as e:
        print(f"Error saat mengambil hourly rates: {e}")
        return {
            "base": "",
            "rates": {},
            "timestamp": ""
        }

def get_history_content():
    """
    Menghasilkan konten HTML untuk halaman history.
    """
    conversion_history = get_conversion_history()
    stats = get_history_stats()
    
    # Dapatkan data kurs per jam untuk contoh (USD ke IDR)
    hourly_data = get_hourly_exchange_data("USD", "IDR", 100)
    
    content = f'''
    <div class="history-container">
        <!-- Statistics Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-info">
                    <h3>{stats['total_conversions']}</h3>
                    <p>Total Conversions</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💱</div>
                <div class="stat-info">
                    <h3>{stats['most_used_from']}</h3>
                    <p>Most Used From</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-info">
                    <h3>{stats['most_used_to']}</h3>
                    <p>Most Used To</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-info">
                    <h3>{stats['total_amount_converted']:,.0f}</h3>
                    <p>Total Amount</p>
                </div>
            </div>
        </div>

        <!-- Tabs -->
        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="showTab('conversion-history')">
                    <span class="tab-icon">📋</span>
                    Conversion History
                </button>
                <button class="tab-btn" onclick="showTab('hourly-rates')">
                Hourly Rates    <span class="tab-icon">📈</span>
                    
                </button>
            </div>

            <!-- Conversion History Tab -->
            <div id="conversion-history" class="tab-content active">
                <div class="section-header">
                    <h3>Recent Conversions</h3>
                    <button class="clear-btn" onclick="clearHistory()">
                        <span class="btn-icon">🗑</span>
                        Clear History
                    </button>
                </div>
                
                <div class="history-list">
    '''
    
    if conversion_history:
        for record in conversion_history[:20]:  # Tampilkan 20 terakhir
            try:
                amount = record['amount']
                from_curr = record['from_currency']
                to_curr = record['to_currency']
                result = record['result']
                timestamp = record['timestamp']
                rate = record['rate']
                
                content += f'''
                    <div class="history-item">
                        <div class="history-main">
                            <div class="conversion-info">
                                <span class="amount">{amount:,.2f} {from_curr}</span>
                                <span class="arrow">→</span>
                                <span class="result">{result:,.2f} {to_curr}</span>
                            </div>
                            <div class="rate-info">
                                <span class="rate">Rate: {rate:.6f}</span>
                            </div>
                        </div>
                        <div class="history-meta">
                            <span class="timestamp">{timestamp}</span>
                        </div>
                    </div>
                '''
            except:
                continue
    else:
        content += '''
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <h3>No Conversion History</h3>
                <p>Start converting currencies to see your history here.</p>
            </div>
        '''
    
    content += '''
                </div>
            </div>

            <!-- Hourly Rates Tab -->
<div id="hourly-rates" class="tab-content">
    <div class="refresh-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: #1c1f3f; padding: 10px 15px; border-radius: 8px; border-left: 4px solid #4CAF50;">
        <span style="color: #4CAF50;">● Auto-refresh every hour</span>
        <span style="color: #ccc;">Last updated: <span id="lastUpdated"></span></span>
        <button onclick="refreshHourlyData()" style="background: #e94560; color: white; border: none; padding: 8px 14px; border-radius: 5px; cursor: pointer;">🔄 Refresh Now</button>
    </div>

    <div style="display: flex; gap: 20px; margin-bottom: 20px;">
        <div>
            <label for="fromCurrency">From Currency:</label><br>
            <select id="fromCurrency" onchange="refreshHourlyData()" style="padding: 6px; border-radius: 5px; background: #1a1d3d; color: white;">
            </select>
        </div>
        <div>
            <label for="toCurrency">To Currency:</label><br>
            <select id="toCurrency" onchange="refreshHourlyData()" style="padding: 6px; border-radius: 5px; background: #1a1d3d; color: white;">
            </select>
        </div>
    </div>

    <div class="rate-display" style="text-align: center; margin-bottom: 25px;">
        <div id="rateValue" style="font-size: 2.5rem; color: #e94560; font-weight: bold;">0.0000</div>
        <div id="rateDesc" style="color: #ccc;">1 USD = 0.0000 ???</div>
    </div>

    <div style="background: #1f223f; padding: 20px; border-radius: 12px; border-left: 4px solid #e94560;">
        <h3 id="chartTitle" style="color: #e94560; margin-bottom: 10px;">USD/IDR Hourly Rates</h3>
        <canvas id="hourlyChart"></canvas>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
let hourlyChart = null;

async function refreshHourlyData() {
    const from = document.getElementById('fromCurrency').value || 'USD';
    const to = document.getElementById('toCurrency').value || 'IDR';
    const res = await fetch(`/api/hourly-rates/${from}/${to}`);
    const data = await res.json();

    const labels = data.map(d => d.time);
    const rates = data.map(d => d.rate);
    const latestRate = rates[rates.length - 1] || 0;

    document.getElementById('rateValue').textContent = latestRate.toFixed(4);
    document.getElementById('rateDesc').textContent = `1 ${from} = ${latestRate.toFixed(4)} ${to}`;
    document.getElementById('chartTitle').textContent = `${from}/${to} Hourly Rates`;

    const ctx = document.getElementById(\"hourlyChart\").getContext(\"2d\");
    if (hourlyChart) hourlyChart.destroy();
    hourlyChart = new Chart(ctx, {
        type: \"line\",
        data: {
            labels: labels,
            datasets: [{
                label: `${from}/${to}`,
                data: rates,
                borderColor: \"#e94560\",
                backgroundColor: \"rgba(233, 69, 96, 0.2)\",
                fill: true,
                tension: 0.3,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();
}

async function populateCurrencySelectors() {
    const res = await fetch('/api/rates');
    const data = await res.json();
    if (!data.length) return;

    const latestRates = data[data.length - 1].rates;
    const selectorFrom = document.getElementById('fromCurrency');
    const selectorTo = document.getElementById('toCurrency');
    selectorFrom.innerHTML = selectorTo.innerHTML = '';

    for (let curr in latestRates) {
        selectorFrom.innerHTML += `<option value=\"${curr}\" ${curr === 'USD' ? 'selected' : ''}>${curr}</option>`;
        selectorTo.innerHTML += `<option value=\"${curr}\" ${curr === 'IDR' ? 'selected' : ''}>${curr}</option>`;
    }
}

window.onload = async function () {
    await populateCurrencySelectors();
    await refreshHourlyData();
};
</script>



    '''
    
    if hourly_data:
        for i, data in enumerate(hourly_data[-12:]):  # Tampilkan 12 jam terakhir
            trend_class = f"trend-{data['trend']}"
            change_symbol = "↗" if data['trend'] == 'up' else "↘" if data['trend'] == 'down' else "➡"
            
            # Format tanggal untuk display yang lebih baik
            try:
                # Parse ISO format timestamp
                dt = datetime.datetime.fromisoformat(data['timestamp'])
                time_display = dt.strftime("%H:%M")
                date_display = dt.strftime("%Y-%m-%d %H:%M")
            except:
                time_display = data['timestamp'][-5:] if len(data['timestamp']) > 5 else data['timestamp']
                date_display = data['timestamp']
            
            content += f'''
                <div class="hourly-item {trend_class}" onclick="showRateDetails({i}, '{data['timestamp']}', {data['rate']:.6f}, {data['converted_amount']:.2f}, {data['change']:.6f}, {data['change_percent']:.2f}, '{data['trend']}', '{data['from_currency']}', '{data['to_currency']}', {data['amount']})">
                    <div class="time-info">
                        <span class="time">{time_display}</span>
                        <span class="trend-icon">{change_symbol}</span>
                    </div>
                    <div class="rate-display">
                        <span class="rate-value">{data['rate']:,.4f}</span>
                        <span class="converted">≈ {data['converted_amount']:,.0f} IDR</span>
                    </div>
                    <div class="change-info">
                        <span class="change-value">
                            {data['change']:+.4f} ({data['change_percent']:+.2f}%)
                        </span>
                    </div>
                    <div class="click-indicator">
                        <span class="click-icon">👆</span>
                        <span class="click-text">Click for details</span>
                    </div>
                </div>
            '''
    else:
        content += '''
            <div class="empty-state">
                <div class="empty-icon">📈</div>
                <h3>No Rate History</h3>
                <p>Exchange rate data will appear here once available.</p>
            </div>
        '''
    
    content += '''
                </div>
            </div>
        </div>

        <!-- Rate Details Modal -->
        <div id="rateModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Exchange Rate Details</h2>
                    <span class="close" onclick="closeModal()">&times;</span>
                </div>
                <div class="modal-body">
                    <div class="rate-detail-grid">
                        <div class="detail-card">
                            <div class="detail-icon">🕐</div>
                            <div class="detail-info">
                                <h4>Timestamp</h4>
                                <p id="detail-timestamp">-</p>
                            </div>
                        </div>
                        <div class="detail-card">
                            <div class="detail-icon">💱</div>
                            <div class="detail-info">
                                <h4>Exchange Rate</h4>
                                <p id="detail-rate">-</p>
                            </div>
                        </div>
                        <div class="detail-card">
                            <div class="detail-icon">💰</div>
                            <div class="detail-info">
                                <h4>Conversion</h4>
                                <p id="detail-conversion">-</p>
                            </div>
                        </div>
                        <div class="detail-card">
                            <div class="detail-icon" id="detail-trend-icon">📈</div>
                            <div class="detail-info">
                                <h4>Change</h4>
                                <p id="detail-change">-</p>
                            </div>
                        </div>
                    </div>
                    <div class="additional-info">
                        <div class="info-section">
                            <h4>📊 Rate Analysis</h4>
                            <p id="rate-analysis">-</p>
                        </div>
                        <div class="info-section">
                            <h4>💡 Market Insights</h4>
                            <p id="market-insights">-</p>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="modal-btn" onclick="closeModal()">Close</button>
                </div>
            </div>
        </div>
    </div>

    <style>
        .history-container {
            max-width: 1200px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: rgba(15, 52, 96, 0.4);
            padding: 25px;
            border-radius: 15px;
            border-left: 4px solid #e94560;
            display: flex;
            align-items: center;
            gap: 20px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-icon {
            font-size: 2.5rem;
            opacity: 0.8;
        }

        .stat-info h3 {
            color: #e94560;
            font-size: 2rem;
            margin: 0;
            font-weight: bold;
        }

        .stat-info p {
            color: #ccc;
            margin: 5px 0 0 0;
            font-size: 0.9rem;
        }

        .tab-container {
            background: rgba(15, 52, 96, 0.3);
            border-radius: 15px;
            overflow: hidden;
            border-left: 4px solid #e94560;
        }

        .tab-buttons {
            display: flex;
            background: rgba(15, 52, 96, 0.5);
            border-bottom: 1px solid rgba(233, 69, 96, 0.2);
        }

        .tab-btn {
            flex: 1;
            padding: 20px;
            border: none;
            background: transparent;
            color: #ccc;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 16px;
        }

        .tab-btn:hover {
            background: rgba(233, 69, 96, 0.1);
            color: white;
        }

        .tab-btn.active {
            background: rgba(233, 69, 96, 0.2);
            color: #e94560;
            border-bottom: 3px solid #e94560;
        }

        .tab-icon {
            font-size: 1.2rem;
        }

        .tab-content {
            display: none;
            padding: 30px;
        }

        .tab-content.active {
            display: block;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .section-header h3 {
            color: #e94560;
            font-size: 1.5rem;
            margin: 0;
        }

        .rate-info-small {
            color: #ccc;
            font-size: 0.9rem;
        }

        .clear-btn {
            background: linear-gradient(135deg, #e94560, #c73650);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .clear-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(233, 69, 96, 0.3);
        }

        .history-list {
            max-height: 600px;
            overflow-y: auto;
            padding-right: 10px;
        }

        .history-item {
            background: rgba(22, 33, 62, 0.5);
            margin-bottom: 15px;
            padding: 20px;
            border-radius: 12px;
            border-left: 3px solid #e94560;
            transition: all 0.3s ease;
        }

        .history-item:hover {
            background: rgba(22, 33, 62, 0.7);
            transform: translateX(5px);
        }

        .history-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .conversion-info {
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .amount, .result {
            font-weight: bold;
            font-size: 1.1rem;
        }

        .amount {
            color: #4CAF50;
        }

        .result {
            color: #e94560;
        }

        .arrow {
            color: #ccc;
            font-size: 1.2rem;
        }

        .rate-info {
            color: #ccc;
            font-size: 0.9rem;
        }

        .history-meta {
            color: #888;
            font-size: 0.8rem;
        }

        .hourly-chart {
            max-height: 600px;
            overflow-y: auto;
            padding-right: 10px;
        }

        .hourly-item {
            background: rgba(22, 33, 62, 0.5);
            margin-bottom: 12px;
            padding: 20px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
            flex-wrap: wrap;
            gap: 15px;
            cursor: pointer;
            position: relative;
        }

        .hourly-item:hover {
            background: rgba(22, 33, 62, 0.7);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(233, 69, 96, 0.2);
        }

        .trend-up {
            border-left: 3px solid #4CAF50;
        }

        .trend-down {
            border-left: 3px solid #f44336;
        }

        .trend-stable {
            border-left: 3px solid #ccc;
        }

        .time-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .time {
            font-weight: bold;
            color: #e94560;
        }

        .trend-icon {
            font-size: 1.2rem;
        }

        .rate-display {
            text-align: center;
        }

        .rate-value {
            display: block;
            font-weight: bold;
            font-size: 1.1rem;
            color: white;
        }

        .converted {
            display: block;
            font-size: 0.9rem;
            color: #ccc;
            margin-top: 5px;
        }

        .change-info {
            text-align: right;
        }

        .change-value {
            font-weight: bold;
            font-size: 0.9rem;
        }

        .trend-up .change-value {
            color: #4CAF50;
        }

        .trend-down .change-value {
            color: #f44336;
        }

        .trend-stable .change-value {
            color: #ccc;
        }

        .click-indicator {
            position: absolute;
            top: 5px;
            right: 10px;
            display: flex;
            align-items: center;
            gap: 5px;
            opacity: 0.7;
            font-size: 0.8rem;
            color: #ccc;
        }

        .click-icon {
            font-size: 1rem;
        }

        .click-text {
            font-size: 0.75rem;
        }

        .hourly-item:hover .click-indicator {
            opacity: 1;
            color: #e94560;
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
        }

        .modal-content {
            background: linear-gradient(135deg, rgba(15, 52, 96, 0.9), rgba(22, 33, 62, 0.9));
            margin: 5% auto;
            padding: 0;
            border-radius: 20px;
            width: 90%;
            max-width: 700px;
            border: 1px solid rgba(233, 69, 96, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            animation: modalSlideIn 0.3s ease-out;
        }

        @keyframes modalSlideIn {
            from {
                opacity: 0;
                transform: translateY(-50px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .modal-header {
            background: rgba(233, 69, 96, 0.1);
            padding: 25px 30px;
            border-bottom: 1px solid rgba(233, 69, 96, 0.2);
            border-radius: 20px 20px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h2 {
            color: #e94560;
            margin: 0;
            font-size: 1.5rem;
        }

        .close {
            color: #ccc;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s ease;
        }

        .close:hover {
            color: #e94560;
        }

        .modal-body {
            padding: 30px;
        }

        .rate-detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .detail-card {
            background: rgba(22, 33, 62, 0.6);
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #e94560;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: transform 0.3s ease;
        }

        .detail-card:hover {
            transform: translateY(-3px);
        }

        .detail-icon {
            font-size: 2rem;
            opacity: 0.8;
        }

        .detail-info h4 {
            color: #e94560;
            margin: 0 0 5px 0;
            font-size: 1rem;
        }

        .detail-info p {
            color: white;
            margin: 0;
            font-weight: bold;
            font-size: 1.1rem;
        }

        .additional-info {
            margin-top: 30px;
        }

        .info-section {
            background: rgba(22, 33, 62, 0.4);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 3px solid #e94560;
        }

        .info-section h4 {
            color: #e94560;
            margin: 0 0 10px 0;
            font-size: 1.1rem;
        }

        .info-section p {
            color: #ccc;
            margin: 0;
            line-height: 1.6;
        }

        .modal-footer {
            background: rgba(15, 52, 96, 0.5);
            padding: 20px 30px;
            border-top: 1px solid rgba(233, 69, 96, 0.2);
            border-radius: 0 0 20px 20px;
            text-align: center;
        }

        .modal-btn {
            background: linear-gradient(135deg, #e94560, #c73650);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        .modal-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(233, 69, 96, 0.3);
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #ccc;
        }

        .empty-icon {
            font-size: 4rem;
            opacity: 0.5;
            margin-bottom: 20px;
        }

        .empty-state h3 {
            color: #e94560;
            margin-bottom: 10px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }

            .stat-card {
                padding: 20px;
            }

            .tab-btn {
                padding: 15px 10px;
                font-size: 14px;
            }

            .tab-content {
                padding: 20px;
            }

            .section-header {
                flex-direction: column;
                align-items: flex-start;
            }

            .history-main {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }

            .conversion-info {
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }

            .hourly-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
                padding: 15px;
            }

            .rate-display, .change-info {
                text-align: left;
            }

            .click-indicator {
                position: static;
                margin-top: 10px;
                justify-content: center;
            }

            .modal-content {
                width: 95%;
                margin: 10% auto;
            }

            .rate-detail-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Custom Scrollbar */
        .history-list::-webkit-scrollbar,
        .hourly-chart::-webkit-scrollbar {
            width: 8px;
        }

        .history-list::-webkit-scrollbar-track,
        .hourly-chart::-webkit-scrollbar-track {
            background: rgba(15, 52, 96, 0.3);
            border-radius: 4px;
        }

        .history-list::-webkit-scrollbar-thumb,
        .hourly-chart::-webkit-scrollbar-thumb {
            background: #e94560;
            border-radius: 4px;
        }

        .history-list::-webkit-scrollbar-thumb:hover,
        .hourly-chart::-webkit-scrollbar-thumb:hover {
            background: #c73650;
        }
    </style>

    <script>
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all buttons
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked button
            event.target.classList.add('active');
        }

        function clearHistory() {
            if (confirm('Are you sure you want to clear all conversion history? This action cannot be undone.')) {
                fetch('/clear-history', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            location.reload();
                        } else {
                            alert('Failed to clear history. Please try again.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while clearing history.');
                    });
            }
        }

        function showRateDetails(index, timestamp, rate, convertedAmount, change, changePercent, trend, fromCurrency, toCurrency, amount) {
            // Format timestamp for display
            let formattedTimestamp;
            try {
                const date = new Date(timestamp);
                formattedTimestamp = date.toLocaleString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            } catch (e) {
                formattedTimestamp = timestamp;
            }

            // Update modal content
            document.getElementById('detail-timestamp').textContent = formattedTimestamp;
            document.getElementById('detail-rate').textContent = `1 ${fromCurrency} = ${rate.toFixed(6)} ${toCurrency}`;
            document.getElementById('detail-conversion').textContent = `${amount} ${fromCurrency} = ${convertedAmount.toFixed(2)} ${toCurrency}`;
            
            // Update change information with color
            const changeElement = document.getElementById('detail-change');
            const trendIcon = document.getElementById('detail-trend-icon');
            
            if (trend === 'up') {
                changeElement.innerHTML = `<span style="color: #4CAF50;">+${change.toFixed(6)} (+${changePercent.toFixed(2)}%)</span>`;
                trendIcon.textContent = '📈';
            } else if (trend === 'down') {
                changeElement.innerHTML = `<span style="color: #f44336;">${change.toFixed(6)} (${changePercent.toFixed(2)}%)</span>`;
                trendIcon.textContent = '📉';
            } else {
                changeElement.innerHTML = `<span style="color: #ccc;">No change (0.00%)</span>`;
                trendIcon.textContent = '➡️';
            }

            // Generate rate analysis
            const rateAnalysis = generateRateAnalysis(rate, change, changePercent, trend);
            document.getElementById('rate-analysis').textContent = rateAnalysis;

            // Generate market insights
            const marketInsights = generateMarketInsights(fromCurrency, toCurrency, trend, changePercent);
            document.getElementById('market-insights').textContent = marketInsights;

            // Show modal
            document.getElementById('rateModal').style.display = 'block';
        }

        function closeModal() {
            document.getElementById('rateModal').style.display = 'none';
        }

        function generateRateAnalysis(rate, change, changePercent, trend) {
            if (trend === 'up') {
                if (Math.abs(changePercent) > 2) {
                    return `Strong upward movement detected. The exchange rate has increased significantly by ${Math.abs(changePercent).toFixed(2)}%, indicating positive market momentum.`;
                } else if (Math.abs(changePercent) > 0.5) {
                    return `Moderate upward trend observed. The rate shows steady growth of ${Math.abs(changePercent).toFixed(2)}%, suggesting stable market conditions.`;
                } else {
                    return `Slight upward movement. The rate has increased marginally by ${Math.abs(changePercent).toFixed(2)}%, indicating minor market fluctuations.`;
                }
            } else if (trend === 'down') {
                if (Math.abs(changePercent) > 2) {
                    return `Significant downward movement detected. The exchange rate has decreased by ${Math.abs(changePercent).toFixed(2)}%, suggesting market volatility or negative sentiment.`;
                } else if (Math.abs(changePercent) > 0.5) {
                    return `Moderate downward trend observed. The rate shows a decline of ${Math.abs(changePercent).toFixed(2)}%, indicating some market pressure.`;
                } else {
                    return `Slight downward movement. The rate has decreased marginally by ${Math.abs(changePercent).toFixed(2)}%, showing minor market adjustments.`;
                }
            } else {
                return `Stable exchange rate with no significant movement. This indicates a balanced market with minimal volatility during this period.`;
            }
        }

        function generateMarketInsights(fromCurrency, toCurrency, trend, changePercent) {
            const insights = [
                `Exchange rates between ${fromCurrency} and ${toCurrency} are influenced by various economic factors including interest rates, inflation, and political stability.`,
                `Currency fluctuations are normal and reflect the dynamic nature of global financial markets and economic conditions.`,
                `For international transactions, consider the timing of your exchanges to optimize value based on current market trends.`,
                `Historical rate data can help identify patterns, but past performance doesn't guarantee future movements.`,
                `Economic events, central bank policies, and geopolitical developments can significantly impact exchange rates.`
            ];

            // Add trend-specific insight
            if (Math.abs(changePercent) > 1) {
                if (trend === 'up') {
                    insights.unshift(`The current upward trend suggests ${fromCurrency} is strengthening against ${toCurrency}. This could be favorable for ${fromCurrency} holders looking to exchange.`);
                } else if (trend === 'down') {
                    insights.unshift(`The current downward trend indicates ${fromCurrency} is weakening against ${toCurrency}. Consider market timing for optimal exchange rates.`);
                }
            }

            // Return a random insight
            return insights[Math.floor(Math.random() * insights.length)];
        }

        // Close modal when clicking outside of it
        window.onclick = function(event) {
            const modal = document.getElementById('rateModal');
            if (event.target === modal) {
                closeModal();
            }
        }

        // Close modal with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        });
    </script>
    '''
    
    
    return content