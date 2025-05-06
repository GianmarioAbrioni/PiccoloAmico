from datetime import datetime

def string_to_date(date_string):
    """Convert a string to a date object."""
    if not date_string:
        return None
    
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None
