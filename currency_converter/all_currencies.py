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

    }
    return regions
