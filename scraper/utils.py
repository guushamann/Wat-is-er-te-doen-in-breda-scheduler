import re
from urllib.parse import urlparse
def url_path_starts_with_number(url):
    # Parse the URL and extract the path
    path = urlparse(url).path
    
    # Check if the path starts with a number using a regular expression
    return bool(re.match(r"^/\d", path))

def extract_leading_number(url):
    # Parse the URL and extract the path
    path = urlparse(url).path
    
    # Use a regular expression to extract the leading number
    match = re.match(r"^/(\d+)", path)
    return int(match.group(1)) if match else None


def write_file(txt,path):
    f = open(path, 'w+')        
    f.truncate(0)
    f.write(txt)
    f.close()


def to_dict(obj):
    if hasattr(obj, '__dict__'):
        return {key: to_dict(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_dict(item) for item in obj]
    return obj

