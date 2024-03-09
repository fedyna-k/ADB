def get_flag_emoji(countryCode: str) -> str:
    """
    Get flag emoji from country code.
    from: https://dev.to/jorik/country-code-to-flag-emoji-a21
    :param: countryCode - The country code
    :return: The corresponding flag emoji
    """
    letters = list(countryCode.upper())
    chars = [chr(0x1f1a5 + ord(l)) for l in letters]

    return "".join(chars)