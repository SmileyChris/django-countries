from django_countries import Countries


countries = Countries(
    only={'NZ': 'New Zealand', 'NV': 'Neverland'},
)
