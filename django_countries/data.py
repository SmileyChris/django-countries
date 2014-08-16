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
from collections import namedtuple
import glob
import os

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Allows this module to be executed without Django installed.
    _ = lambda x: x

CountryTuple = namedtuple('CountryTuple', ['name', 'alpha2', 'alpha3', 'numeric',])

COUNTRIES_LIST = tuple(
    CountryTuple(*values)
    for values in (
        (_(u"Afghanistan"), 'AF', 'AFG', '004',),
        (_(u"Åland Islands"), 'AX', 'ALA', '248',),
        (_(u"Albania"), 'AL', 'ALB', '008',),
        (_(u"Algeria"), 'DZ', 'DZA', '012',),
        (_(u"American Samoa"), 'AS', 'ASM', '016',),
        (_(u"Andorra"), 'AD', 'AND', '020',),
        (_(u"Angola"), 'AO', 'AGO', '024',),
        (_(u"Anguilla"), 'AI', 'AIA', '660',),
        (_(u"Antarctica"), 'AQ', 'ATA', '010',),
        (_(u"Antigua and Barbuda"), 'AG', 'ATG', '028',),
        (_(u"Argentina"), 'AR', 'ARG', '032',),
        (_(u"Armenia"), 'AM', 'ARM', '051',),
        (_(u"Aruba"), 'AW', 'ABW', '533',),
        (_(u"Australia"), 'AU', 'AUS', '036',),
        (_(u"Austria"), 'AT', 'AUT', '040',),
        (_(u"Azerbaijan"), 'AZ', 'AZE', '031',),
        (_(u"Bahamas"), 'BS', 'BHS', '044',),
        (_(u"Bahrain"), 'BH', 'BHR', '048',),
        (_(u"Bangladesh"), 'BD', 'BGD', '050',),
        (_(u"Barbados"), 'BB', 'BRB', '052',),
        (_(u"Belarus"), 'BY', 'BLR', '112',),
        (_(u"Belgium"), 'BE', 'BEL', '056',),
        (_(u"Belize"), 'BZ', 'BLZ', '084',),
        (_(u"Benin"), 'BJ', 'BEN', '204',),
        (_(u"Bermuda"), 'BM', 'BMU', '060',),
        (_(u"Bhutan"), 'BT', 'BTN', '064',),
        (_(u"Bolivia, Plurinational State of"), 'BO', 'BOL', '068',),
        (_(u"Bonaire, Sint Eustatius and Saba"), 'BQ', 'BES', '535',),
        (_(u"Bosnia and Herzegovina"), 'BA', 'BIH', '070',),
        (_(u"Botswana"), 'BW', 'BWA', '072',),
        (_(u"Bouvet Island"), 'BV', 'BVT', '074',),
        (_(u"Brazil"), 'BR', 'BRA', '076',),
        (_(u"British Indian Ocean Territory"), 'IO', 'IOT', '086',),
        (_(u"Brunei Darussalam"), 'BN', 'BRN', '096',),
        (_(u"Bulgaria"), 'BG', 'BGR', '100',),
        (_(u"Burkina Faso"), 'BF', 'BFA', '854',),
        (_(u"Burundi"), 'BI', 'BDI', '108',),
        (_(u"Cambodia"), 'KH', 'KHM', '116',),
        (_(u"Cameroon"), 'CM', 'CMR', '120',),
        (_(u"Canada"), 'CA', 'CAN', '124',),
        (_(u"Cabo Verde"), 'CV', 'CPV', '132',),
        (_(u"Cayman Islands"), 'KY', 'CYM', '136',),
        (_(u"Central African Republic"), 'CF', 'CAF', '140',),
        (_(u"Chad"), 'TD', 'TCD', '148',),
        (_(u"Chile"), 'CL', 'CHL', '152',),
        (_(u"China"), 'CN', 'CHN', '156',),
        (_(u"Christmas Island"), 'CX', 'CXR', '162',),
        (_(u"Cocos (Keeling) Islands"), 'CC', 'CCK', '166',),
        (_(u"Colombia"), 'CO', 'COL', '170',),
        (_(u"Comoros"), 'KM', 'COM', '174',),
        (_(u"Congo"), 'CG', 'COG', '178',),
        (_(u"Congo, the Democratic Republic of the"), 'CD', 'COD', '180',),
        (_(u"Cook Islands"), 'CK', 'COK', '184',),
        (_(u"Costa Rica"), 'CR', 'CRI', '188',),
        (_(u"Côte d'Ivoire"), 'CI', 'CIV', '384',),
        (_(u"Croatia"), 'HR', 'HRV', '191',),
        (_(u"Cuba"), 'CU', 'CUB', '192',),
        (_(u"Curaçao"), 'CW', 'CUW', '531',),
        (_(u"Cyprus"), 'CY', 'CYP', '196',),
        (_(u"Czech Republic"), 'CZ', 'CZE', '203',),
        (_(u"Denmark"), 'DK', 'DNK', '208',),
        (_(u"Djibouti"), 'DJ', 'DJI', '262',),
        (_(u"Dominica"), 'DM', 'DMA', '212',),
        (_(u"Dominican Republic"), 'DO', 'DOM', '214',),
        (_(u"Ecuador"), 'EC', 'ECU', '218',),
        (_(u"Egypt"), 'EG', 'EGY', '818',),
        (_(u"El Salvador"), 'SV', 'SLV', '222',),
        (_(u"Equatorial Guinea"), 'GQ', 'GNQ', '226',),
        (_(u"Eritrea"), 'ER', 'ERI', '232',),
        (_(u"Estonia"), 'EE', 'EST', '233',),
        (_(u"Ethiopia"), 'ET', 'ETH', '231',),
        (_(u"Falkland Islands (Malvinas)"), 'FK', 'FLK', '238',),
        (_(u"Faroe Islands"), 'FO', 'FRO', '234',),
        (_(u"Fiji"), 'FJ', 'FJI', '242',),
        (_(u"Finland"), 'FI', 'FIN', '246',),
        (_(u"France"), 'FR', 'FRA', '250',),
        (_(u"French Guiana"), 'GF', 'GUF', '254',),
        (_(u"French Polynesia"), 'PF', 'PYF', '258',),
        (_(u"French Southern Territories"), 'TF', 'ATF', '260',),
        (_(u"Gabon"), 'GA', 'GAB', '266',),
        (_(u"Gambia"), 'GM', 'GMB', '270',),
        (_(u"Georgia"), 'GE', 'GEO', '268',),
        (_(u"Germany"), 'DE', 'DEU', '276',),
        (_(u"Ghana"), 'GH', 'GHA', '288',),
        (_(u"Gibraltar"), 'GI', 'GIB', '292',),
        (_(u"Greece"), 'GR', 'GRC', '300',),
        (_(u"Greenland"), 'GL', 'GRL', '304',),
        (_(u"Grenada"), 'GD', 'GRD', '308',),
        (_(u"Guadeloupe"), 'GP', 'GLP', '312',),
        (_(u"Guam"), 'GU', 'GUM', '316',),
        (_(u"Guatemala"), 'GT', 'GTM', '320',),
        (_(u"Guernsey"), 'GG', 'GGY', '831',),
        (_(u"Guinea"), 'GN', 'GIN', '324',),
        (_(u"Guinea-Bissau"), 'GW', 'GNB', '624',),
        (_(u"Guyana"), 'GY', 'GUY', '328',),
        (_(u"Haiti"), 'HT', 'HTI', '332',),
        (_(u"Heard Island and McDonald Islands"), 'HM', 'HMD', '334',),
        (_(u"Holy See (Vatican City State)"), 'VA', 'VAT', '336',),
        (_(u"Honduras"), 'HN', 'HND', '340',),
        (_(u"Hong Kong"), 'HK', 'HKG', '344',),
        (_(u"Hungary"), 'HU', 'HUN', '348',),
        (_(u"Iceland"), 'IS', 'ISL', '352',),
        (_(u"India"), 'IN', 'IND', '356',),
        (_(u"Indonesia"), 'ID', 'IDN', '360',),
        (_(u"Iran, Islamic Republic of"), 'IR', 'IRN', '364',),
        (_(u"Iraq"), 'IQ', 'IRQ', '368',),
        (_(u"Ireland"), 'IE', 'IRL', '372',),
        (_(u"Isle of Man"), 'IM', 'IMN', '833',),
        (_(u"Israel"), 'IL', 'ISR', '376',),
        (_(u"Italy"), 'IT', 'ITA', '380',),
        (_(u"Jamaica"), 'JM', 'JAM', '388',),
        (_(u"Japan"), 'JP', 'JPN', '392',),
        (_(u"Jersey"), 'JE', 'JEY', '832',),
        (_(u"Jordan"), 'JO', 'JOR', '400',),
        (_(u"Kazakhstan"), 'KZ', 'KAZ', '398',),
        (_(u"Kenya"), 'KE', 'KEN', '404',),
        (_(u"Kiribati"), 'KI', 'KIR', '296',),
        (_(u"Korea, Democratic People's Republic of"), 'KP', 'PRK', '408',),
        (_(u"Korea, Republic of"), 'KR', 'KOR', '410',),
        (_(u"Kuwait"), 'KW', 'KWT', '414',),
        (_(u"Kyrgyzstan"), 'KG', 'KGZ', '417',),
        (_(u"Lao People's Democratic Republic"), 'LA', 'LAO', '418',),
        (_(u"Latvia"), 'LV', 'LVA', '428',),
        (_(u"Lebanon"), 'LB', 'LBN', '422',),
        (_(u"Lesotho"), 'LS', 'LSO', '426',),
        (_(u"Liberia"), 'LR', 'LBR', '430',),
        (_(u"Libya"), 'LY', 'LBY', '434',),
        (_(u"Liechtenstein"), 'LI', 'LIE', '438',),
        (_(u"Lithuania"), 'LT', 'LTU', '440',),
        (_(u"Luxembourg"), 'LU', 'LUX', '442',),
        (_(u"Macao"), 'MO', 'MAC', '446',),
        (_(u"Macedonia, the former Yugoslav Republic of"), 'MK', 'MKD', '807',),
        (_(u"Madagascar"), 'MG', 'MDG', '450',),
        (_(u"Malawi"), 'MW', 'MWI', '454',),
        (_(u"Malaysia"), 'MY', 'MYS', '458',),
        (_(u"Maldives"), 'MV', 'MDV', '462',),
        (_(u"Mali"), 'ML', 'MLI', '466',),
        (_(u"Malta"), 'MT', 'MLT', '470',),
        (_(u"Marshall Islands"), 'MH', 'MHL', '584',),
        (_(u"Martinique"), 'MQ', 'MTQ', '474',),
        (_(u"Mauritania"), 'MR', 'MRT', '478',),
        (_(u"Mauritius"), 'MU', 'MUS', '480',),
        (_(u"Mayotte"), 'YT', 'MYT', '175',),
        (_(u"Mexico"), 'MX', 'MEX', '484',),
        (_(u"Micronesia, Federated States of"), 'FM', 'FSM', '583',),
        (_(u"Moldova, Republic of"), 'MD', 'MDA', '498',),
        (_(u"Monaco"), 'MC', 'MCO', '492',),
        (_(u"Mongolia"), 'MN', 'MNG', '496',),
        (_(u"Montenegro"), 'ME', 'MNE', '499',),
        (_(u"Montserrat"), 'MS', 'MSR', '500',),
        (_(u"Morocco"), 'MA', 'MAR', '504',),
        (_(u"Mozambique"), 'MZ', 'MOZ', '508',),
        (_(u"Myanmar"), 'MM', 'MMR', '104',),
        (_(u"Namibia"), 'NA', 'NAM', '516',),
        (_(u"Nauru"), 'NR', 'NRU', '520',),
        (_(u"Nepal"), 'NP', 'NPL', '524',),
        (_(u"Netherlands"), 'NL', 'NLD', '528',),
        (_(u"New Caledonia"), 'NC', 'NCL', '540',),
        (_(u"New Zealand"), 'NZ', 'NZL', '554',),
        (_(u"Nicaragua"), 'NI', 'NIC', '558',),
        (_(u"Niger"), 'NE', 'NER', '562',),
        (_(u"Nigeria"), 'NG', 'NGA', '566',),
        (_(u"Niue"), 'NU', 'NIU', '570',),
        (_(u"Norfolk Island"), 'NF', 'NFK', '574',),
        (_(u"Northern Mariana Islands"), 'MP', 'MNP', '580',),
        (_(u"Norway"), 'NO', 'NOR', '578',),
        (_(u"Oman"), 'OM', 'OMN', '512',),
        (_(u"Pakistan"), 'PK', 'PAK', '586',),
        (_(u"Palau"), 'PW', 'PLW', '585',),
        (_(u"Palestine, State of"), 'PS', 'PSE', '275',),
        (_(u"Panama"), 'PA', 'PAN', '591',),
        (_(u"Papua New Guinea"), 'PG', 'PNG', '598',),
        (_(u"Paraguay"), 'PY', 'PRY', '600',),
        (_(u"Peru"), 'PE', 'PER', '604',),
        (_(u"Philippines"), 'PH', 'PHL', '608',),
        (_(u"Pitcairn"), 'PN', 'PCN', '612',),
        (_(u"Poland"), 'PL', 'POL', '616',),
        (_(u"Portugal"), 'PT', 'PRT', '620',),
        (_(u"Puerto Rico"), 'PR', 'PRI', '630',),
        (_(u"Qatar"), 'QA', 'QAT', '634',),
        (_(u"Réunion"), 'RE', 'REU', '638',),
        (_(u"Romania"), 'RO', 'ROU', '642',),
        (_(u"Russian Federation"), 'RU', 'RUS', '643',),
        (_(u"Rwanda"), 'RW', 'RWA', '646',),
        (_(u"Saint Barthélemy"), 'BL', 'BLM', '652',),
        (_(u"Saint Helena, Ascension and Tristan da Cunha"), 'SH', 'SHN', '654',),
        (_(u"Saint Kitts and Nevis"), 'KN', 'KNA', '659',),
        (_(u"Saint Lucia"), 'LC', 'LCA', '662',),
        (_(u"Saint Martin (French part)"), 'MF', 'MAF', '663',),
        (_(u"Saint Pierre and Miquelon"), 'PM', 'SPM', '666',),
        (_(u"Saint Vincent and the Grenadines"), 'VC', 'VCT', '670',),
        (_(u"Samoa"), 'WS', 'WSM', '882',),
        (_(u"San Marino"), 'SM', 'SMR', '674',),
        (_(u"Sao Tome and Principe"), 'ST', 'STP', '678',),
        (_(u"Saudi Arabia"), 'SA', 'SAU', '682',),
        (_(u"Senegal"), 'SN', 'SEN', '686',),
        (_(u"Serbia"), 'RS', 'SRB', '688',),
        (_(u"Seychelles"), 'SC', 'SYC', '690',),
        (_(u"Sierra Leone"), 'SL', 'SLE', '694',),
        (_(u"Singapore"), 'SG', 'SGP', '702',),
        (_(u"Sint Maarten (Dutch part)"), 'SX', 'SXM', '534',),
        (_(u"Slovakia"), 'SK', 'SVK', '703',),
        (_(u"Slovenia"), 'SI', 'SVN', '705',),
        (_(u"Solomon Islands"), 'SB', 'SLB', '090',),
        (_(u"Somalia"), 'SO', 'SOM', '706',),
        (_(u"South Africa"), 'ZA', 'ZAF', '710',),
        (_(u"South Georgia and the South Sandwich Islands"), 'GS', 'SGS', '239',),
        (_(u"South Sudan"), 'SS', 'SSD', '728',),
        (_(u"Spain"), 'ES', 'ESP', '724',),
        (_(u"Sri Lanka"), 'LK', 'LKA', '144',),
        (_(u"Sudan"), 'SD', 'SDN', '729',),
        (_(u"Suriname"), 'SR', 'SUR', '740',),
        (_(u"Svalbard and Jan Mayen"), 'SJ', 'SJM', '744',),
        (_(u"Swaziland"), 'SZ', 'SWZ', '748',),
        (_(u"Sweden"), 'SE', 'SWE', '752',),
        (_(u"Switzerland"), 'CH', 'CHE', '756',),
        (_(u"Syrian Arab Republic"), 'SY', 'SYR', '760',),
        (_(u"Taiwan, Province of China"), 'TW', 'TWN', '158',),
        (_(u"Tajikistan"), 'TJ', 'TJK', '762',),
        (_(u"Tanzania, United Republic of"), 'TZ', 'TZA', '834',),
        (_(u"Thailand"), 'TH', 'THA', '764',),
        (_(u"Timor-Leste"), 'TL', 'TLS', '626',),
        (_(u"Togo"), 'TG', 'TGO', '768',),
        (_(u"Tokelau"), 'TK', 'TKL', '772',),
        (_(u"Tonga"), 'TO', 'TON', '776',),
        (_(u"Trinidad and Tobago"), 'TT', 'TTO', '780',),
        (_(u"Tunisia"), 'TN', 'TUN', '788',),
        (_(u"Turkey"), 'TR', 'TUR', '792',),
        (_(u"Turkmenistan"), 'TM', 'TKM', '795',),
        (_(u"Turks and Caicos Islands"), 'TC', 'TCA', '796',),
        (_(u"Tuvalu"), 'TV', 'TUV', '798',),
        (_(u"Uganda"), 'UG', 'UGA', '800',),
        (_(u"Ukraine"), 'UA', 'UKR', '804',),
        (_(u"United Arab Emirates"), 'AE', 'ARE', '784',),
        (_(u"United Kingdom"), 'GB', 'GBR', '826',),
        (_(u"United States"), 'US', 'USA', '840',),
        (_(u"United States Minor Outlying Islands"), 'UM', 'UMI', '581',),
        (_(u"Uruguay"), 'UY', 'URY', '858',),
        (_(u"Uzbekistan"), 'UZ', 'UZB', '860',),
        (_(u"Vanuatu"), 'VU', 'VUT', '548',),
        (_(u"Venezuela, Bolivarian Republic of"), 'VE', 'VEN', '862',),
        (_(u"Viet Nam"), 'VN', 'VNM', '704',),
        (_(u"Virgin Islands, British"), 'VG', 'VGB', '092',),
        (_(u"Virgin Islands, U.S."), 'VI', 'VIR', '850',),
        (_(u"Wallis and Futuna"), 'WF', 'WLF', '876',),
        (_(u"Western Sahara"), 'EH', 'ESH', '732',),
        (_(u"Yemen"), 'YE', 'YEM', '887',),
        (_(u"Zambia"), 'ZM', 'ZMB', '894',),
        (_(u"Zimbabwe"), 'ZW', 'ZWE', '716',),

    )
)

COUNTRIES = {
    c.alpha2: c.name
    for c in COUNTRIES_LIST
}

COUNTRIES3 = {
    c.alpha3: c.name
    for c in COUNTRIES_LIST
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
    with open(filename, 'rb') as csv_file:
        for row in csv.reader(csv_file):
            name = row[0].decode('utf-8').rstrip('*')
            name = re.sub(r'\(the\)', '', name)
            if name:
                countries.append((name, row[1].decode('utf-8')))
    with open(__file__, 'r') as source_file:
        contents = source_file.read()
    bits = re.match(
        '(.*\nCOUNTRIES = \{\n)(.*)(\n\}.*)', contents, re.DOTALL).groups()
    country_list = []
    for name, code in countries:
        name = name.replace('"', r'\"').strip()
        country_list.append(
            '    "{code}": _("{name}"),'.format(name=name, code=code))
    content = bits[0]
    content += '\n'.join(country_list).encode('utf-8')
    content += bits[2]
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
