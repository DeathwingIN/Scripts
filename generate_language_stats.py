import os
import requests
from collections import defaultdict
import matplotlib.pyplot as plt

GH_USERNAME = os.getenv('GH_USERNAME')
GH_TOKEN = os.getenv('GH_TOKEN')
# GH_USERNAME = "DeathwingIN"
# GH_TOKEN = "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"

def get_repos(username, token=None):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {token}'} if token else {}
    repos = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get('next', {}).get('url')
    return repos

def get_languages(repo, token=None):
    url = repo['languages_url']
    headers = {'Authorization': f'token {token}'} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    repos = get_repos(GH_USERNAME, GH_TOKEN)
    language_stats = defaultdict(int)

    for repo in repos:
        languages = get_languages(repo, GH_TOKEN)
        for language, bytes_count in languages.items():
            language_stats[language] += bytes_count

    total_bytes = sum(language_stats.values())
    language_percentages = {lang: (count / total_bytes) * 100 for lang, count in language_stats.items()}

    languages = list(language_percentages.keys())
    percentages = list(language_percentages.values())
    colors = plt.cm.tab20c.colors[:len(languages)]  # Get distinct colors for each language

    fig, ax = plt.subplots(figsize=(8, 6), facecolor='black')  # Set entire image background to black
    bars = ax.barh(languages, percentages, color=colors)

    for bar, pct in zip(bars, percentages):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 4, f'{pct:.1f}%', va='center', ha='left', color='green')

    ax.set_title('Most Used Languages', color='green')  # Set title color to green
    ax.invert_yaxis()  # Invert y-axis to display languages from top to bottom
    ax.set_facecolor('black')  # Set background color inside the chart
    ax.tick_params(axis='y', colors='green')  # Set font color for y-axis ticks
    ax.spines['bottom'].set_color('black')  # Remove color for bottom spine
    ax.spines['left'].set_color('black')  # Remove color for left spine
    ax.spines['top'].set_color('black')  # Remove color for top spine
    ax.spines['right'].set_color('black')  # Remove color for right spine
    ax.xaxis.set_visible(False)  # Remove the x-axis
    plt.savefig(os.path.join(os.getcwd(), 'language_stats.png'), bbox_inches='tight')  # Save the plot

# Call the main function
main()
