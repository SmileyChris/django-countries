# Template Tags

## Overview

Django Countries provides template tags to work with countries in your templates without using a `CountryField` directly.

## Loading the Template Tags

First, load the countries template tag library at the top of your template:

```django
{% load countries %}
```

## get_country

If you have your country code stored in a different place than a `CountryField`, you can use the `get_country` template tag to get a `Country` object and have access to all of its properties.

### Syntax

```django
{% get_country 'COUNTRY_CODE' as variable_name %}
```

### Example

```django
{% load countries %}
{% get_country 'BR' as country %}
{{ country.name }}
```

This will output: `Brazil`

### Accessing Country Properties

Once you have a country object, you can access any of its properties:

```django
{% load countries %}
{% get_country 'NZ' as country %}

<h2>{{ country.name }}</h2>
<p>Code: {{ country.code }}</p>
<p>Alpha3: {{ country.alpha3 }}</p>
<p>Flag: <img src="{{ country.flag }}" alt="{{ country.name }} flag"></p>
<p>Unicode flag: {{ country.unicode_flag }}</p>
```

### Using Variables

You can also use a variable instead of a hard-coded country code:

```django
{% load countries %}
{% get_country user_country_code as country %}
<p>Welcome from {{ country.name }}!</p>
```

## get_countries

If you need a list of all countries, use the `get_countries` tag:

### Syntax

```django
{% get_countries as variable_name %}
```

### Example

```django
{% load countries %}
{% get_countries as countries %}
<select name="country">
  {% for country in countries %}
    <option value="{{ country.code }}">{{ country.name }}</option>
  {% endfor %}
</select>
```

This creates a dropdown with all available countries.

### Building Custom Selects

You can use this to build more complex selects:

```django
{% load countries %}
{% get_countries as countries %}

<select name="country" id="country-select">
  <option value="">-- Select a country --</option>
  {% for country in countries %}
    <option value="{{ country.code }}" {% if country.code == selected_country %}selected{% endif %}>
      {{ country.unicode_flag }} {{ country.name }}
    </option>
  {% endfor %}
</select>
```

### Filtering Countries

The `get_countries` tag respects your project's settings like `COUNTRIES_ONLY`, `COUNTRIES_OVERRIDE`, and `COUNTRIES_FIRST`.

## Displaying Flags

### Individual Flag Images

```django
{% load countries %}
{% load static %}

{% get_country 'US' as country %}
<img src="{{ country.flag }}" alt="{{ country.name }} flag">
```

### Flag Sprites (Recommended)

For better performance when displaying multiple flags, use the CSS sprite:

```django
{% load countries %}
{% load static %}

<link rel="stylesheet" href="{% static 'flags/sprite.css' %}">

{% get_country 'FR' as country %}
<i class="{{ country.flag_css }}"></i>
```

### High-Resolution Flag Sprites

For high-DPI displays:

```django
{% load countries %}
{% load static %}

<link rel="stylesheet" href="{% static 'flags/sprite-hq.css' %}">

{% get_country 'JP' as country %}
Normal: <i class="{{ country.flag_css }}"></i>
Large: <i class="flag2x {{ country.flag_css }}"></i>
Extra Large: <i class="flag3x {{ country.flag_css }}"></i>
```

### Accessible Flags

For better accessibility, add `aria-label`:

```django
{% load countries %}
{% load static %}

<link rel="stylesheet" href="{% static 'flags/sprite.css' %}">

{% get_country 'CA' as country %}
<i class="{{ country.flag_css }}"
   aria-label="{% blocktrans with country_code=country.code %}
     {{ country_code }} flag
   {% endblocktrans %}"></i>
```

## Unicode Flag Emoji

Modern browsers and operating systems support unicode flag emoji:

```django
{% load countries %}
{% get_country 'DE' as country %}
{{ country.unicode_flag }} {{ country.name }}
```

This will display: 🇩🇪 Germany

## Complete Example

Here's a complete example combining multiple template tags:

```django
{% load countries %}
{% load static %}

<link rel="stylesheet" href="{% static 'flags/sprite-hq.css' %}">

<h1>Country Directory</h1>

{% get_countries as countries %}
<div class="country-list">
  {% for country in countries %}
    <div class="country-item">
      <i class="flag2x {{ country.flag_css }}" aria-label="{{ country.code }} flag"></i>
      <h3>{{ country.name }}</h3>
      <dl>
        <dt>Code:</dt>
        <dd>{{ country.code }}</dd>
        <dt>Alpha3:</dt>
        <dd>{{ country.alpha3 }}</dd>
        <dt>Numeric:</dt>
        <dd>{{ country.numeric }}</dd>
        <dt>IOC:</dt>
        <dd>{{ country.ioc_code }}</dd>
      </dl>
    </div>
  {% endfor %}
</div>
```

## See Also

- [CountryField Reference](field.md) - Learn about the Country object properties
- [Forms & Widgets](forms.md) - Use countries in forms
- [Settings](settings.md) - Configure which countries are available
