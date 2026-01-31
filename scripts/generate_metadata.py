import yaml
import os
import re
import json
import datetime
import zoneinfo
from countryinfo import CountryInfo
from babel import Locale, numbers

# Advanced Economies (IMF 2024 list - simplified)
ADVANCED_ECONOMIES = {
    "AD", "AT", "AU", "BE", "CA", "CH", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GB", 
    "GR", "HK", "IE", "IL", "IS", "IT", "JP", "KR", "LI", "LT", "LU", "LV", "MC", "MT", "NL", 
    "NO", "NZ", "PT", "PR", "SG", "SK", "SI", "SM", "SE", "TW", "US"
}

# Date format mapping
DATE_FORMATS = {
    "US": "MM/DD/YYYY",
    "BZ": "MM/DD/YYYY",
    "FM": "MM/DD/YYYY",
    "MH": "MM/DD/YYYY",
    "PH": "MM/DD/YYYY",
    "CA": "YYYY-MM-DD",
    "JP": "YYYY/MM/DD",
    "CN": "YYYY/MM/DD",
    "KR": "YYYY/MM/DD",
    "TW": "YYYY/MM/DD",
    "HU": "YYYY/MM/DD",
    "LT": "YYYY-MM-DD",
}

def get_currency_info(currency_code):
    try:
        locale = Locale('en', 'US')
        name = locale.currencies.get(currency_code, currency_code)
        symbol = numbers.get_currency_symbol(currency_code, locale='en_US')
        return name, symbol
    except Exception:
        return None, None

def get_django_codes():
    codes = set()
    try:
        with open('django_countries/data.py', 'r') as f:
            content = f.read()
            matches = re.findall(r'"([A-Z]{2})": _\(', content)
            codes.update(matches)
    except Exception:
        pass
    return codes

def get_mledoze_data():
    mledoze_map = {}
    try:
        with open('countries_src.json', 'r') as f:
            data = json.load(f)
            for country in data:
                cca2 = country.get('cca2')
                if cca2:
                    mledoze_map[cca2] = country
    except Exception:
        pass
    return mledoze_map

def get_utc_offset_from_tz_name(tz_name):
    try:
        tz = zoneinfo.ZoneInfo(tz_name)
        now = datetime.datetime.now(tz)
        offset = now.strftime('%z')
        return offset[:3] + ':' + offset[3:]
    except Exception:
        return None

def generate_metadata():
    django_codes = get_django_codes()
    mledoze_data = get_mledoze_data()
    all_ci_data = CountryInfo().all()
    
    iso_to_ci = {}
    for name, data in all_ci_data.items():
        iso = data.get('ISO', {}).get('alpha2')
        if iso:
            iso_to_ci[iso] = data

    metadata = {}
    
    for iso_code in sorted(django_codes):
        info = iso_to_ci.get(iso_code)
        m_info = mledoze_data.get(iso_code, {})
        
        # Currency code
        curr_code = None
        m_currencies = m_info.get('currencies')
        if isinstance(m_currencies, dict) and m_currencies:
            curr_code = next(iter(m_currencies))
        elif isinstance(m_currencies, list) and m_currencies:
            curr_code = m_currencies[0]
        elif info and info.get('currencies'):
            curr_code = info.get('currencies')[0]
        
        curr_name, curr_symbol = None, None
        if curr_code and m_info:
            c_data = m_info.get('currencies', {})
            if isinstance(c_data, dict):
                 c_info = c_data.get(curr_code, {})
                 curr_name = c_info.get('name')
                 curr_symbol = c_info.get('symbol')
        
        if not curr_name and curr_code:
             curr_name, curr_symbol = get_currency_info(curr_code)

        # Calling code
        calling_code = None
        if m_info and m_info.get('idd'):
            idd = m_info.get('idd')
            if idd.get('root'):
                suffixes = idd.get('suffixes', [])
                # If many suffixes, it's likely area codes (like US/CA), just take root
                suffix = suffixes[0] if len(suffixes) == 1 else ''
                calling_code = idd.get('root') + suffix
        elif info and info.get('callingCodes'):
            calling_code = "+" + info.get('callingCodes')[0]

        # Capital
        capital = None
        if m_info and m_info.get('capital'):
            capital = m_info.get('capital')[0]
        elif info and info.get('capital'):
            capital = info.get('capital')

        # Continent
        continent = None
        if m_info and m_info.get('region'):
            continent = m_info.get('region')
        elif info and info.get('region'):
            continent = info.get('region')

        # Languages
        lang_names = []
        m_languages = m_info.get('languages')
        if m_languages:
            if isinstance(m_languages, dict):
                lang_names = list(m_languages.values())
            else:
                lang_names = m_languages
        elif info and info.get('languages'):
            languages = info.get('languages')
            for l in languages:
                try:
                    name = Locale('en').languages.get(l)
                    lang_names.append((name or l).capitalize())
                except Exception:
                    lang_names.append(l.capitalize())

        # Timezones
        timezones = []
        if m_info and m_info.get('timezones'):
            timezones = m_info.get('timezones')
        elif info and info.get('timezones'):
            timezones = info.get('timezones')

        timezones = [tz for tz in timezones if tz]

        metadata[iso_code] = {
            'currency_name': curr_name,
            'currency_symbol': curr_symbol,
            'calling_code': calling_code,
            'utc_offset': None,
            'capital_city': capital,
            'continent': continent,
            'date_format': DATE_FORMATS.get(iso_code, 'DD/MM/YYYY'),
            'official_language': lang_names,
            'timezones': timezones
        }
        
        # UTC Offset Logic
        offset_found = False
        if timezones:
            for tz in timezones:
                if '/' in tz:
                    offset = get_utc_offset_from_tz_name(tz)
                    if offset:
                        metadata[iso_code]['utc_offset'] = offset
                        offset_found = True
                        break
                
                if 'UTC' in tz:
                    offset = tz.replace('UTC', '').replace(' ', '')
                    offset = offset.replace('−', '-')
                    if not offset or offset == '±00:00':
                        offset = '+00:00'
                    elif len(offset) == 3 or (len(offset) == 2 and offset[0] in '+-'):
                        sign = offset[0]
                        val = offset[1:].zfill(2)
                        offset = f"{sign}{val}:00"
                    elif len(offset) == 5 and offset[0] in '+-' and ':' not in offset:
                        offset = offset[:3] + ':' + offset[3:]
                    
                    if re.match(r'^[+-]\d{2}:\d{2}$', offset):
                        metadata[iso_code]['utc_offset'] = offset
                        offset_found = True
                        break
        
        # Manual overrides for accuracy/consistency
        if iso_code == 'AD': metadata[iso_code]['utc_offset'] = '+01:00'
        if iso_code == 'GB': metadata[iso_code]['utc_offset'] = '+00:00'
        if iso_code == 'US': 
            metadata[iso_code]['utc_offset'] = '-05:00'
            metadata[iso_code]['capital_city'] = 'Washington, D.C.'
        if iso_code == 'NG':
            metadata[iso_code]['currency_name'] = 'Naira'

    sorted_metadata = {k: metadata[k] for k in sorted(metadata.keys())}
    
    with open('django_countries/data/country_metadata.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(sorted_metadata, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    generate_metadata()
