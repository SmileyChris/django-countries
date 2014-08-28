#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a self-generating script that contains all of the iso3166-1 data.

To regenerate, a CSV file must be created that contains the latest data. Here's
how to do that:

1. Visit https://www.iso.org/obp
2. Click the "Country Codes" radio option and click the search button
3. Filter by "Officially assigned codes"
4. Change the results per page to 300
5. Copy the html table and paste into Libreoffice Calc / Excel
6. Delete the French name column
7. Save as a CSV file in django_countires/iso3166-1.csv
8. Run this script from the command line
"""
from __future__ import unicode_literals
import glob
import os

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Allows this module to be executed without Django installed.
    _ = lambda x: x

# Nicely titled (and translatable) country names.
COUNTRIES = {
    "AF": _("Afghanistan"),
    "AX": _("Åland Islands"),
    "AL": _("Albania"),
    "DZ": _("Algeria"),
    "AS": _("American Samoa"),
    "AD": _("Andorra"),
    "AO": _("Angola"),
    "AI": _("Anguilla"),
    "AQ": _("Antarctica"),
    "AG": _("Antigua and Barbuda"),
    "AR": _("Argentina"),
    "AM": _("Armenia"),
    "AW": _("Aruba"),
    "AU": _("Australia"),
    "AT": _("Austria"),
    "AZ": _("Azerbaijan"),
    "BS": _("Bahamas"),
    "BH": _("Bahrain"),
    "BD": _("Bangladesh"),
    "BB": _("Barbados"),
    "BY": _("Belarus"),
    "BE": _("Belgium"),
    "BZ": _("Belize"),
    "BJ": _("Benin"),
    "BM": _("Bermuda"),
    "BT": _("Bhutan"),
    "BO": _("Bolivia"),
    "BQ": _("Bonaire, Sint Eustatius and Saba"),
    "BA": _("Bosnia and Herzegovina"),
    "BW": _("Botswana"),
    "BV": _("Bouvet Island"),
    "BR": _("Brazil"),
    "IO": _("British Indian Ocean Territory"),
    "BN": _("Brunei Darussalam"),
    "BG": _("Bulgaria"),
    "BF": _("Burkina Faso"),
    "BI": _("Burundi"),
    "CV": _("Cabo Verde"),
    "KH": _("Cambodia"),
    "CM": _("Cameroon"),
    "CA": _("Canada"),
    "KY": _("Cayman Islands"),
    "CF": _("Central African Republic"),
    "TD": _("Chad"),
    "CL": _("Chile"),
    "CN": _("China"),
    "CX": _("Christmas Island"),
    "CC": _("Cocos (Keeling) Islands"),
    "CO": _("Colombia"),
    "KM": _("Comoros"),
    "CG": _("Congo"),
    "CD": _("Congo"),
    "CK": _("Cook Islands"),
    "CR": _("Costa Rica"),
    "CI": _("Côte d'Ivoire"),
    "HR": _("Croatia"),
    "CU": _("Cuba"),
    "CW": _("Curaçao"),
    "CY": _("Cyprus"),
    "CZ": _("Czech Republic"),
    "DK": _("Denmark"),
    "DJ": _("Djibouti"),
    "DM": _("Dominica"),
    "DO": _("Dominican Republic"),
    "EC": _("Ecuador"),
    "EG": _("Egypt"),
    "SV": _("El Salvador"),
    "GQ": _("Equatorial Guinea"),
    "ER": _("Eritrea"),
    "EE": _("Estonia"),
    "ET": _("Ethiopia"),
    "FK": _("Falkland Islands  [Malvinas]"),
    "FO": _("Faroe Islands"),
    "FJ": _("Fiji"),
    "FI": _("Finland"),
    "FR": _("France"),
    "GF": _("French Guiana"),
    "PF": _("French Polynesia"),
    "TF": _("French Southern Territories"),
    "GA": _("Gabon"),
    "GM": _("Gambia (The)"),
    "GE": _("Georgia"),
    "DE": _("Germany"),
    "GH": _("Ghana"),
    "GI": _("Gibraltar"),
    "GR": _("Greece"),
    "GL": _("Greenland"),
    "GD": _("Grenada"),
    "GP": _("Guadeloupe"),
    "GU": _("Guam"),
    "GT": _("Guatemala"),
    "GG": _("Guernsey"),
    "GN": _("Guinea"),
    "GW": _("Guinea-Bissau"),
    "GY": _("Guyana"),
    "HT": _("Haiti"),
    "HM": _("Heard Island and McDonald Islands"),
    "VA": _("Holy See  [Vatican City State]"),
    "HN": _("Honduras"),
    "HK": _("Hong Kong"),
    "HU": _("Hungary"),
    "IS": _("Iceland"),
    "IN": _("India"),
    "ID": _("Indonesia"),
    "IR": _("Iran"),
    "IQ": _("Iraq"),
    "IE": _("Ireland"),
    "IM": _("Isle of Man"),
    "IL": _("Israel"),
    "IT": _("Italy"),
    "JM": _("Jamaica"),
    "JP": _("Japan"),
    "JE": _("Jersey"),
    "JO": _("Jordan"),
    "KZ": _("Kazakhstan"),
    "KE": _("Kenya"),
    "KI": _("Kiribati"),
    "KP": _("Korea"),
    "KR": _("Korea"),
    "KW": _("Kuwait"),
    "KG": _("Kyrgyzstan"),
    "LA": _("Lao People's Democratic Republic"),
    "LV": _("Latvia"),
    "LB": _("Lebanon"),
    "LS": _("Lesotho"),
    "LR": _("Liberia"),
    "LY": _("Libya"),
    "LI": _("Liechtenstein"),
    "LT": _("Lithuania"),
    "LU": _("Luxembourg"),
    "MO": _("Macao"),
    "MK": _("Macedonia"),
    "MG": _("Madagascar"),
    "MW": _("Malawi"),
    "MY": _("Malaysia"),
    "MV": _("Maldives"),
    "ML": _("Mali"),
    "MT": _("Malta"),
    "MH": _("Marshall Islands"),
    "MQ": _("Martinique"),
    "MR": _("Mauritania"),
    "MU": _("Mauritius"),
    "YT": _("Mayotte"),
    "MX": _("Mexico"),
    "FM": _("Micronesia"),
    "MD": _("Moldova"),
    "MC": _("Monaco"),
    "MN": _("Mongolia"),
    "ME": _("Montenegro"),
    "MS": _("Montserrat"),
    "MA": _("Morocco"),
    "MZ": _("Mozambique"),
    "MM": _("Myanmar"),
    "NA": _("Namibia"),
    "NR": _("Nauru"),
    "NP": _("Nepal"),
    "NL": _("Netherlands"),
    "NC": _("New Caledonia"),
    "NZ": _("New Zealand"),
    "NI": _("Nicaragua"),
    "NE": _("Niger"),
    "NG": _("Nigeria"),
    "NU": _("Niue"),
    "NF": _("Norfolk Island"),
    "MP": _("Northern Mariana Islands"),
    "NO": _("Norway"),
    "OM": _("Oman"),
    "PK": _("Pakistan"),
    "PW": _("Palau"),
    "PS": _("Palestine"),
    "PA": _("Panama"),
    "PG": _("Papua New Guinea"),
    "PY": _("Paraguay"),
    "PE": _("Peru"),
    "PH": _("Philippines"),
    "PN": _("Pitcairn"),
    "PL": _("Poland"),
    "PT": _("Portugal"),
    "PR": _("Puerto Rico"),
    "QA": _("Qatar"),
    "RE": _("Réunion"),
    "RO": _("Romania"),
    "RU": _("Russian Federation"),
    "RW": _("Rwanda"),
    "BL": _("Saint Barthélemy"),
    "SH": _("Saint Helena, Ascension and Tristan da Cunha"),
    "KN": _("Saint Kitts and Nevis"),
    "LC": _("Saint Lucia"),
    "MF": _("Saint Martin (French part)"),
    "PM": _("Saint Pierre and Miquelon"),
    "VC": _("Saint Vincent and the Grenadines"),
    "WS": _("Samoa"),
    "SM": _("San Marino"),
    "ST": _("Sao Tome and Principe"),
    "SA": _("Saudi Arabia"),
    "SN": _("Senegal"),
    "RS": _("Serbia"),
    "SC": _("Seychelles"),
    "SL": _("Sierra Leone"),
    "SG": _("Singapore"),
    "SX": _("Sint Maarten (Dutch part)"),
    "SK": _("Slovakia"),
    "SI": _("Slovenia"),
    "SB": _("Solomon Islands"),
    "SO": _("Somalia"),
    "ZA": _("South Africa"),
    "GS": _("South Georgia and the South Sandwich Islands"),
    "SS": _("South Sudan"),
    "ES": _("Spain"),
    "LK": _("Sri Lanka"),
    "SD": _("Sudan"),
    "SR": _("Suriname"),
    "SJ": _("Svalbard and Jan Mayen"),
    "SZ": _("Swaziland"),
    "SE": _("Sweden"),
    "CH": _("Switzerland"),
    "SY": _("Syrian Arab Republic"),
    "TW": _("Taiwan"),
    "TJ": _("Tajikistan"),
    "TZ": _("Tanzania"),
    "TH": _("Thailand"),
    "TL": _("Timor-Leste"),
    "TG": _("Togo"),
    "TK": _("Tokelau"),
    "TO": _("Tonga"),
    "TT": _("Trinidad and Tobago"),
    "TN": _("Tunisia"),
    "TR": _("Turkey"),
    "TM": _("Turkmenistan"),
    "TC": _("Turks and Caicos Islands"),
    "TV": _("Tuvalu"),
    "UG": _("Uganda"),
    "UA": _("Ukraine"),
    "AE": _("United Arab Emirates"),
    "GB": _("United Kingdom"),
    "US": _("United States"),
    "UM": _("United States Minor Outlying Islands"),
    "UY": _("Uruguay"),
    "UZ": _("Uzbekistan"),
    "VU": _("Vanuatu"),
    "VE": _("Venezuela"),
    "VN": _("Viet Nam"),
    "VG": _("Virgin Islands (British)"),
    "VI": _("Virgin Islands (U.S.)"),
    "WF": _("Wallis and Futuna"),
    "EH": _("Western Sahara"),
    "YE": _("Yemen"),
    "ZM": _("Zambia"),
    "ZW": _("Zimbabwe"),
}

FULL_COUNTRIES = {
    "BO": _("Bolivia, Plurinational State of"),
    "CD": _("Congo (the Democratic Republic of the)"),
    "IR": _("Iran (the Islamic Republic of)"),
    "KP": _("Korea (the Democratic People's Republic of)"),
    "KR": _("Korea (the Republic of)"),
    "MK": _("Macedonia (the former Yugoslav Republic of)"),
    "FM": _("Micronesia (the Federated States of)"),
    "MD": _("Moldova (the Republic of)"),
    "PS": _("Palestine, State of"),
    "TW": _("Taiwan (Province of China)"),
    "TZ": _("Tanzania, United Republic of"),
    "VE": _("Venezuela, Bolivarian Republic of"),
}


def self_generate(
        output_filename, filename='iso3166-1.csv'):  # pragma: no cover
    """
    The following code can be used for self-generation of this file.

    It requires a UTF-8 CSV file containing the short ISO name and two letter
    country code as the first two columns.
    """
    import csv
    import re
    countries = []
    full_countries = []
    with open(filename, 'rb') as csv_file:
        for row in csv.reader(csv_file):
            name = row[0].decode('utf-8').rstrip('*')
            name = re.sub(r'\(the\)', '', name)
            truncated = re.sub(r'[(,].*\bof\b.*$', '', name)
            if truncated:
                countries.append((truncated, row[1].decode('utf-8')))
                if truncated != name:
                    full_countries.append((name, row[1].decode('utf-8')))
    with open(__file__, 'r') as source_file:
        contents = source_file.read()
    bits = re.match(
        '(.*\nCOUNTRIES = \{\n)(.*)(\n\}\n\nFULL_COUNTRIES = \{\n)(.*)(\n\}.*)', contents, re.DOTALL).groups()
    country_list = []
    full_country_list = []
    for name, code in countries:
        name = name.replace('"', r'\"').strip()
        country_list.append(
            '    "{code}": _("{name}"),'.format(name=name, code=code))
    for name, code in full_countries:
        name = name.replace('"', r'\"').strip()
        full_country_list.append(
            '    "{code}": _("{name}"),'.format(name=name, code=code))
    content = bits[0]
    content += '\n'.join(country_list).encode('utf-8')
    content += bits[2]
    content += '\n'.join(full_country_list).encode('utf-8')
    content += bits[4]
    with open(output_filename, 'wb') as output_file:
        output_file.write(content)
    return countries


def check_flags():
    files = {}
    this_dir = os.path.dirname(__file__)
    for path in glob.glob(os.path.join(this_dir, 'static', 'flags', '*.gif')):
        files[os.path.basename(os.path.splitext(path)[0]).upper()] = path

    flags_missing = set(COUNTRIES) - set(files)
    if flags_missing:  # pragma: no cover
        print("The following country codes are missing a flag:")
        for code in sorted(flags_missing):
            print("  {} ({})".format(code, COUNTRIES[code]))
    else:
        print("All country codes have flags. :)")

    code_missing = set(files) - set(COUNTRIES)
    # Special-case EU
    code_missing.discard('EU')
    if code_missing:  # pragma: no cover
        print("")
        print("The following flags don't have a matching country code:")
        for path in sorted(code_missing):
            print("  {}".format(path))


if __name__ == '__main__':
    countries = self_generate(__file__)
    print('Wrote {0} countries.'.format(len(countries)))

    # Check flag static files:
    print("")
    check_flags()
