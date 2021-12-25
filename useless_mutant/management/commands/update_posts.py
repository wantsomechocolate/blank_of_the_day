from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = "This command doesn't take any arguments. It loops through all the ACTIVE hashtags and tries to create a post for it"
    def handle(self, *args, **options):

        ## Standard
        import random, datetime, os
        from datetime import datetime, timezone
        from io import BytesIO
        from urllib.request import urlretrieve
        from collections import Counter

        ## From the project
        import useless_mutant.useless_module as um
        from useless_mutant.models import Post, Hashtag

        ## Pillow
        from PIL import Image
        
        ## Django
        from django.core.files.uploadedfile import InMemoryUploadedFile

        ## Error handling
        from urllib.error import HTTPError, URLError
        from PIL import UnidentifiedImageError


        MAX_NUM_RESULT = 100

        ## Get all active hashtags and loop through them to try and create a post
        active_hashtags = Hashtag.objects.filter(enabled = True)

        for hashtag in active_hashtags:

            self.stdout.write("Starting to create a post for "+str(hashtag.name))

            c = um.tally_twitter_votes(hashtag.name)
            # If there are no votes than don't create a post!
            if c == Counter():
                self.stdout.write("There are no votes to create a post")
                self.stdout.write("")
                self.stdout.write("")
                continue

            most_popular_tuple = c.most_common(1)[0]
            most_popular_vote = most_popular_tuple[0]
            most_popular_count= most_popular_tuple[1]

            if most_popular_count == 1:
                self.stdout.write("No one rose above the rest")
                self.stdout.write("")
                self.stdout.write("")
                continue

            q_raw=most_popular_vote

            self.stdout.write("The raw tweet text is: "+str(q_raw))

            ## remove urls
            pattern = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'
            matches = re.finditer(pattern,q_raw)
            for match in matches:
                q_raw = q_raw.replace(match.group()," ")

            self.stdout.write("The tweet without links is: "+str(q_raw))

            ## Remove special characters
            remove_list=r"""@#$%^&*()[]{}"'\/?<>‘’|:;.,~`"""
            for char in remove_list:
                q = q_raw.replace(char," ")

            ## remove newlines and whitespace
            q = " ".join(q.split())

            self.stdout.write("The search text is: "+str(q))

            ## Can I import the value of MAX_NUM_RESULT to this sheet?
            i = random.randrange(0,MAX_NUM_RESULT)

            link_info = um.google_image_search(q,i)

            if 'error' in link_info.keys():
                self.stdout.write("The search query did not return any results")
                self.stdout.write("")
                self.stdout.write("")
                continue

            img_link=link_info['link']

            h, h_created_tf = Hashtag.objects.get_or_create(name = hashtag.name)

            if not h_created_tf:
                h.last_post_added_time=datetime.now(timezone.utc)
                #datetime.datetime.utcnow()


            self.stdout.write("The query returned this link: "+str(img_link))

            
            ## Try to get the url as a file. Sometimes this randomly failes so try three times.
            attempts=0
            success = False
            while attempts<3:
                try:
                    response = urlretrieve(img_link) #returns  tuple with a file object and header info
                    success = True
                    break
                except HTTPError: 
                    attempts+=1
                    self.stdout.write("Error trying to open the link, attempt: "+str(attempts))
                except URLError:
                    attempts+=1
                    self.stdout.write("Error trying to open the link, attempt: "+str(attempts))

            if success == False:
                self.stdout.write("Reading the link in as an image failed, moving on")
                self.stdout.write("")
                self.stdout.write("")
                continue


            ## Come up with a name for the file
            created_at = datetime.now(timezone.utc)
            time_string = datetime.strftime(created_at,"%Y%m%d%H%M%S%f")
            filename = "{}-{}.{}".format(hashtag,time_string,'png')
            #filename = os.path.join(hashtag.name,filename)


            ## Try to open in pillow and convert to a png
            try:
                img = Image.open(response[0])
            except UnidentifiedImageError:
                self.stdout.write("Pillow raised an unidentified Image Error, moving on")
                self.stdout.write("")
                self.stdout.write("")
                continue               

            #create an in memory place for the png version to go
            f = BytesIO()
            img.save(f,format='PNG')

            #Convert to something Django can sve
            image = InMemoryUploadedFile(f, None, filename, 'image/png', f.tell(), None)

            p = Post(	search_query 		        =	q 					 ,
                        search_query_raw            =   q_raw                , 
                        search_query_raw_with_links	=	most_popular_vote	 , 
                        link 				        = 	img_link			 ,
                        image                       =   image                , 
                        votes 				        = 	most_popular_count   , 
                        hashtag 			        = 	h 					 ,
                        created_at			        =	created_at           , 	)

            h.save()
            p.save()
            
            self.stdout.write("Successfully created a post, I think.")
            self.stdout.write("")
            self.stdout.write("")

