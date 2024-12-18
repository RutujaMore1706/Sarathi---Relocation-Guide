#access_token = 'bhed8hjp0bv46jp3jbohqcabld'  # Replace with your actual Meetup API access token


'''                                ******************************JSON****************************
import requests
import time
import json

API_URL = "https://api.meetup.com/gql"
API_TOKEN = "bhed8hjp0bv46jp3jbohqcabld"  # Replace with your actual API token

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

query = """
query GetBostonGroups($cursor: String) {
  keywordSearch(
    input: {
      first: 10, 
      after: $cursor
    },
    filter: {
      source: GROUPS,
      lat: 42.3601,
      lon: -71.0589,
      radius: 25,
      query: "Boston"
    }
  ) {
    count
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        result {
          ... on Group {
            id
            name
            urlname
            description
            link
            city
            zip
            memberships {
              count
            }
            topicCategory {
              id
              name
            }
            pastEvents(input: {first: 3}) {
              edges {
                node {
                  id
                  title
                  dateTime
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

def fetch_groups(cursor=None):
    variables = {"cursor": cursor}
    response = requests.post(API_URL, json={"query": query, "variables": variables}, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.text)
        return None
    
    return response.json()["data"]["keywordSearch"]

def get_all_boston_groups():
    all_groups = []
    cursor = None
    
    while True:
        result = fetch_groups(cursor)
        if result is None:
            print("Error fetching groups. Stopping.")
            break
        
        groups = [edge["node"]["result"] for edge in result["edges"]]
        all_groups.extend(groups)
        
        if not result["pageInfo"]["hasNextPage"]:
            break
        
        cursor = result["pageInfo"]["endCursor"]
        time.sleep(1)  # Add a delay to avoid hitting rate limits
    
    return all_groups

# Fetch and print all Boston groups
boston_groups = get_all_boston_groups()
print(f"Total groups found: {len(boston_groups)}")

# Save the data to a JSON file
output_file = "boston_groups.json"
with open(output_file, 'w') as f:
    json.dump(boston_groups, f, indent=4)

print(f"Data saved to {output_file}")
'''

import requests
import time
import json
import csv 

API_URL = "https://api.meetup.com/gql"
API_TOKEN = "bhed8hjp0bv46jp3jbohqcabld"  # Replace with your actual API token

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

query = """
query GetBostonGroups($cursor: String) {
  keywordSearch(
    input: {
      first: 10, 
      after: $cursor
    },
    filter: {
      source: GROUPS,
      lat: 42.3601,
      lon: -71.0589,
      radius: 25,
      query: "Boston"
    }
  ) {
    count
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        result {
          ... on Group {
            id
            name
            urlname
            description
            link
            city
            zip
            memberships {
              count
            }
            topicCategory {
              id
              name
            }
            topics {
                      name
            }
            pastEvents(input: {first: 3}) {
              edges {
                node {
                  id
                  title
                  dateTime
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

def fetch_groups(cursor=None):
    variables = {"cursor": cursor}
    response = requests.post(API_URL, json={"query": query, "variables": variables}, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.text)
        return None
    
    return response.json()["data"]["keywordSearch"]

def get_all_boston_groups():
    all_groups = []
    cursor = None
    
    while True:
        result = fetch_groups(cursor)
        if result is None:
            print("Error fetching groups. Stopping.")
            break
        
        groups = [edge["node"]["result"] for edge in result["edges"]]
        all_groups.extend(groups)
        
        if not result["pageInfo"]["hasNextPage"]:
            break
        
        cursor = result["pageInfo"]["endCursor"]
        time.sleep(1)  # Add a delay to avoid hitting rate limits
    
    return all_groups

# Fetch and print all Boston groups
boston_groups = get_all_boston_groups()
print(f"Total groups found: {len(boston_groups)}")


def save_groups_to_csv(groups, filename="boston_groups.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow([
            "Name", "Description", "Link", "City", "Zip", "Member Count", "Topic Category", "Topics","Past Events"
        ])
        
        for group in groups:
            past_events = "; ".join(
                [f"{event['node']['title']} (ID: {event['node']['id']}, Date: {event['node']['dateTime']})"
                 for event in group['pastEvents']['edges']]
            )
            writer.writerow([
                group['name'],
                group['description'][:100] if group['description'] else "No description",
                group['link'],
                group['city'],
                group['zip'],
                group['memberships']['count'],
                group['topicCategory']['name'] if group['topicCategory'] else "No category",
                ', '.join([topic['name'] for topic in group['topics']]) if 'topics' in group and group['topics'] else "No Topics",
                past_events
            ])

# Save the data to a CSV file
save_groups_to_csv(boston_groups)
print(f"Total groups found: {len(boston_groups)}")