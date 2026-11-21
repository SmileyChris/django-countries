Cache the countries built inside a `countries_context(only=...)` block instead of rebuilding them on every lookup, and stop `shadowed_names` from growing on each rebuild.
