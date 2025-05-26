import re

def extract_endpoints(js_code):
    pattern = re.compile(r'(?<=[\'"`])\/[a-zA-Z0-9_\-\/\.]*?(?=[\'"`])')
    return sorted(set(pattern.findall(js_code)))
