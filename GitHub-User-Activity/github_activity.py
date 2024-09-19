import click
import requests
import json
from datetime import datetime, timedelta
import os
import sys

# Constants
API_BASE_URL = "https://api.github.com"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".github_activity_cache")
CACHE_EXPIRY = timedelta(minutes=5)

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cached_data(username):
    cache_file = os.path.join(CACHE_DIR, f"{username}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cached_data = json.load(f)
        if datetime.now() - datetime.fromisoformat(cached_data["timestamp"]) < CACHE_EXPIRY:
            return cached_data["events"]
    return None

def cache_data(username, events):
    cache_file = os.path.join(CACHE_DIR, f"{username}.json")
    cached_data = {
        "timestamp": datetime.now().isoformat(),
        "events": events
    }
    with open(cache_file, "w") as f:
        json.dump(cached_data, f)

def fetch_github_activity(username):
    cached_data = get_cached_data(username)
    if cached_data:
        return cached_data

    url = f"{API_BASE_URL}/users/{username}/events"
    response = requests.get(url)
    
    if response.status_code == 200:
        events = response.json()
        cache_data(username, events)
        return events
    elif response.status_code == 404:
        click.echo(f"Error: User '{username}' not found.")
        sys.exit(1)
    else:
        click.echo(f"Error: Unable to fetch data. Status code: {response.status_code}")
        sys.exit(1)

def format_event(event):
    event_type = event["type"]
    repo_name = event["repo"]["name"]
    created_at = datetime.fromisoformat(event["created_at"].rstrip("Z"))
    
    if event_type == "PushEvent":
        commits = event["payload"]["commits"]
        return f"Pushed {len(commits)} commit(s) to {repo_name}"
    elif event_type == "IssuesEvent":
        action = event["payload"]["action"]
        issue_number = event["payload"]["issue"]["number"]
        return f"{action.capitalize()} issue #{issue_number} in {repo_name}"
    elif event_type == "PullRequestEvent":
        action = event["payload"]["action"]
        pr_number = event["payload"]["pull_request"]["number"]
        return f"{action.capitalize()} pull request #{pr_number} in {repo_name}"
    elif event_type == "CreateEvent":
        ref_type = event["payload"]["ref_type"]
        return f"Created {ref_type} in {repo_name}"
    elif event_type == "DeleteEvent":
        ref_type = event["payload"]["ref_type"]
        return f"Deleted {ref_type} in {repo_name}"
    elif event_type == "WatchEvent":
        return f"Starred {repo_name}"
    else:
        return f"{event_type} in {repo_name}"

@click.command()
@click.argument("username")
@click.option("--limit", default=10, help="Number of events to display")
@click.option("--type", "event_type", help="Filter events by type")
def main(username, limit, event_type):
    """Fetch and display recent GitHub activity for a user."""
    events = fetch_github_activity(username)
    
    if event_type:
        events = [e for e in events if e["type"] == event_type]
    
    click.echo(f"Recent GitHub activity for {username}:")
    for event in events[:limit]:
        formatted_event = format_event(event)
        created_at = datetime.fromisoformat(event["created_at"].rstrip("Z"))
        click.echo(f"[{created_at.strftime('%Y-%m-%d %H:%M:%S')}] {formatted_event}")

if __name__ == "__main__":
    main()