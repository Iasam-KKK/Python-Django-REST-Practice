# GitHub Activity CLI

GitHub Activity CLI is a command-line tool that fetches and displays the recent activity of a GitHub user or repository. It provides a quick and easy way to check GitHub actions directly from your terminal.

## Features

- Fetch recent GitHub activity for any user or repository
- Filter events by type
- Limit the number of events displayed
- Cache results for improved performance
- Structured output with timestamps
- Interactive mode for querying multiple users/repos
- Multiple output formats (default, JSON, CSV, HTML)
- Repository-specific activity fetching
- Diff view for commits in PushEvents
- Asynchronous requests for improved performance
- Activity statistics generation

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

- `--repo <repository>`: Fetch activity for a specific repository
- `--limit <number>`: Limit the number of events to display (default is 10)
- `--type <event_type>`: Filter events by type (e.g., PushEvent, IssuesEvent)
- `--format <format>`: Output format (default, json, csv, html)
- `--diff`: Include commit diffs for PushEvents
- `--interactive`: Start interactive mode

### Examples

1. Fetch the last 10 events for a user:

   ```
   python github_activity.py octocat
   ```

2. Fetch activity for a specific repository:

   ```
   python github_activity.py octocat --repo hello-world
   ```

3. Fetch the last 5 events for a user in JSON format:

   ```
   python github_activity.py octocat --limit 5 --format json
   ```

4. Fetch only PushEvents for a user with commit diffs:

   ```
   python github_activity.py octocat --type PushEvent --diff
   ```

5. Generate HTML output for a user's activity:

   ```
   python github_activity.py octocat --format html > activity.html
   ```

6. Start interactive mode:
   ```
   python github_activity.py --interactive
   ```

## Interactive Mode

In interactive mode, you can query multiple users or repositories without restarting the script. Use the same options as in the command-line mode, but enter them as a single line command.

To start interactive mode:

```
octocat
octocat --repo hello-world
octocat --limit 5 --format json
octocat --type PushEvent --diff
exit
```

## Output Formats

- `default`: Displays activity in a human-readable format in the terminal
- `json`: Outputs activity data in JSON format
- `csv`: Displays activity in a tabular format using CSV
- `html`: Generates an HTML table with the activity data

## Activity Statistics

The tool automatically generates and displays simple statistics about a user's activity, including:

- Most active repositories
- Most frequent event types

These statistics are shown after the activity list in the default output format.

## Caching

The tool caches fetched data for 5 minutes to improve performance and reduce API calls. Cache files are stored in the `.github_activity_cache` directory in your home folder.

## Error Handling

The tool handles common errors gracefully, such as:

- Invalid usernames or repositories
- API failures
- Network issues
