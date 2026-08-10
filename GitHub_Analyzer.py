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
            
        self.page_number = int(input("Enter number of items per page: "))
        self.number = int(input("Enter number of items to show: "))
        self.command = input("Enter your command (info/followers/followings/diff/exit): ")

    async def information(self):
        user = await self.api.users.get_by_username(self.user_name)
        print(f"\nInformation for @{self.user_name}")
        print(f"Followers: {user.followers}")
        print(f"Following: {user.following}")
        print(f"Name: {user.name}")
        print(f"Profile: {user.html_url}")

    async def user_followers(self):
        followers = await self.api.users.list_followers_for_user(
            username=self.user_name, 
            per_page=self.page_number
        )
        print(f"\nFirst {len(followers[:self.number])} followers:")
        for f in followers[:self.number]:
            print(f"  @{f.login}")

    async def user_followings(self):
        following = await self.api.users.list_following_for_user(
            username=self.user_name, 
            per_page=self.page_number
        )
        print(f"\nFirst {len(following[:self.number])} followings:")
        for f in following[:self.number]:
            print(f"  @{f.login}")

    async def compare(self):
        followers = await self.api.users.list_followers_for_user(
            username=self.user_name, 
            per_page=self.page_number
        )
        following = await self.api.users.list_following_for_user(
            username=self.user_name, 
            per_page=self.page_number
        )
        
        followers_set = {f.login for f in followers}
        following_set = {f.login for f in following}
        
        not_following_back = following_set - followers_set
        not_followed_back = followers_set - following_set
        mutual = followers_set & following_set
        
        print(f"\nMutual followers: {len(mutual)}")
        print(f"Not following back: {len(not_following_back)}")
        print(f"Not followed back: {len(not_followed_back)}")
        
        if not_following_back:
            print("\nYou follow them but they don't follow you:")
            for user in list(not_following_back)[:10]:
                print(f"  @{user}")
        
        if not_followed_back:
            print("\nThey follow you but you don't follow them:")
            for user in list(not_followed_back)[:10]:
                print(f"  @{user}")

    async def run_command(self):
        cmd = self.command.lower().strip()
        
        if cmd == "info":
            await self.information()
        elif cmd == "followers":
            await self.user_followers()
        elif cmd == "followings":
            await self.user_followings()
        elif cmd == "diff":
            await self.compare()
        elif cmd == "exit":
            print("Goodbye!")
            sys.exit()
        else:
            print(f"Invalid command: '{self.command}'")
            print("Valid commands: info, followers, followings, diff, exit")

async def main():
    print("GitHub_Analyzer: Created by Amir Mohammad Tavallali Nia!")
    app = GitHubAnalyzer()
    
    while True:
        try:
            await app.run_command()
            new_command = input("\nEnter command (info/followers/followings/diff/exit): ").strip()
            app.command = new_command
            
        except KeyboardInterrupt:
            print("\nProgram terminated!")
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
