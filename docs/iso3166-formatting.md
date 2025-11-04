# ISO 3166-1 Country Name Formatting

This document explains the formatting patterns, inconsistencies, and historical context of country names in the ISO 3166-1 standard, as used by django-countries.

## Overview

ISO 3166-1 defines short names for countries and territories used in coding (e.g., alpha-2, alpha-3). While the **codes** are rigidly defined, the **names** in the Online Browsing Platform (OBP) have stylistic irregularities—most notably:

* Inconsistent use of **parentheses vs commas**
* Inconsistent **capitalization** of "The"

These quirks stem from how ISO derives its names from **United Nations sources (UNTERM)** and applies **sorting conventions** described in the standard itself.

## Parentheses vs Commas

### Observed Pattern (OBP Data)

**Parentheses:** ~41 countries

Used for:
- **Qualifiers / state designations**
  - "Bolivia (Plurinational State of)"
  - "Iran (Islamic Republic of)"
  - "Netherlands (Kingdom of the)"
- **Articles**
  - "Gambia (the)"
  - "Niger (the)"
- **Alternative or political names**
  - "Falkland Islands (the) [Malvinas]"

**Commas:** Only 4 countries

1. **Bonaire, Sint Eustatius and Saba** – multi-territory list
2. **Palestine, State of** – state designation inversion
3. **Saint Helena, Ascension and Tristan da Cunha** – multi-territory list
4. **Tanzania, the United Republic of** – formal name inversion

### What ISO Says

* ISO 3166-1:2020 allows names to be **"inverted… allowing the distinctive word to appear first"** for alphabetical sorting (Annex F).
* The **comma** signals such inversion: moving the distinctive term first and appending the descriptor after.
* Therefore:
  - **Comma → inversion for sorting** (distinctive word first)
  - **Parentheses → qualifiers or articles**, not part of inversion logic

### Documentary Sources

| Case | Change Origin | Explanation |
|------|---------------|-------------|
| Bonaire, Sint Eustatius and Saba | ISO 3166-1 Newsletter VI-8 (2010-12-15) | New multi-territory name after Netherlands Antilles dissolution |
| Palestine, State of | ISO 3166-1 Newsletter VI-14 (2013-02-06) | Updated following UN recognition; inverted for "distinctive word first" |
| Saint Helena, Ascension and Tristan da Cunha | ISO 3166-1 Newsletter VI-7 (2010-02-22) | Adopted new name listing all three territories |
| Tanzania, the United Republic of | Pre-newsletter era | Inverted per Annex F rule ("distinctive word first") |

## Capitalization of "The"

### Observed Pattern

| Form | Count | Example | Notes |
|------|-------|---------|-------|
| **(The)** (capital T) | 1 | Bahamas (The) – BS | Only case where article is capitalized |
| **(the)** (lower t) | 31 | Gambia (the), Congo (the), Philippines (the)… | All others use lowercase |
| **, the** | 1 | Tanzania, the United Republic of | Comma + lowercase article |

### Reason

* "**The Bahamas**" is officially capitalized in both national and UN usage; even the UN Blue Book lists **Bahamas (The)**.
* For most other countries (e.g., "the Gambia"), ISO aligns with **UNTERM**, which lowercases the article.
* An ISO newsletter (for Gambia) explicitly noted a change for "**alignment of the English short name (lower case) with UNTERM**".

### Interpretation

* ISO uses **UNTERM as the authoritative source**, adopting its casing.
* The Bahamas is an exception honoring **country-preferred capitalization** ("The Bahamas").

## Countries with "(the)" in Names

31 countries have lowercase "(the)" in their official ISO 3166-1 names:

1. British Indian Ocean Territory (the)
2. Cayman Islands (the)
3. Central African Republic (the)
4. Cocos (Keeling) Islands (the)
5. Comoros (the)
6. Congo (the)
7. Congo (the Democratic Republic of the)
8. Cook Islands (the)
9. Dominican Republic (the)
10. Falkland Islands (the) [Malvinas]
11. Faroe Islands (the)
12. French Southern Territories (the)
13. Gambia (the)
14. Holy See (the)
15. Korea (the Democratic People's Republic of)
16. Korea (the Republic of)
17. Lao People's Democratic Republic (the)
18. Marshall Islands (the)
19. Moldova (the Republic of)
20. Niger (the)
21. Northern Mariana Islands (the)
22. Philippines (the)
23. Russian Federation (the)
24. Sudan (the)
25. Syrian Arab Republic (the)
26. Turks and Caicos Islands (the)
27. United Arab Emirates (the)
28. United Kingdom of Great Britain and Northern Ireland (the)
29. United States Minor Outlying Islands (the)
30. United States of America (the)
31. Tanzania, the United Republic of (comma format)

## Structure in ISO 3166-1

From the standard itself:

* **Short name (title case)** – used in OBP, shows parentheses for moved articles and qualifiers.
* **Short NAME (uppercase)** – used in code lists; may invert elements using commas for alphabetical order.

Thus, the punctuation difference partially comes from maintaining **dual representations** (display vs sort forms).

## UN Influence and Historical Politics

ISO's names follow **UNTERM / UN Statistics Division** forms. Parentheses often trace back to UN practice for:

* Politically sensitive dual names (e.g., *Falkland Islands (the) [Malvinas]*)
* Optional or variant designations

Commas arise when the UN or ISO Maintenance Agency needs an **inverted form** for cataloging (rare).

## Summary Table of Formatting Logic

| Symbol | Typical Function | Example | Underlying Rule |
|--------|------------------|---------|-----------------|
| **( )** | Article or qualifier moved after main noun; sometimes alternate name | *Korea (the Republic of)* | Not inversion; mirrors UNTERM "short name" |
| **, ** | Indicates ISO inversion for sorting distinctive word first | *Tanzania, the United Republic of* | Annex F F.2 inversion rule |
| **(The)** vs **(the)** | Capitalized only when article is part of official name | *Bahamas (The)* | Exception aligned to country's preference |
| **Multi-territory commas** | List of distinct geographic units | *Saint Helena, Ascension and Tristan da Cunha* | Literal list, not inversion |

## Implications for django-countries

### Automatic Stripping of "(the)"

The `data.py` self-generation script automatically strips standalone `(the)` from country names:

```python
name = re.sub(r"\(the\)", "", name)
```

This means:
- `"Gambia (the)"` → `"Gambia"`
- `"Niger (the)"` → `"Niger"`
- `"United States of America (the)"` → `"United States of America"`

However, it **does not** strip "the" when it's part of a longer phrase:
- `"Congo (the Democratic Republic of the)"` → keeps as-is (doesn't match the regex)
- `"Netherlands (Kingdom of the)"` → keeps as-is

### Special Cases

**Bahamas (The)**: The only country with capitalized "(The)" is **not** stripped by the regex (which only matches lowercase). This is intentional to preserve the official capitalization preference.

**Netherlands**: Recently updated in OBP from "Netherlands" to "Netherlands (Kingdom of the)" to reflect the official constitutional name.

### Common Names Feature

The `COMMON_NAMES` dictionary in `base.py` provides user-friendly alternatives for countries with verbose official names:

- Primarily used for state designations: "Bolivia" instead of "Bolivia (Plurinational State of)"
- Also used for political simplification: "North Korea" / "South Korea" instead of "Korea (the Democratic People's Republic of)" / "Korea (the Republic of)"
- **Not needed** for countries with standalone "(the)" as these are automatically stripped

When `COUNTRIES_COMMON_NAMES` setting is enabled (default: `True`), these friendly names replace the official ISO names in dropdown lists and displays.

## Political Objections and the "Country" Definition

### Common Objection

A frequent objection to django-countries is that certain territories listed in ISO 3166-1 are "not countries" according to some political viewpoints. These objections have appeared repeatedly in GitHub issues:

**Taiwan naming** ([#16](https://github.com/SmileyChris/django-countries/issues/16), [#29](https://github.com/SmileyChris/django-countries/issues/29), [#60](https://github.com/SmileyChris/django-countries/issues/60), [#342](https://github.com/SmileyChris/django-countries/issues/342)):
- Listed as "Taiwan, Province of China" in ISO 3166-1
- Some users find this offensive and request "Taiwan" or "Republic of China"
- Others request "Taiwan, China" or "Chinese Taipei"

**Kosovo** ([#5](https://github.com/SmileyChris/django-countries/issues/5), [#25](https://github.com/SmileyChris/django-countries/issues/25), [#107](https://github.com/SmileyChris/django-countries/issues/107), [#139](https://github.com/SmileyChris/django-countries/issues/139), [#214](https://github.com/SmileyChris/django-countries/issues/214), [#239](https://github.com/SmileyChris/django-countries/issues/239), [#314](https://github.com/SmileyChris/django-countries/issues/314), [#423](https://github.com/SmileyChris/django-countries/issues/423)):
- Not in ISO 3166-1 (uses temporary code XK)
- Repeatedly requested for inclusion despite not being in the standard
- Now available via `COUNTRIES_OVERRIDE` customization

**Other territories**:
- **Hong Kong** - Special Administrative Region of China
- **Macao** - Special Administrative Region of China
- **Palestine** - Listed as "Palestine, State of"
- **Tibet** - Not recognized as separate from China in ISO 3166-1
- **Vatican City** - Listed as "Holy See (the)"

Users sometimes request that these be:
- Removed from the list entirely
- Renamed (e.g., "Taiwan, China" or "Chinese Taipei")
- Reclassified in some way

### Why django-countries Follows ISO 3166-1

**ISO 3166-1 is not about political "countries"** - it's about **coding areas** for data processing and standardization. The standard itself carefully avoids the term "country" in favor of:

- "Country name" (referring to the short name used for coding)
- "Entity" or "territory"
- "Areas of geographical interest"

ISO 3166-1 includes:

- Sovereign states (e.g., France, Japan)
- Dependent territories (e.g., Guam, French Guiana)
- Special Administrative Regions (e.g., Hong Kong, Macao)
- Disputed territories (e.g., Western Sahara)
- Administrative regions (e.g., Taiwan)

**Why ISO, not political definitions:**

1. **Neutrality** - ISO 3166-1 is maintained by an international standards body, not any single government
2. **Stability** - Political definitions change; ISO provides stable codes for data interchange
3. **Universality** - Used globally for postal codes, domain names (ccTLDs), currency codes, etc.
4. **Practical utility** - Shipping addresses, phone numbers, and payment processing require these regions to be coded

### Customizing for Your Use Case

If your application has specific political requirements or regional considerations, django-countries provides extensive customization options:

**Remove territories:**
```python
COUNTRIES_ONLY = ['US', 'CA', 'MX']  # North America only
```

**Rename territories:**
```python
COUNTRIES_OVERRIDE = {
    'TW': 'Taiwan, China',
    'HK': 'Hong Kong SAR, China',
    'MO': 'Macao SAR, China',
}
```

**Exclude specific territories:**
```python
COUNTRIES_OVERRIDE = {
    'TW': None,  # Removes Taiwan from list
}
```

See the [Customization Guide](advanced/customization.md) for complete details.

### Our Position

django-countries **follows ISO 3166-1 by default** because:

1. It's the international standard for territorial coding
2. It's politically neutral (maintained by ISO, not any government)
3. It's what most developers expect and need
4. It's easily customizable for those with different requirements

We recognize that ISO 3166-1 includes territories that are politically disputed or not universally recognized as independent countries. This is intentional - the standard serves as a coding system for **practical data interchange**, not a political statement about sovereignty.

If the ISO list doesn't match your application's requirements, please use the customization features rather than requesting changes to the default list.

## Conclusions

1. **No single "rule" document** exists for commas vs parentheses; ISO 3166-1's Annex F allows discretion to invert names for sorting.
2. **Parentheses** mark **qualifiers, articles, or alternate names**, mirroring UNTERM.
3. **Commas** mark **inversions** or **multi-territory enumerations**; only four examples appear in the current OBP.
4. **Capitalized "The"** appears solely in *Bahamas (The)* due to **official self-designation**.
5. **All other lowercase articles** follow **UNTERM normalization** (confirmed in a Gambia newsletter).
6. **ISO 3166-1 is a coding standard, not a political definition** - it includes territories regardless of sovereignty status for practical data interchange purposes.

## References

* ISO 3166-1:2020, Clauses 3.14–3.16 & Annex F (sorting/inversion rules)
* ISO 3166-1 Newsletters VI-7, VI-8, VI-14 (2010–2013)
* UN TERM / UN Blue Book country listings
* GitHub discussions highlighting developer confusion about formatting inconsistencies
* ANSI blog "ISO 3166-1:2020 – Country Codes Standard Changes"

## See Also

* [Common Names](usage/settings.md#countries_common_names) - Using friendly country names
* [Customization](advanced/customization.md) - Overriding country names
* [Updating Country Data](contributing.md#updating-country-data) - How to update country data from ISO OBP
