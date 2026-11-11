def normalize_registration(plate):
    """
    Removes spaces, dashes and dots from a registration number and upper-cases it.

    Bug fixed: the original function assumed plate was a non-empty string.
    It crashed on None (AttributeError) and returned an empty string for ''.
    Now raises ValueError for any non-string or blank input.
    """
    if not isinstance(plate, str):
        raise ValueError("registration must be a string")
    plate = plate.strip()
    if not plate:
        raise ValueError("registration cannot be blank")
    plate = plate.upper()
    for ch in [' ', '-', '.']:
        plate = plate.replace(ch, '')
    if not plate:
        raise ValueError("registration contains no alphanumeric characters")
    return plate


def total_claim_amount(text):
    """
    Adds up claim amounts separated by semicolons.

    Bug fixed: the original function assumed every token was a whole number.
    It crashed with ValueError on empty strings, whitespace-only input, or
    non-numeric tokens (e.g. '12000;abc;800').
    Now raises ValueError with a descriptive message for any invalid token,
    and handles trailing/leading whitespace around each amount.
    """
    if not isinstance(text, str):
        raise ValueError("input must be a string")
    text = text.strip()
    if not text:
        raise ValueError("input cannot be blank")
    total = 0
    for token in text.split(';'):
        token = token.strip()
        if not token.lstrip('-').isdigit():
            raise ValueError(f"invalid claim amount: {token!r}")
        total += int(token)
    return total


def driver_age(dob, current_year=2026):
    """
    Works out the driver's age from a DD/MM/YYYY date of birth.

    Bug fixed: the original function assumed dob always had three '/'-separated
    parts and that the third part was a valid integer year.
    It crashed with:
      - ValueError / IndexError on strings without exactly three parts
      - ValueError on a non-numeric year field (e.g. '14/08/YYYY')
    Now raises ValueError with a descriptive message for any malformed input.
    """
    if not isinstance(dob, str):
        raise ValueError("date of birth must be a string")
    parts = dob.split('/')
    if len(parts) != 3:
        raise ValueError("date of birth must be in DD/MM/YYYY format")
    day_str, month_str, year_str = parts
    if not year_str.isdigit():
        raise ValueError(f"invalid year in date of birth: {year_str!r}")
    return current_year - int(year_str)


def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    try:
        print("Normalized registration:", normalize_registration(value))
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    try:
        print("Total claimed:", total_claim_amount(value))
    except ValueError as e:
        print("Error:", e)

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    try:
        print("Driver age in 2026:", driver_age(value))
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
