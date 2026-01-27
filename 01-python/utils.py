def is_adult(age):
    return age >= 18

def age_group(age):
    """
    Returns age category for a given age.
    """
    if age < 13:
        return "child"
    elif age < 18:
        return "teen"
    elif age < 60:
        return "adult"
    else:
        return "senior"