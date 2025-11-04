# Forms & Widgets

## CountrySelectWidget

A widget is included that can show the flag image after the select box (updated with JavaScript when the selection changes).

### Basic Usage

When you create your form, you can use this custom widget like normal:

```python
from django import forms
from django_countries.widgets import CountrySelectWidget
from myapp import models

class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ("name", "country")
        widgets = {"country": CountrySelectWidget()}
```

### Customizing the Layout

Pass a `layout` text argument to the widget to change the positioning of the flag and widget. The default layout is:

```python
'{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'
```

You can customize it like this:

```python
from django_countries.widgets import CountrySelectWidget

class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ("name", "country")
        widgets = {
            "country": CountrySelectWidget(
                layout='<div>{widget}</div><div><img src="{country.flag}"></div>'
            )
        }
```

## Custom Forms

If you want to use the countries in a custom form (not a ModelForm), use the model field's custom form field to ensure the translatable strings for the country choices are left lazy until the widget renders:

```python
from django import forms
from django_countries.fields import CountryField

class CustomForm(forms.Form):
    country = CountryField().formfield()
```

### Non-Required Fields

Use `CountryField(blank=True)` for non-required form fields:

```python
class CustomForm(forms.Form):
    country = CountryField(blank=True).formfield()
```

### Custom Blank Label

Use `blank_label` to customize the label for the initial blank option:

```python
class CustomForm(forms.Form):
    country = CountryField(blank_label="(Select country)").formfield()
```

### Using CountrySelectWidget in Custom Forms

You can also use the CountrySelectWidget as the widget for this field if you want the flag image after the select box:

```python
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CustomForm(forms.Form):
    country = CountryField().formfield(widget=CountrySelectWidget())
```

## Examples

### Basic ModelForm

```python
from django import forms
from myapp.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'country']
```

This will automatically use the appropriate form field for the CountryField.

### ModelForm with Custom Widget

```python
from django import forms
from django_countries.widgets import CountrySelectWidget
from myapp.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'country']
        widgets = {
            'country': CountrySelectWidget()
        }
```

### Standalone Form

```python
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget()
    )
```

## See Also

- [CountryField Reference](field.md) - Learn about the country field
- [Multiple Countries](../advanced/multiple.md) - Handle multiple country selection
- [Customization](../advanced/customization.md) - Customize country lists per field
