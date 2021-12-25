
*Description*
This is a goofy personal project that automatically creates daily posts based on twitter hashtags and google image search results. The general idea is that a number of hashtags are setup in the backend and once a day, a script runs that uses the twitter search API to look for tweets containing the given hashtags. Then for each hashtag, the tweets for that hashtag are ranked in order of frequency and the winning tweet (after some modification) is used as the query for a google image search using the google custom search API. An image result is chosen at random from the top 100 results (if there are that many) and a post is created. 

*Powered By*
Python, Django, Heroku, Heroku-Postgres, Amazon S3, Git, Github 

*Dependencies*
- boto3==1.9.125
- Django==2.2.10
- python-twitter==3.5
- google-api-python-client==1.7.8
- psycopg2==2.7.7
- Pillow==8.4.0
- django-heroku==0.3.1
- django-storages==1.12.3
- gunicorn==20.1.0

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
	- The way I imagine this working is having an Instagram winner and a Twitter winner for every hashtag, and then potentially having a combined winner (prorate based on userbase?)
- Add support for special hashtags that are already taken by the application, e.g. admin and hashtags_all
	- I think I would just have a url regex like /special/(admin|hashtags_all|...) that then just loads the correct view. 