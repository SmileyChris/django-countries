Fix `Country` equality and hashing when `countries_str_attr` is not `"code"`. Two such `Country` objects never compared equal, and the admin showed an empty value for these fields.
