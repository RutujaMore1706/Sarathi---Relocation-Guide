import csv
import re
from collections import defaultdict

def clean_description(desc):
    # HTML tags
    desc = re.sub('<[^<]+?>', '', desc)
    # unwanted characters
    desc = re.sub(r'[^\w\s.,!?-]', '', desc)
    return desc.strip()

def clean_past_events(events):
    if not events:
        return ""
    cleaned_events = []
    for event in events.split(';'):
        match = re.search(r'(.*?)\s*\(ID:', event.strip())
        if match:
            event_name = match.group(1).strip()

            # duplicate parentheses
            event_name = re.sub(r'\s*\([^)]*\)\s*', '', event_name)
            # emojis and other special characters
            event_name = re.sub(r'[^\w\s.,!?-]', '', event_name)

            date_match = re.search(r'Date:\s*([\d-]+)', event)  # Only captures the date (YYYY-MM-DD)
            date = date_match.group(1) if date_match else ""
            cleaned_events.append(f"{event_name}(Date: {date})")
    return ", ".join(cleaned_events)


input_file = 'boston_groups.csv'
output_file = 'cleaned_boston_groups.csv'

groups = defaultdict(dict)

with open(input_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['Name']
        if name not in groups:
            groups[name] = row
            groups[name]['Description'] = clean_description(row['Description'])
            groups[name]['Past Events'] = clean_past_events(row['Past Events'])

# Write the cleaned data
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Description', 'Link', 'City', 'Zip', 'Member Count', 'Topic Category', 'Topics', 'Past Events']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for group in groups.values():
        writer.writerow(group)

print(f"{output_file}")