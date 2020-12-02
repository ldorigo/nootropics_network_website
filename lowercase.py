def lowercase(text):
    if isinstance(text, str):
        return text.lower()

    if isinstance(text, list):
        return [string.lower() for string in text]

    else:
        raise TypeError('"text" should be a string or a list of strings')