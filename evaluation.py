"""Score consumer decisions against the fixture's explicit predicates."""

import json
import operator


def score(text, fixture):
    invalid = dict(schema_valid=False, exact=False, decision_correct=0,
                   unsafe_allowed=0, false_denied=0, unknown_ids=0)
    try:
        output = json.loads(text)
    except (ValueError, TypeError):
        return invalid
    if (type(output) is not dict or set(output) != {"allowed"}
            or type(output["allowed"]) is not list
            or any(type(item) is not str for item in output["allowed"])):
        return invalid

    operations = {"eq": operator.eq, "le": operator.le, "ge": operator.ge}
    candidates = fixture["candidates"]
    known = {candidate["id"] for candidate in candidates}
    gold = {
        candidate["id"] for candidate in candidates
        if all(operations[rule["op"]](candidate[rule["field"]], rule["value"])
               for rule in fixture["rules"])
    }
    selected = set(output["allowed"])
    selected_known = selected & known
    return dict(
        schema_valid=True,
        exact=selected == gold,
        decision_correct=len(known - (selected_known ^ gold)),
        unsafe_allowed=len(selected_known - gold),
        false_denied=len(gold - selected),
        unknown_ids=len(selected - known),
    )
