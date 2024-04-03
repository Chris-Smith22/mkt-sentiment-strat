# Process Description
This document outlines the internal processes and resources used to access and use the Reddit API


**App Creation and API Access**
To access the Reddit API, you must follow a sequence of steps: 
1. On the [Reddit app website](https://www.reddit.com/prefs/apps), click on the "are you a developer? Create an app..." button. 
2. Create a name for the app, select "script", add a description, and input values into "about url" and "redirect uri" fields. 
3. Once the app is created, you will be redirected to a “Developed Applications” page. A client ID will be displayed in the top left corner and a secret key will appear. Keep track of these values. 
4. Register app with Reddit by [submitting a ticket](https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id=14868593862164)
5. Fill in appropriate fields. Make sure to select the "I'm a Developer" and "I want to register to use the Reddit API" fields. 
6. The Reddit API can now be accessed in code by using the praw.Reddit() command with fields client_id (from step 3), client_secret (secret key from step 3) and user_agent (username the app is under)


***Useful links / resources***
- [Sample Project](https://github.com/tstewart161/Reddit_Sentiment_Trader)
- [Sample Project Description](https://www.reddit.com/r/algotrading/comments/nyi94x/i_made_an_algo_that_tracks_sentiment_on_reddit/)

