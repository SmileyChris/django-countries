#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    _ = lambda x: x

# Nicely titled (and translatable) region names.
REGIONS = {
    1: _("World"),
    2: _("Africa"),
    3: _("North America"),
    5: _("South America"),
    9: _("Oceania"),
    11: _("Western Africa"),
    13: _("Central America"),
    14: _("Eastern Africa"),
    15: _("Northern Africa"),
    17: _("Middle Africa"),
    18: _("Southern Africa"),
    19: _("Americas"),
    21: _("Northern America"),
    29: _("Caribbean"),
    30: _("Eastern Asia"),
    34: _("Southern Asia"),
    35: _("South-Eastern Asia"),
    39: _("Southern Europe"),
    53: _("Australia and New Zealand"),
    54: _("Melanesia"),
    57: _("Micronesia"),
    61: _("Polynesia"),
    142: _("Asia"),
    143: _("Central Asia"),
    145: _("Western Asia"),
    150: _("Europe"),
    151: _("Eastern Europe"),
    154: _("Northern Europe"),
    155: _("Western Europe"),
}

REGION_MAP = {
    1: [2, 9, 19, 142, 150],
    2: [11, 14, 15, 17, 18],
    3: [13, 21, 29],
    5: [32, 68, 76, 152, 170, 218, 238, 254, 328, 600, 604, 740, 858, 862],
    9: [53, 54, 57, 61],
    11: [132, 204, 270, 288, 324, 384, 430, 466, 478, 562, 566, 624, 654, 686, 694, 768, 854],
    13: [84, 188, 222, 320, 340, 484, 558, 591],
    14: [108, 174, 175, 231, 232, 262, 404, 450, 454, 480, 508, 638, 646, 690, 706, 716, 728, 800, 834, 894],
    15: [12, 434, 504, 729, 732, 788, 818],
    17: [24, 120, 140, 148, 178, 180, 226, 266, 678],
    18: [72, 426, 516, 710, 748],
    19: [5, 13, 21, 29],
    21: [60, 124, 304, 666, 840],
    29: [28, 44, 52, 92, 136, 192, 212, 214, 308, 312, 332, 388, 474, 500, 531, 533, 534, 535, 630, 652, 659, 660, 662, 663, 670, 780, 796, 850],
    30: [156, 344, 392, 408, 410, 446, 496],
    34: [4, 50, 64, 144, 356, 364, 462, 524, 586],
    35: [96, 104, 116, 360, 418, 458, 608, 626, 702, 704, 764],
    39: [8, 20, 70, 191, 292, 300, 336, 380, 470, 499, 620, 674, 688, 705, 724, 807],
    53: [36, 554, 574],
    54: [90, 242, 540, 548, 598],
    57: [296, 316, 520, 580, 583, 584, 585],
    61: [16, 184, 258, 570, 612, 772, 776, 798, 876, 882],
    142: [30, 34, 35, 143, 145],
    143: [398, 417, 762, 795, 860],
    145: [31, 48, 51, 196, 268, 275, 368, 376, 400, 414, 422, 512, 634, 682, 760, 784, 792, 887],
    150: [39, 151, 154, 155],
    151: [100, 112, 203, 348, 498, 616, 642, 643, 703, 804],
    154: [208, 233, 234, 246, 248, 352, 372, 428, 440, 578, 680, 744, 752, 826, 830, 831, 832, 833],
    155: [40, 56, 250, 276, 438, 442, 492, 528, 756],
}

MAP_REGION = {
    2: [1],
}


def self_generate(
                output_filename, url='http://unstats.un.org/unsd/methods/m49/m49regin.htm'): # pragma: no cover
                
                import re
                import requests
                import pprint
                try:
                    from html.parser import HTMLParser
                except ImportError as e:
                    from HTMLParser import HTMLParser
                
                class regionHTMLParser(HTMLParser): # pragma: no cover
                    def __init__(self):
                        HTMLParser.__init__(self)
                        self.regionTableFound = False
                        
                        self.foundTD = False
                        self.foundH3 = False
                        self.foundB = False
                        self.foundI = False
                        self.foundP = False
                        self.isFootnote = False
                        
                        self.regions = {
                            "001World": [],
                            # From Footnote b/
                            "003North America": ["21", "29", "13"]
                            }
                        self.region_tree = []
                        self.regions_tree = {}
                        self.region_data = []
                        self.text = ""
                    
                    def add_to_region_tree(self):
                        self.regions_tree[self.region_tree[-1]] = self.region_data
                        self.region_data = []
                        self.region_tree.pop()
                        
                    def add_regions(self):
                        if len(self.regions_tree.keys()) > 0:
                            new_regions = self.regions.copy()
                            new_regions.update(self.regions_tree)
                            self.regions = new_regions
                            self.regions[self.region_tree[-1]] = list(self.regions_tree.keys())
                            region = self.region_tree.pop()
                            
                            while len(self.region_tree) > 0:
                                if  self.region_tree[-1] not in self.regions:
                                    self.regions[self.region_tree[-1]] = [region]
                                else:
                                    self.regions[self.region_tree[-1]].append(region)
                                region = self.region_tree.pop()
                            
                            self.regions["001World"].append(region)
                            self.regions_tree = {}
                    
                    def handle_starttag(self, tag, attrs):
                        if self.regionTableFound:
                            if tag == "td":
                                # td is for collecting text
                                self.foundTD = True
                            if tag == "h3":
                                # h3 is a new top level
                                self.foundH3 = True
                            elif tag == "b":
                                # b is a new region level
                                self.foundB = True
                            #elif tag == "i":
                                # i is a new region level
                                #self.foundI = True
                            elif tag == "p":
                                # p is a country
                                self.foundP = True
                            elif tag == "a":
                                for attr in attrs:
                                    if attr[0] == 'href' and "#ftn" in attr[1] :
                                        self.isFootnote = True
                            elif tag == "td":
                                for attr in attrs:
                                    if attr[0] == 'class'  and attr[1] == 'cheader2':
                                        if self.regionTableFound:
                                            self.add_to_region_tree()
                                            self.add_regions()
                                        self.regionTableFound = False
                    
                    def handle_endtag(self, tag):
                        if self.regionTableFound:
                            if tag == "table":
                                if self.regionTableFound:
                                    self.add_to_region_tree()
                                    self.add_regions()
                                self.regionTableFound = False
                            elif tag == "tr":
                                # Ignore 419 Latin America & Caribean, 
                                # hierarchy in html is not clear
                                if not "419" in self.text:
                                    if (self.foundH3 or self.foundB or self.foundI):
                                        if len(self.region_data) > 0:
                                            self.add_to_region_tree()
                                        if self.foundH3:
                                            self.add_regions()
                                        
                                        self.region_tree.append(self.text)
                                    elif self.text and len(self.region_tree) > 0:
                                        self.region_data.append(self.text)
                                
                                self.text = ""
                                
                                self.foundTD = False
                                self.foundH3 = False
                                self.foundB = False
                                self.foundI = False
                                self.foundP = False
                            elif tag == "a" and self.isFootnote:
                                self.isFootnote = False
                    
                    def handle_data(self, data):
                        if not self.regionTableFound and "Geographical region" in data and "each region" in data:
                            self.regionTableFound = True
                        elif self.foundTD and not self.isFootnote: 
                            self.text = self.text + data.strip()

                r = requests.get(url)
                parser = regionHTMLParser()
                parser.feed(r.text)
                regions = sorted(parser.regions.keys())
                
                with open(__file__, 'r') as source_file:
                    contents = source_file.read()
                # Write regions.
                bits = re.match(
                    '(.*\nREGIONS = \{\n)(.*?)(\n\}.*)', contents, re.DOTALL).groups()
                region_list = []
                for name in regions:
                    code = name[0:3].lstrip('0')
                    name = name[3:]
                    region_list.append(
                        '    {code}: _("{name}"),'.format(name=name, code=code))
                content = bits[0].encode('utf-8')
                content += '\n'.join(region_list).encode('utf-8')
                # Write regions map
                map_bits = re.match(
                    '(.*\nREGION_MAP = \{\n)(.*?)(\n\}.*)', bits[2], re.DOTALL).groups()
                map_list = []
                region_maps = {}
                for name in regions:
                    code = name[0:3].lstrip('0')
                    region_map = []
                    for region in parser.regions[name]:
                        region_map.append(int(region[0:3]))
                    region_maps[code] = sorted(region_map)
                    map_list.append(
                        '    {code}: [{region_map}],'.format(code=code, region_map=', '.join(str(x) for x in region_maps[code])))
                content += map_bits[0].encode('utf-8')
                content += '\n'.join(map_list).encode('utf-8')
                content += map_bits[2].encode('utf-8')
                # Write inverse regions map
                """" 
                bits_map = re.match(
                    '(.*\nMAP_REGION = \{\n)(.*?)(\n\}.*)', map_bits[2], re.DOTALL).groups()
                list_map = []
                maps_region = {}
                for code in sorted(region_maps.keys()):
                    for region_code in region_maps[code]:
                        if region_code not in maps_region:
                            maps_region[region_code] = []
                        maps_region[region_code].append(int(code))
                        
                for code in maps_region:
                    for region_code in maps_region[code]:
                        if region_code in maps_region:
                            for code_region in maps_region[region_code]:
                                if code_region not in maps_region[code]:
                                    maps_region[code].append(code_region)
                        
                for code in sorted(maps_region.keys()):
                    list_map.append(
                        '    {code}: [{map_region}],'.format(code=code, map_region=', '.join(str(x) for x in sorted(maps_region[code]))))
                        
                content += bits_map[0].encode('utf-8')
                content += '\n'.join(list_map).encode('utf-8')
                content += bits_map[2].encode('utf-8')
                """
                # Generate file.
                with open(output_filename, 'wb') as output_file:
                    output_file.write(content)
                return parser.regions

if __name__ == '__main__':  # pragma: no cover
    regions = self_generate(__file__)
    print('Wrote {0} regions.'.format(len(regions)))
    print("")
