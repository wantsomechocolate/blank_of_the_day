from apiclient.discovery import build
import os

api_key = os.environ['USELESSMUTANT_APIKEY']
service = build('customsearch','v1', developerKey = api_key)

res = service.cse().list(q='cat',cx=os.environ['USELESSMUTANT_CX'], searchType='image', num=1, imgType='clipart', fileType='png',safe='high')
res_ex = res.execute()

img_link=res_ex['items'][0]['link']

print (img_link)
