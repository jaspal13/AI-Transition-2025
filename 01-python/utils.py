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

def build_age_group_lookup(people):
    """
    Returns a dict mapping name -> age_group
    """
    return {
        p["name"]: age_group(p["age"])
        for p in people
    }

def prepare_people_data(people):
    """
    High-level data preparation pipeline.
    Returns enriched_people, lookup
    """
    enriched = enrich_people_with_age_group(people)
    lookup = build_age_group_lookup(people)
    return enriched, lookup

def prepare_people_data_validated(people):
    """
    Validates and prepares people data.

    Returns:
      valid_people: list of enriched people dicts
      errors: list of error messages
    """
    valid_people, errors = [],[]
    for idx, p in enumerate(people):
        if "name" not in p or "age" not in p:
            errors.append(f"Index {idx}: missing required fields")
            continue
        if not isinstance(p["age"],int) or p["age"]<0:
            errors.append(f"Index {idx}: Age is invalid")
        enriched_person = {
            "name":p["name"],
            "age":p["age"],
            "age_group":age_group(p["age"])
        }
        valid_people.append(enriched_person)
    return valid_people, errors

