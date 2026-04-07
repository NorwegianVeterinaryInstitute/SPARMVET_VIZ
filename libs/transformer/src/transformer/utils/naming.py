import re


def clean_column_header(col_name: str) -> str:
    """
    Standard project-wide logic to sanitize complex bioinformatics headers 
    (e.g., Tool/Result:Column) into safe, readable snake_case YAML keys.
    """
    s = str(col_name).lower()
    # Replace slashes, dots, colons, spaces, hyphens with underscores
    s = re.sub(r'[/.:\s\-]+', '_', s)
    # Remove all other non-alphanumeric (except underscores)
    s = re.sub(r'[^\w_]', '', s)
    # Deduplicate underscores (e.g., __ to _)
    s = re.sub(r'_+', '_', s)
    # Strip leading/trailing underscores
    return s.strip('_')
