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

def enrich_people_with_age_group(people):
    """
    Takes a list of people dicts and adds age_group to each.
    Returns a NEW list.
    """
    return [
        {
            "name": p["name"],
            "age": p["age"],
            "age_group": age_group(p["age"])
        }
        for p in people
    ]