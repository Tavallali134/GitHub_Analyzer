"""GitHub_Analyzer: Created by Amir Mohammad Tavallali Nia!

You can refer to this link to see my games and apps:
https://t.me/A_M_T_N134
"""

import asyncio
import sys
from ghapi.all import GhApi

class GitHubAnalyzer():
    def __init__(self):
        self.api = GhApi()
        self.user_name = input("Enter your username in GitHub: ").strip()
        if not self.user_name:
            print("Username cannot be empty!")
            sys.exit()
        self.page_items = int(input("Enter number of items per page: "))
        self.page_number = int(input("Enter page number: "))
        self.repo_name = None
        self.command = None

    async def information(self):
        user = await self.api.users.get_by_username(self.user_name)
        print(f"\nInformation for @{self.user_name}")
        print(f"Followers: {user.followers}")
        print(f"Following: {user.following}")
        print(f"Name: {user.name}")
        print(f"Profile: {user.html_url}")

    async def user_followers(self):
        followers = await self.api.users.list_followers_for_user(username=self.user_name, per_page=self.page_items, page=self.page_number)
        print(f"\nFollowers of @{self.user_name} (page {self.page_number}):")
        for f in followers:
            print(f"  @{f.login}")

    async def user_followings(self):
        following = await self.api.users.list_following_for_user(username=self.user_name, per_page=self.page_items, page=self.page_number)
        print(f"\nFollowings of @{self.user_name} (page {self.page_number}):")
        for f in following:
            print(f"  @{f.login}")

    async def compare(self):
        followers = await self.api.users.list_followers_for_user(username=self.user_name, per_page=self.page_items, page=self.page_number)
        following = await self.api.users.list_following_for_user(username=self.user_name, per_page=self.page_items, page=self.page_number)
        followers_set = {f.login for f in followers}
        following_set = {f.login for f in following}
        not_following_back = following_set - followers_set
        not_followed_back = followers_set - following_set
        mutual = followers_set & following_set
        print(f"\nMutual followers: {len(mutual)}")
        print(f"Not following back: {len(not_following_back)}")
        print(f"Not followed back: {len(not_followed_back)}")
        if not_following_back:
            print(f"\n@{self.user_name} follows them but they don't follow @{self.user_name}:")
            for user in list(not_following_back)[:10]:
                print(f"  @{user}")
        if not_followed_back:
            print(f"\nThey follow @{self.user_name} but @{self.user_name} doesn't follow them:")
            for user in list(not_followed_back)[:10]:
                print(f"  @{user}")

    async def user_repos(self):
        repos = await self.api.repos.list_for_user(username=self.user_name, per_page=self.page_items, page=self.page_number, sort="updated", direction="desc")
        print(f"\nRepositories of @{self.user_name} (page {self.page_number}):")
        for repo in repos:
            stars = repo.stargazers_count
            forks = repo.forks_count
            lang = repo.language if repo.language else "Unknown"
            print(f"  {repo.name} | Stars: {stars} | Forks: {forks} | Language: {lang}")
            print(f"     URL: {repo.html_url}")

    async def repo_info(self):
        _repo = await self.api.repos.get(owner=self.user_name, repo=self.repo_name)
        print(f"\nRepository: {_repo.full_name}")
        print(f"  Description: {_repo.description}")
        print(f"  Stars: {_repo.stargazers_count}")
        print(f"  Forks: {_repo.forks_count}")
        print(f"  Language: {_repo.language}")
        print(f"  Open Issues: {_repo.open_issues_count}")
        print(f"  Created: {_repo.created_at}")
        print(f"  Updated: {_repo.updated_at}")
        print(f"  URL: {_repo.html_url}")

    async def repo_languages(self):
        languages = await self.api.repos.list_languages(owner=self.user_name, repo=self.repo_name)
        total = sum(languages.values()) if languages else 0
        print(f"\nLanguages in {self.repo_name}:")
        if not languages:
            print("  No language data available.")
            return
        for lang, size in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            percent = (size / total) * 100 if total else 0
            print(f"  {lang}: {size} KB ({percent:.1f}%)")

    async def repo_contributors(self):
        contributors = await self.api.repos.list_contributors(owner=self.user_name, repo=self.repo_name, per_page=self.page_items, page=self.page_number)
        print(f"\nContributors of {self.repo_name} (page {self.page_number}):")
        for c in contributors:
            print(f"  @{c.login} - {c.contributions} contributions")

    async def commands(self):
        user_commands = {
            "info": self.information,
            "followers": self.user_followers,
            "followings": self.user_followings,
            "diff": self.compare,
            "repos": self.user_repos,
        }
        repo_commands = {
            "repo info": self.repo_info,
            "repo lang": self.repo_languages,
            "repo contributors": self.repo_contributors,
        }
        cmd = self.command.lower().strip()
        if cmd == "exit":
            print("Exiting ...")
            sys.exit()
        elif cmd == "help":
            print("""Available Commands:
info: Display general information about the GitHub user
followers: List followers of the user
followings: List users the user is following
diff: Compare followers and followings (mutual, not following back, not followed back)
repos: List repositories of the user
repo info: Display detailed information about a specific repository
repo lang: Show language breakdown of a specific repository
repo contributors: List contributors of a specific repository
exit: Exit the program

Usage Guide:
1. First enter your GitHub username and pagination settings when prompted
2. Use 'info' to see general profile information
3. Use 'followers' or 'followings' to list connections
4. Use 'diff' to analyze mutual and non-mutual connections
5. Use 'repos' to list your repositories
6. For repository-specific commands:
   repo info: shows details like stars, forks, issues, etc.
   repo lang: shows language usage percentages
   repo contributors: lists contributors with contribution counts
   Note: You will be asked to enter a repository name for repo commands

Note: All commands are case-insensitive. Type 'exit' to quit.
""")
        elif cmd in user_commands:
            await user_commands[cmd]()
        elif cmd in repo_commands:
            if not self.repo_name:
                self.repo_name = input("Enter the name of repository: ").strip()
                if not self.repo_name:
                    print("Repository name cannot be empty!")
                    return
            await repo_commands[cmd]()
        else:
            print(f"Invalid command: '{self.command}'")

async def main():
    print("GitHub_Analyzer: Created by Amir Mohammad Tavallali Nia!")

    try:
        app = GitHubAnalyzer()
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        sys.exit()

    while True:
        try:
            app.command = input("\nEnter command: ").strip().lower()
            await app.commands()
        except KeyboardInterrupt:
            print("\nExiting ...")
            sys.exit()
        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "404" in error_msg:
                print(f"User '{app.user_name}' not found!")
                print("Please check the username and try again.")
            elif "rate limit" in error_msg or "403" in error_msg:
                print("GitHub API rate limit exceeded!")
                print("Please wait a few minutes and try again.")
            elif "connection" in error_msg or "timeout" in error_msg:
                print("Network connection error!")
                print("Please check your internet connection.")
            elif "invalid" in error_msg:
                print(f"Invalid input: {e}")
            else:
                print(f"Unexpected error: {e}")
                print("Please try again.")

if __name__ == "__main__":
    asyncio.run(main())