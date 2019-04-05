
*Description*
This is a goofy personal project that automatically creates daily posts based on twitter hashtags and google image search results. The general idea is that a number of hashtags are setup in the backend and once a day, a script runs that uses the twitter search API to look for tweets containing the given hashtags. Then for each hashtag, the tweets for that hashtag are modified to remove everything after the first hashtag and also remove the beginning of the tweet if it was a retweet. The tweets are then ranked in order of frequency and the winning text is used as the query for a google image search using the google custom search API. An image result is chosen at random from the top 100 results and a post is created. The most voted #example of the day is: 'tweet text' ::image::. 

*Powered By*
This project uses Python as the scripting language, Django as the templating framework, Heroku as the hosting platform, Heroku-Postgres and Amazon Simple Storage Service as the storage utilities, Git and Github as the versioning utilities. 

*To Do List*
- Obviously I should write some tests for this application. 
- Get logging working
- Get emails working when 500 and 404 errors occur (or go straight to something like Sentry)
- Update Procfile to have a release item that migrates the db because right now I have to manually migrate when deploying the app with a fresh database. 
- Remove uncessary static files and media files that were part of development. 
- Remove anything related to celery as it is not being used for this relatively simple application. 


*Future Development*
- Include other sources of social media in the voting process. 
	- Consider adding in Instagram for example
	- They I imagine this working is having an Instagram winner and a Twitter winner for every hashtag, and then potentially having a combined winner (prorate based on userbase?)
- Add support for special hashtags that are already taken by the application, e.g. admin and hashtags_all
	- I think I would just have a url regex like /special/(admin|hashtags_all|...) then then just loads the correct view. 
