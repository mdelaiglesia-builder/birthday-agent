import argparse
from extract_action_items import extract_action_items

parser = argparse.ArgumentParser(description="Meeting notes file")
parser.add_argument("filepath", help="Path to the file to analyze")
args = parser.parse_args()

try:
    with open(args.filepath) as f:
        content = f.read()

        action_items = extract_action_items(content)
        
        for a in action_items:
            if (a["owner"] is not None):
                print(f"- {a['task']} ({a['owner']})")
            else:
                print(f"- {a['task']} (unassigned)")
except FileNotFoundError:
    print(f"Error: file '{args.filepath}' not found.")