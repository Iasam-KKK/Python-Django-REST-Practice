# GitHub Activity CLI

GitHub Activity CLI is a command-line tool that fetches and displays the recent activity of a GitHub user. It provides a quick and easy way to check a user's GitHub actions directly from your terminal.

## Features

- Fetch recent GitHub activity for any user
- Filter events by type
- Limit the number of events displayed
- Cache results for improved performance
- Structured output with timestamps

## Installation

1. Clone this repository or download the source code.

2. Navigate to the project directory:

   ````
   cd path/to/github-activity-cli
   ```

   ````

3. Install the required dependencies:
   ````
   pip install -r requirements.txt
   ```
   ````

## Usage

The basic syntax for using the CLI is:

### Options

- `--limit <number>`: Limit the number of events to display (default is 10)
- `--type <event_type>`: Filter events by type (e.g., PushEvent, IssuesEvent)

### Examples

1. Fetch the last 10 events for a user:

   ```
   python github_activity.py octocat
   ```

2. Fetch the last 5 events for a user:

   ```
   python github_activity.py octocat --limit 5
   ```

3. Fetch only PushEvents for a user:

   ```
   python github_activity.py octocat --type PushEvent
   ```

4. Combine options:
   ```
   python github_activity.py octocat --limit 3 --type PushEvent
   ```

## Caching

The tool caches fetched data for 5 minutes to improve performance and reduce API calls. Cache files are stored in the `.github_activity_cache` directory in your home folder.

## Error Handling

The tool handles common errors gracefully, such as:

- Invalid usernames
- API failures
- Network issues
