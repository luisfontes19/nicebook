def number_to_letter(number):
    # Determine the number of letters in the alphabet
    alphabet_size = 26

    # Convert the number to the corresponding letter in the alphabet
    letter = chr((number - 1) % alphabet_size + ord('A'))

    # If the number exceeds the alphabet size, increment to the next letter
    if number > alphabet_size:
        letter = letter + chr((number - 1) // alphabet_size + ord('A'))

    return letter


def number_to_roman(number):
    roman_numerals = {
        1: 'I',
        4: 'IV',
        5: 'V',
        9: 'IX',
        10: 'X',
        40: 'XL',
        50: 'L',
        90: 'XC',
        100: 'C',
        400: 'CD',
        500: 'D',
        900: 'CM',
        1000: 'M'
    }

    result = ''
    for value, numeral in sorted(roman_numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result

