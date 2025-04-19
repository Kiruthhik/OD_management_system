from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    print(f"Accessing key: {key}")
    if dictionary is None or not isinstance(dictionary, dict):
        return []
    print(f"Value: {dictionary.get(key, [])}")
    return dictionary.get(key, [])
