def format_text(text, settings):
    """
    Format extracted text based on user settings
    """
    if settings.get('remove_extra_spaces'):
        text = " ".join(text.split())
    
    if settings.get('line_spacing'):
        text = text.replace('\n', '\n\n')
    
    return text
