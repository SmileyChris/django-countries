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
7. Save as a CSV file in django_countries/iso3166-1.csv
8. Run this script from the command line
"""
from __future__ import unicode_literals
import glob
import os

from django_countries.base import CountriesBase

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    def _(x):
        return x


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
    "BO": _("Bolivia (Plurinational State of)"),
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
    "CD": _("Congo (the Democratic Republic of the)"),
    "CG": _("Congo"),
    "CK": _("Cook Islands"),
    "CR": _("Costa Rica"),
    "CI": _("Côte d'Ivoire"),
    "HR": _("Croatia"),
    "CU": _("Cuba"),
    "CW": _("Curaçao"),
    "CY": _("Cyprus"),
    "CZ": _("Czechia"),
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
    "SZ": _("Eswatini"),
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
    "GM": _("Gambia"),
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
    "VA": _("Holy See"),
    "HN": _("Honduras"),
    "HK": _("Hong Kong"),
    "HU": _("Hungary"),
    "IS": _("Iceland"),
    "IN": _("India"),
    "ID": _("Indonesia"),
    "IR": _("Iran (Islamic Republic of)"),
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
    "KP": _("Korea (the Democratic People's Republic of)"),
    "KR": _("Korea (the Republic of)"),
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
    "MK": _("Macedonia (the former Yugoslav Republic of)"),
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
    "FM": _("Micronesia (Federated States of)"),
    "MD": _("Moldova (the Republic of)"),
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
    "PS": _("Palestine, State of"),
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
    "SE": _("Sweden"),
    "CH": _("Switzerland"),
    "SY": _("Syrian Arab Republic"),
    "TW": _("Taiwan (Province of China)"),
    "TJ": _("Tajikistan"),
    "TZ": _("Tanzania, United Republic of"),
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
    "GB": _("United Kingdom of Great Britain and Northern Ireland"),
    "UM": _("United States Minor Outlying Islands"),
    "US": _("United States of America"),
    "UY": _("Uruguay"),
    "UZ": _("Uzbekistan"),
    "VU": _("Vanuatu"),
    "VE": _("Venezuela (Bolivarian Republic of)"),
    "VN": _("Viet Nam"),
    "VG": _("Virgin Islands (British)"),
    "VI": _("Virgin Islands (U.S.)"),
    "WF": _("Wallis and Futuna"),
    "EH": _("Western Sahara"),
    "YE": _("Yemen"),
    "ZM": _("Zambia"),
    "ZW": _("Zimbabwe"),
}

ALT_CODES = {
    "AD": ("AND", 20, 376),
    "AE": ("ARE", 784, 971),
    "AF": ("AFG", 4, 93),
    "AG": ("ATG", 28, 1),
    "AI": ("AIA", 660, 1),
    "AL": ("ALB", 8, 355),
    "AM": ("ARM", 51, 374),
    "AO": ("AGO", 24, 244),
    "AQ": ("ATA", 10, 672),
    "AR": ("ARG", 32, 54),
    "AS": ("ASM", 16, 1),
    "AT": ("AUT", 40, 43),
    "AU": ("AUS", 36, 61),
    "AW": ("ABW", 533, 297),
    "AX": ("ALA", 248, 358),
    "AZ": ("AZE", 31, 994),
    "BA": ("BIH", 70, 387),
    "BB": ("BRB", 52, 1),
    "BD": ("BGD", 50, 880),
    "BE": ("BEL", 56, 32),
    "BF": ("BFA", 854, 226),
    "BG": ("BGR", 100, 359),
    "BH": ("BHR", 48, 973),
    "BI": ("BDI", 108, 257),
    "BJ": ("BEN", 204, 229),
    "BL": ("BLM", 652, 590),
    "BM": ("BMU", 60, 1),
    "BN": ("BRN", 96, 673),
    "BO": ("BOL", 68, 591),
    "BQ": ("BES", 535, 599),
    "BR": ("BRA", 76, 55),
    "BS": ("BHS", 44, 1),
    "BT": ("BTN", 64, 975),
    "BV": ("BVT", 74, 0),
    "BW": ("BWA", 72, 267),
    "BY": ("BLR", 112, 375),
    "BZ": ("BLZ", 84, 501),
    "CA": ("CAN", 124, 1),
    "CC": ("CCK", 166, 61),
    "CD": ("COD", 180, 243),
    "CF": ("CAF", 140, 236),
    "CG": ("COG", 178, 242),
    "CH": ("CHE", 756, 41),
    "CI": ("CIV", 384, 225),
    "CK": ("COK", 184, 682),
    "CL": ("CHL", 152, 56),
    "CM": ("CMR", 120, 237),
    "CN": ("CHN", 156, 86),
    "CO": ("COL", 170, 57),
    "CR": ("CRI", 188, 506),
    "CU": ("CUB", 192, 53),
    "CV": ("CPV", 132, 238),
    "CW": ("CUW", 531, 599),
    "CX": ("CXR", 162, 61),
    "CY": ("CYP", 196, 357),
    "CZ": ("CZE", 203, 420),
    "DE": ("DEU", 276, 49),
    "DJ": ("DJI", 262, 253),
    "DK": ("DNK", 208, 45),
    "DM": ("DMA", 212, 1),
    "DO": ("DOM", 214, 1),
    "DZ": ("DZA", 12, 213),
    "EC": ("ECU", 218, 593),
    "EE": ("EST", 233, 372),
    "EG": ("EGY", 818, 20),
    "EH": ("ESH", 732, 212),
    "ER": ("ERI", 232, 291),
    "ES": ("ESP", 724, 34),
    "ET": ("ETH", 231, 251),
    "FI": ("FIN", 246, 358),
    "FJ": ("FJI", 242, 679),
    "FK": ("FLK", 238, 500),
    "FM": ("FSM", 583, 691),
    "FO": ("FRO", 234, 298),
    "FR": ("FRA", 250, 33),
    "GA": ("GAB", 266, 241),
    "GB": ("GBR", 826, 44),
    "GD": ("GRD", 308, 1),
    "GE": ("GEO", 268, 995),
    "GF": ("GUF", 254, 594),
    "GG": ("GGY", 831, 44),
    "GH": ("GHA", 288, 233),
    "GI": ("GIB", 292, 350),
    "GL": ("GRL", 304, 299),
    "GM": ("GMB", 270, 220),
    "GN": ("GIN", 324, 224),
    "GP": ("GLP", 312, 590),
    "GQ": ("GNQ", 226, 240),
    "GR": ("GRC", 300, 30),
    "GS": ("SGS", 239, 500),
    "GT": ("GTM", 320, 502),
    "GU": ("GUM", 316, 1),
    "GW": ("GNB", 624, 245),
    "GY": ("GUY", 328, 592),
    "HK": ("HKG", 344, 852),
    "HM": ("HMD", 334, 0),
    "HN": ("HND", 340, 504),
    "HR": ("HRV", 191, 385),
    "HT": ("HTI", 332, 509),
    "HU": ("HUN", 348, 36),
    "ID": ("IDN", 360, 62),
    "IE": ("IRL", 372, 353),
    "IL": ("ISR", 376, 972),
    "IM": ("IMN", 833, 44),
    "IN": ("IND", 356, 91),
    "IO": ("IOT", 86, 246),
    "IQ": ("IRQ", 368, 964),
    "IR": ("IRN", 364, 98),
    "IS": ("ISL", 352, 354),
    "IT": ("ITA", 380, 39),
    "JE": ("JEY", 832, 44),
    "JM": ("JAM", 388, 1),
    "JO": ("JOR", 400, 962),
    "JP": ("JPN", 392, 81),
    "KE": ("KEN", 404, 254),
    "KG": ("KGZ", 417, 996),
    "KH": ("KHM", 116, 855),
    "KI": ("KIR", 296, 686),
    "KM": ("COM", 174, 269),
    "KN": ("KNA", 659, 1),
    "KP": ("PRK", 408, 850),
    "KR": ("KOR", 410, 82),
    "KW": ("KWT", 414, 965),
    "KY": ("CYM", 136, 1),
    "KZ": ("KAZ", 398, 7),
    "LA": ("LAO", 418, 856),
    "LB": ("LBN", 422, 961),
    "LC": ("LCA", 662, 1),
    "LI": ("LIE", 438, 423),
    "LK": ("LKA", 144, 94),
    "LR": ("LBR", 430, 231),
    "LS": ("LSO", 426, 266),
    "LT": ("LTU", 440, 370),
    "LU": ("LUX", 442, 352),
    "LV": ("LVA", 428, 371),
    "LY": ("LBY", 434, 218),
    "MA": ("MAR", 504, 212),
    "MC": ("MCO", 492, 377),
    "MD": ("MDA", 498, 373),
    "ME": ("MNE", 499, 382),
    "MF": ("MAF", 663, 590),
    "MG": ("MDG", 450, 261),
    "MH": ("MHL", 584, 692),
    "MK": ("MKD", 807, 389),
    "ML": ("MLI", 466, 223),
    "MM": ("MMR", 104, 95),
    "MN": ("MNG", 496, 976),
    "MO": ("MAC", 446, 853),
    "MP": ("MNP", 580, 1),
    "MQ": ("MTQ", 474, 596),
    "MR": ("MRT", 478, 222),
    "MS": ("MSR", 500, 1),
    "MT": ("MLT", 470, 356),
    "MU": ("MUS", 480, 230),
    "MV": ("MDV", 462, 960),
    "MW": ("MWI", 454, 265),
    "MX": ("MEX", 484, 52),
    "MY": ("MYS", 458, 60),
    "MZ": ("MOZ", 508, 258),
    "NA": ("NAM", 516, 264),
    "NC": ("NCL", 540, 687),
    "NE": ("NER", 562, 227),
    "NF": ("NFK", 574, 672),
    "NG": ("NGA", 566, 234),
    "NI": ("NIC", 558, 505),
    "NL": ("NLD", 528, 31),
    "NO": ("NOR", 578, 47),
    "NP": ("NPL", 524, 977),
    "NR": ("NRU", 520, 674),
    "NU": ("NIU", 570, 683),
    "NZ": ("NZL", 554, 64),
    "OM": ("OMN", 512, 968),
    "PA": ("PAN", 591, 507),
    "PE": ("PER", 604, 51),
    "PF": ("PYF", 258, 689),
    "PG": ("PNG", 598, 675),
    "PH": ("PHL", 608, 63),
    "PK": ("PAK", 586, 92),
    "PL": ("POL", 616, 48),
    "PM": ("SPM", 666, 508),
    "PN": ("PCN", 612, 64),
    "PR": ("PRI", 630, 1),
    "PS": ("PSE", 275, 970),
    "PT": ("PRT", 620, 351),
    "PW": ("PLW", 585, 680),
    "PY": ("PRY", 600, 595),
    "QA": ("QAT", 634, 974),
    "RE": ("REU", 638, 262),
    "RO": ("ROU", 642, 40),
    "RS": ("SRB", 688, 381),
    "RU": ("RUS", 643, 7),
    "RW": ("RWA", 646, 250),
    "SA": ("SAU", 682, 966),
    "SB": ("SLB", 90, 677),
    "SC": ("SYC", 690, 248),
    "SD": ("SDN", 729, 249),
    "SE": ("SWE", 752, 46),
    "SG": ("SGP", 702, 65),
    "SH": ("SHN", 654, 290),
    "SI": ("SVN", 705, 386),
    "SJ": ("SJM", 744, 47),
    "SK": ("SVK", 703, 421),
    "SL": ("SLE", 694, 232),
    "SM": ("SMR", 674, 378),
    "SN": ("SEN", 686, 221),
    "SO": ("SOM", 706, 252),
    "SR": ("SUR", 740, 597),
    "SS": ("SSD", 728, 211),
    "ST": ("STP", 678, 239),
    "SV": ("SLV", 222, 503),
    "SX": ("SXM", 534, 1),
    "SY": ("SYR", 760, 963),
    "SZ": ("SWZ", 748, 268),
    "TC": ("TCA", 796, 1),
    "TD": ("TCD", 148, 235),
    "TF": ("ATF", 260, 0),
    "TG": ("TGO", 768, 228),
    "TH": ("THA", 764, 66),
    "TJ": ("TJK", 762, 992),
    "TK": ("TKL", 772, 690),
    "TL": ("TLS", 626, 670),
    "TM": ("TKM", 795, 993),
    "TN": ("TUN", 788, 216),
    "TO": ("TON", 776, 676),
    "TR": ("TUR", 792, 90),
    "TT": ("TTO", 780, 1),
    "TV": ("TUV", 798, 688),
    "TW": ("TWN", 158, 886),
    "TZ": ("TZA", 834, 255),
    "UA": ("UKR", 804, 380),
    "UG": ("UGA", 800, 256),
    "UM": ("UMI", 581, 1),
    "US": ("USA", 840, 1),
    "UY": ("URY", 858, 598),
    "UZ": ("UZB", 860, 998),
    "VA": ("VAT", 336, 379),
    "VC": ("VCT", 670, 1),
    "VE": ("VEN", 862, 58),
    "VG": ("VGB", 92, 1),
    "VI": ("VIR", 850, 1),
    "VN": ("VNM", 704, 84),
    "VU": ("VUT", 548, 678),
    "WF": ("WLF", 876, 681),
    "WS": ("WSM", 882, 685),
    "YE": ("YEM", 887, 967),
    "YT": ("MYT", 175, 262),
    "ZA": ("ZAF", 710, 27),
    "ZM": ("ZMB", 894, 260),
    "ZW": ("ZWE", 716, 263),
}


def self_generate(output_filename, filename="iso3166-1.csv"):  # pragma: no cover
    """
    The following code can be used for self-generation of this file.

    It requires a UTF-8 CSV file containing the short ISO name and two letter
    country code as the first two columns.
    """
    import csv
    import re

    countries = []
    alt_codes = []
    with open(filename, "r") as csv_file:
        for row in csv.reader(csv_file):
            name = row[0].rstrip("*")
            name = re.sub(r"\(the\)", "", name)
            if name:
                countries.append((name, row[1]))
                alt_codes.append((row[1], row[2], int(row[3])))
    with open(__file__, "r") as source_file:
        contents = source_file.read()
    # Write countries.
    bits = re.match("(.*\nCOUNTRIES = \{\n)(.*?)(\n\}.*)", contents, re.DOTALL).groups()
    country_list = []
    for name, code in countries:
        name = name.replace('"', r"\"").strip()
        country_list.append('    "{code}": _("{name}"),'.format(name=name, code=code))
    content = bits[0]
    content += "\n".join(country_list)
    # Write alt codes.
    alt_bits = re.match(
        "(.*\nALT_CODES = \{\n)(.*)(\n\}.*)", bits[2], re.DOTALL
    ).groups()
    alt_list = []
    for code, code3, codenum in alt_codes:
        name = name.replace('"', r"\"").strip()
        alt_list.append(
            '    "{code}": ("{code3}", {codenum}),'.format(
                code=code, code3=code3, codenum=codenum
            )
        )
    content += alt_bits[0]
    content += "\n".join(alt_list)
    content += alt_bits[2]
    # Generate file.
    with open(output_filename, "w") as output_file:
        output_file.write(content)
    return countries


def check_flags(verbosity=1):
    files = {}
    this_dir = os.path.dirname(__file__)
    for path in glob.glob(os.path.join(this_dir, "static", "flags", "*.gif")):
        files[os.path.basename(os.path.splitext(path)[0]).upper()] = path

    flags_missing = set(COUNTRIES) - set(files)
    if flags_missing:  # pragma: no cover
        print("The following country codes are missing a flag:")
        for code in sorted(flags_missing):
            print("  {0} ({1})".format(code, COUNTRIES[code]))
    elif verbosity:  # pragma: no cover
        print("All country codes have flags. :)")

    code_missing = set(files) - set(COUNTRIES)
    # Special-case EU and __
    for special_code in ("EU", "__"):
        code_missing.discard(special_code)
    if code_missing:  # pragma: no cover
        print("")
        print("The following flags don't have a matching country code:")
        for path in sorted(code_missing):
            print("  {0}".format(path))


def check_common_names():
    common_names_missing = set(CountriesBase.COMMON_NAMES) - set(COUNTRIES)
    if common_names_missing:  # pragma: no cover
        print("")
        print("The following common names do not match an official country code:")
        for code in sorted(common_names_missing):
            print("  {0}".format(code))


if __name__ == "__main__":  # pragma: no cover
    countries = self_generate(__file__)
    print("Wrote {0} countries.".format(len(countries)))

    print("")
    check_flags()
    check_common_names()
