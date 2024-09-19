import click
import requests
import json
from datetime import datetime, timedelta
import os
import sys
import asyncio
import aiohttp
import csv
import html
from collections import Counter
from tabulate import tabulate
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Constants
API_BASE_URL = "https://api.github.com"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".github_activity_cache")
CACHE_EXPIRY = timedelta(minutes=5)

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

async def get_cached_data(key):
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cached_data = json.load(f)
        if datetime.now() - datetime.fromisoformat(cached_data["timestamp"]) < CACHE_EXPIRY:
            return cached_data["data"]
    return None

async def cache_data(key, data):
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    cached_data = {
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    with open(cache_file, "w") as f:
        json.dump(cached_data, f)

async def fetch_github_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        elif response.status == 404:
            click.echo(f"Error: Resource not found. URL: {url}")
            return None
        else:
            click.echo(f"Error: Unable to fetch data. Status code: {response.status}. URL: {url}")
            return None

async def fetch_github_activity(session, username, repo=None):
    if repo:
        url = f"{API_BASE_URL}/repos/{username}/{repo}/events"
        cache_key = f"{username}_{repo}"
    else:
        url = f"{API_BASE_URL}/users/{username}/events"
        cache_key = username

    cached_data = await get_cached_data(cache_key)
    if cached_data:
        return cached_data

    events = await fetch_github_data(session, url)
    if events:
        await cache_data(cache_key, events)
    return events

async def fetch_commit_diff(session, username, repo, commit_sha):
    url = f"{API_BASE_URL}/repos/{username}/{repo}/commits/{commit_sha}"
    commit_data = await fetch_github_data(session, url)
    if commit_data and 'files' in commit_data:
        return commit_data['files']
    return None

def format_event(event, include_diff=False):
    event_type = event["type"]
    repo_name = event["repo"]["name"]
    created_at = datetime.fromisoformat(event["created_at"].rstrip("Z"))
    
    if event_type == "PushEvent":
        commits = event["payload"]["commits"]
        result = f"Pushed {len(commits)} commit(s) to {repo_name}"
        if include_diff:
            result += "\nCommit(s) details:"
            for commit in commits:
                result += f"\n  - {commit['sha'][:7]}: {commit['message']}"
        return result
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

def generate_statistics(events):
    repo_activity = Counter()
    event_types = Counter()

    for event in events:
        repo_activity[event["repo"]["name"]] += 1
        event_types[event["type"]] += 1

    most_active_repos = repo_activity.most_common(5)
    most_frequent_events = event_types.most_common(5)

    return {
        "most_active_repos": most_active_repos,
        "most_frequent_events": most_frequent_events
    }

def output_json(data):
    click.echo(json.dumps(data, indent=2))

def output_csv(data):
    headers = ["Timestamp", "Event"]
    rows = [[event["created_at"], format_event(event)] for event in data]
    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))

def output_html(data):
    html_content = "<html><body><table border='1'><tr><th>Timestamp</th><th>Event</th></tr>"
    for event in data:
        html_content += f"<tr><td>{event['created_at']}</td><td>{html.escape(format_event(event))}</td></tr>"
    html_content += "</table></body></html>"
    click.echo(html_content)

async def fetch_and_display_activity(session, username, repo, limit, event_type, output_format, include_diff):
    events = await fetch_github_activity(session, username, repo)
    if not events:
        return

    if event_type:
        events = [e for e in events if e["type"] == event_type]

    events = events[:limit]

    if output_format == "json":
        output_json(events)
    elif output_format == "csv":
        output_csv(events)
    elif output_format == "html":
        output_html(events)
    else:
        for event in events:
            formatted_event = format_event(event, include_diff)
            created_at = datetime.fromisoformat(event["created_at"].rstrip("Z"))
            click.echo(f"[{created_at.strftime('%Y-%m-%d %H:%M:%S')}] {formatted_event}")

            if include_diff and event["type"] == "PushEvent":
                for commit in event["payload"]["commits"]:
                    diff = await fetch_commit_diff(session, username, repo or event["repo"]["name"].split("/")[-1], commit["sha"])
                    if diff:
                        click.echo("\nDiff:")
                        for file in diff:
                            click.echo(f"  {file['filename']}:")
                            click.echo(f"    Changes: +{file['additions']} -{file['deletions']}")

    stats = generate_statistics(events)
    click.echo("\nActivity Statistics:")
    click.echo("Most Active Repositories:")
    for repo, count in stats["most_active_repos"]:
        click.echo(f"  {repo}: {count} events")
    click.echo("\nMost Frequent Event Types:")
    for event_type, count in stats["most_frequent_events"]:
        click.echo(f"  {event_type}: {count} occurrences")

async def interactive_mode():
    session = PromptSession()
    async with aiohttp.ClientSession() as http_session:
        while True:
            try:
                user_input = await session.prompt_async("Enter command (or 'exit' to quit): ")
                if user_input.lower() == 'exit':
                    break

                args = user_input.split()
                if len(args) < 1:
                    click.echo("Invalid command. Please provide a username.")
                    continue

                username = args[0]
                repo = None
                limit = 10
                event_type = None
                output_format = "default"
                include_diff = False

                for i in range(1, len(args)):
                    if args[i] == "--repo" and i + 1 < len(args):
                        repo = args[i + 1]
                    elif args[i] == "--limit" and i + 1 < len(args):
                        limit = int(args[i + 1])
                    elif args[i] == "--type" and i + 1 < len(args):
                        event_type = args[i + 1]
                    elif args[i] == "--format" and i + 1 < len(args):
                        output_format = args[i + 1]
                    elif args[i] == "--diff":
                        include_diff = True

                await fetch_and_display_activity(http_session, username, repo, limit, event_type, output_format, include_diff)

            except KeyboardInterrupt:
                continue
            except EOFError:
                break

@click.command()
@click.argument("username", required=False)
@click.option("--repo", help="Specify a repository")
@click.option("--limit", default=10, help="Number of events to display")
@click.option("--type", "event_type", help="Filter events by type")
@click.option("--format", "output_format", type=click.Choice(["default", "json", "csv", "html"]), default="default", help="Output format")
@click.option("--diff", is_flag=True, help="Include commit diffs for PushEvents")
@click.option("--interactive", is_flag=True, help="Start interactive mode")
def main(username, repo, limit, event_type, output_format, diff, interactive):
    """Fetch and display recent GitHub activity for a user or repository."""
    if interactive:
        asyncio.run(interactive_mode())
    elif username:
        async def run():
            async with aiohttp.ClientSession() as session:
                await fetch_and_display_activity(session, username, repo, limit, event_type, output_format, diff)
        asyncio.run(run())
    else:
        click.echo("Please provide a username or use --interactive for interactive mode.")

if __name__ == "__main__":
    main()