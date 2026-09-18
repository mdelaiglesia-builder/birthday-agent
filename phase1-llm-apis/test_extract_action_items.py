from extract_action_items import extract_action_items


def test_single_action_item():
    notes = "Team sync: Ana will update the deployment docs by Monday."
    result = extract_action_items(notes)
    assert len(result) == 1
    assert result[0]["owner"] == "Ana"


def test_no_action_items():
    notes = (
        "Quick catch-up: we talked about the recent conference and swapped "
        "some notes. Nothing to follow up on."
    )
    result = extract_action_items(notes)
    assert len(result) == 0


def test_three_action_items():
    notes = (
        "Standup: Laura will fix the login bug today. Diego is going to "
        "write the migration script by end of week. We also agreed the "
        "release notes still need a rewrite, but nobody's picked it up yet."
    )
    result = extract_action_items(notes)
    assert len(result) == 3
    assert result[0]["owner"] == "Laura"
    assert result[1]["owner"] == "Diego"
    assert result[2]["owner"] is None
