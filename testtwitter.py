import snscrape.modules.twitter as sntwitter
from openpyxl import Workbook,load_workbook

wb = Workbook()
ws = wb.active
ws.title = "Sheet1"
ws.append(["username","Content", "Location","id","Attached Link"])

maxTweets =1000
keyword = 'putin'

for i,tweet in enumerate(sntwitter.TwitterSearchScraper('ukraine since:2023-02-01 until:2023-02-02 lang:"en" ').get_items()):
    if i>maxTweets:
        break
    # print(ascii(tweet.rawContent))
    if "https" in ascii(tweet.rawContent):
        splittweet = ascii(tweet.rawContent).split("https")
        # print(splittweet[1])
        
        link = "https" + splittweet[1][:16]
        print(link)
        print("--------------------------------------------")
        ws.append([tweet.user.username,tweet.rawContent,tweet.user.location, tweet.id,link])
wb.save("TweetExcel.xlsx")