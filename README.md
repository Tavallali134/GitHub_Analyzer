# GitHub_Analyzer: Created by Amir Mohammad Tavallali Nia!

You can refer to this link to see my games and apps:
https://t.me/A_M_T_N134

GitHub Follower Analyzer

A command-line tool to fetch and analyze GitHub followers and following data.

## What it does

This tool connects to the GitHub API and retrieves follower and following information for a given username. It allows you to view follower lists, following lists, and compare them to find mutual followers or identify who doesn't follow you back.

# How it works

The program uses the ghapi library to interact with GitHub's REST API. After entering a username, you can run different commands to view specific information. All API calls are handled asynchronously for better performance.

# How to run

1. Install the required library:
pip install ghapi

2. Run the program:
python github_analyzer.py

3. Follow the prompts to enter a username and commands.

# Commands

info: Display user profile information
followers: List followers
followings: List followings
diff: Compare followers and followings
exit: Exit the program
