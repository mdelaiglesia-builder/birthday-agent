from extract_action_items import extract_action_items

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")

notes1 = "Team sync: Ana will update the deployment docs by Monday."
result1 = extract_action_items(notes1)
check("single action item, count", len(result1) == 1)
check("single action item, owner", result1[0]["owner"] == "Ana")

notes2 = "Quick catch-up: we talked about the recent conference and swapped some notes. Nothing to follow up on."
result2 = extract_action_items(notes2)
check("no action items detected, count", len(result2) == 0)

notes3 = "Standup: Laura will fix the login bug today. Diego is going to write the migration script by end of week. We also agreed the release notes still need a rewrite, but nobody's picked it up yet."
result3 = extract_action_items(notes3)
check("three action items, count", len(result3) == 3)
check("three action items, owner 1 (Laura)", result3[0]["owner"] == "Laura")
check("three action items, owner 2 (Diego)", result3[1]["owner"] == "Diego")
check("three action items, owner 3 (None)", result3[2]["owner"] is None)