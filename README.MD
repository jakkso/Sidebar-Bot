## Sidebar Bot

Scrapes CBS's and NFL websites for upcoming NFL games, current team standings and uses the Twitter API to look for links to 
that week's air schedule on the AFN network, then uses that info to update a subreddit's sidebar.

#### Installation
Clone the repo<br>
Requires: PRAW, Requests, BS4 and python-twitter

Install them all via `pip3 install praw requests beautifulsoup4 python-twitter  ` 

It's coded for python3.6+ and probably won't work with python2


### Usage

The bot is hardcoded to be used only with a specific subreddit, though altering it to be used with another subreddit
would be trivially easy.  I wrote it to gain programming experience and to help out a fellow redditor.