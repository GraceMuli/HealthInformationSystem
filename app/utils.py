def format_name(name):
    return name.title().strip()

def validate_age(age):
    return age.isdigit() and 0 < int(age) < 130