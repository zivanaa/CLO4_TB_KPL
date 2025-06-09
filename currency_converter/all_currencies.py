from config import SUPPORTED_CURRENCIES
import requests

def get_currency_flags():
    """Map currency codes to their country flag emojis"""
    flags = {
        'USD': '🇺🇸', 'EUR': '🇪🇺', 'GBP': '🇬🇧', 'JPY': '🇯🇵', 'AUD': '🇦🇺',
        'CAD': '🇨🇦', 'CHF': '🇨🇭', 'CNY': '🇨🇳', 'SEK': '🇸🇪', 'NZD': '🇳🇿',
        'MXN': '🇲🇽', 'SGD': '🇸🇬', 'HKD': '🇭🇰', 'NOK': '🇳🇴', 'KRW': '🇰🇷',
        'TRY': '🇹🇷', 'RUB': '🇷🇺', 'INR': '🇮🇳', 'BRL': '🇧🇷', 'ZAR': '🇿🇦',
        'PLN': '🇵🇱', 'CZK': '🇨🇿', 'HUF': '🇭🇺', 'RON': '🇷🇴', 'BGN': '🇧🇬',
        'HRK': '🇭🇷', 'ISK': '🇮🇸', 'DKK': '🇩🇰', 'THB': '🇹🇭', 'MYR': '🇲🇾',
        'IDR': '🇮🇩', 'PHP': '🇵🇭', 'VND': '🇻🇳', 'AED': '🇦🇪', 'SAR': '🇸🇦',
        'QAR': '🇶🇦', 'KWD': '🇰🇼', 'BHD': '🇧🇭', 'OMR': '🇴🇲', 'JOD': '🇯🇴',
        'LBP': '🇱🇧', 'EGP': '🇪🇬', 'ILS': '🇮🇱', 'PKR': '🇵🇰', 'LKR': '🇱🇰',
        'NPR': '🇳🇵', 'BDT': '🇧🇩', 'MMK': '🇲🇲', 'LAK': '🇱🇦', 'KHR': '🇰🇭',
        'TWD': '🇹🇼', 'MOP': '🇲🇴', 'BND': '🇧🇳', 'FJD': '🇫🇯', 'PGK': '🇵🇬',
        'WST': '🇼🇸', 'TOP': '🇹🇴', 'VUV': '🇻🇺', 'SBD': '🇸🇧', 'NCF': '🇳🇨',
        'XPF': '🇵🇫', 'ARS': '🇦🇷', 'BOB': '🇧🇴', 'CLP': '🇨🇱', 'COP': '🇨🇴',
        'PEN': '🇵🇪', 'UYU': '🇺🇾', 'PYG': '🇵🇾', 'VES': '🇻🇪', 'GYD': '🇬🇾',
        'SRD': '🇸🇷', 'TTD': '🇹🇹', 'JMD': '🇯🇲', 'BBD': '🇧🇧', 'XCD': '⿬',
        'BSD': '🇧🇸', 'BZD': '🇧🇿', 'GTQ': '🇬🇹', 'HNL': '🇭🇳', 'NIO': '🇳🇮',
        'CRC': '🇨🇷', 'PAB': '🇵🇦', 'DOP': '🇩🇴', 'HTG': '🇭🇹', 'CUP': '🇨🇺',
        'AWG': '🇦🇼', 'ANG': '🇳🇱', 'SVC': '🇸🇻', 'DZD': '🇩🇿', 'MAD': '🇲🇦',
        'TND': '🇹🇳', 'LYD': '🇱🇾', 'SDG': '🇸🇩', 'ETB': '🇪🇹', 'KES': '🇰🇪',
        'UGX': '🇺🇬', 'TZS': '🇹🇿', 'RWF': '🇷🇼', 'BIF': '🇧🇮', 'DJF': '🇩🇯',
        'SOS': '🇸🇴', 'ERN': '🇪🇷', 'MRU': '🇲🇷', 'GMD': '🇬🇲', 'GNF': '🇬🇳',
        'SLE': '🇸🇱', 'LRD': '🇱🇷', 'GHS': '🇬🇭', 'NGN': '🇳🇬', 'XOF': '⿬',
        'XAF': '⿬', 'CVE': '🇨🇻', 'STN': '🇸🇹', 'AOA': '🇦🇴', 'ZMW': '🇿🇲',
        'MZN': '🇲🇿', 'MWK': '🇲🇼', 'SZL': '🇸🇿', 'LSL': '🇱🇸', 'BWP': '🇧🇼',
        'NAD': '🇳🇦', 'SCR': '🇸🇨', 'MUR': '🇲🇺', 'KMF': '🇰🇲', 'MGA': '🇲🇬',
        'YER': '🇾🇪', 'IRR': '🇮🇷', 'AFN': '🇦🇫', 'UZS': '🇺🇿', 'KZT': '🇰🇿',
        'KGS': '🇰🇬', 'TJS': '🇹🇯', 'TMT': '🇹🇲', 'AZN': '🇦🇿', 'GEL': '🇬🇪',
        'AMD': '🇦🇲', 'MDL': '🇲🇩', 'UAH': '🇺🇦', 'BYN': '🇧🇾', 'LTL': '🇱🇹',
        'LVL': '🇱🇻', 'EEK': '🇪🇪', 'RSD': '🇷🇸', 'MKD': '🇲🇰', 'ALL': '🇦🇱',
        'BAM': '🇧🇦', 'EUR': '🇪🇺'
    }
    return flags

def group_currencies_by_region():
    """Group currencies by geographical regions"""
    regions = {
        'North America': ['USD', 'CAD', 'MXN', 'GTQ', 'BZD', 'HNL', 'SVC', 'NIO', 'CRC', 'PAB'],
        'Europe': ['EUR', 'GBP', 'CHF', 'SEK', 'NOK', 'DKK', 'PLN', 'CZK', 'HUF', 'RON', 'BGN', 'HRK', 'ISK', 'RSD', 'MKD', 'ALL', 'BAM'],
        'Asia': ['JPY', 'CNY', 'INR', 'KRW', 'SGD', 'HKD', 'THB', 'MYR', 'IDR', 'PHP', 'VND', 'TWD', 'PKR', 'LKR', 'NPR', 'BDT', 'MMK', 'LAK', 'KHR'],
        'Middle East': ['AED', 'SAR', 'QAR', 'KWD', 'BHD', 'OMR', 'JOD', 'LBP', 'ILS', 'YER', 'IRR'],
        'Africa': ['ZAR', 'EGP', 'NGN', 'KES', 'GHS', 'MAD', 'TND', 'DZD', 'ETB', 'UGX', 'TZS', 'ZMW', 'BWP', 'NAD'],
        'South America': ['BRL', 'ARS', 'CLP', 'COP', 'PEN', 'VES', 'UYU', 'BOB', 'PYG', 'GYD', 'SRD'],
        'Caribbean': ['XCD', 'JMD', 'TTD', 'BBD', 'BSD', 'DOP', 'HTG', 'CUP', 'AWG', 'ANG'],
        'Oceania': ['AUD', 'NZD', 'FJD', 'PGK', 'WST', 'TOP', 'VUV', 'SBD', 'XPF']
    }
    return regions

def get_popular_currencies():
    """Get list of most traded currencies"""
    return [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('JPY', 'Japanese Yen'),
        ('GBP', 'British Pound'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CNY', 'Chinese Yuan'),
        ('SEK', 'Swedish Krona'),
        ('NZD', 'New Zealand Dollar')
    ]

def get_all_currencies_content():
    """Generate HTML content for all currencies page"""
    
    if not SUPPORTED_CURRENCIES:
        return """
        <div class="alert alert-warning" style="background: rgba(233, 69, 96, 0.1); border: 1px solid #e94560; color: white; padding: 20px; border-radius: 10px;">
            <h4 style="color: #e94560;">⚠ Unable to Load Currencies</h4>
            <p>Failed to fetch currency data from the API. Please check your internet connection and try again.</p>
        </div>
        """
  
    flags = get_currency_flags()
    regions = group_currencies_by_region()
    popular = get_popular_currencies()
    
