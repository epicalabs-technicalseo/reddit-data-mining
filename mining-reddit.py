import praw
import csv
import datetime

# Create an app: https://www.reddit.com/prefs/apps
# Use http://localhost:8080 as redirect uri
username = "epicalabs"
password = "xxxxxxxxxxx"
clientid = "AqaUpWUKY5yF2w"
clientsecret = "xxxxxxxxxxxxxxxxxxxx"


def writeheaders():
    f.writerow(["Number", "Keyword", "Title", "Score", "Comments", "URL", "Domain", "Permalink", "ID", "Subreddit",
                "CreatedDate"])


def writefields():
    f.writerow([startNum, search.strip(), submission.title,
                submission.score, submission.num_comments,
                submission.url, submission.domain, submission.permalink, submission.id,
                submission.subreddit, datetime.datetime.utcfromtimestamp(submission.created).strftime('%m-%d-%Y')])


reddit = praw.Reddit(client_id=clientid,
                     client_secret=clientsecret,
                     password=password,
                     user_agent='Reddit search data extractor by /u/' + username + '',
                     username=username)

print("Authentication for " + str(reddit.user.me()) + " is verified. Proceeding.\r\n")

outfilename = input("Enter a CSV filename to output the data to (e.g., reddit-data.csv)\r\n")
search = input("Enter a search (e.g., 'how do you') or multiple searches delimited with commas:\r\n")
sortsub = input("How do you want to sort results? Enter relevance, hot, top, new, or comments.\r\n")
filtersub = input("Do you want to restrict to a certain subreddit? Enter 'Yes' or 'No'.\r\n")

search_list = search.split(',')

if (filtersub.lower() == "yes"):
    subreddit = input("Enter the subreddit names delimited with commas (i.e., BigSEO):\r\n")
    subreddit_list = subreddit.split(',')
    file = open(outfilename, "w+", newline="\n", encoding="utf-8")
    f = csv.writer(file)
    writeheaders()
    for subs in subreddit_list:
        for search in search_list:
            startNum = 0
            for submission in reddit.subreddit(subs.strip()).search(search, sort=sortsub):
                startNum += 1
                writefields()
            print("Writing out posts results for the search '" + search.strip() + "' in 'r/" + subs.strip() + "'\r\n")
        file.close
else:
    file = open(outfilename, "w+", newline="\n", encoding="utf-8")
    f = csv.writer(file)
    writeheaders()
    for search in search_list:
        startNum = 0
        for submission in reddit.subreddit('all').search(search.lower(), sort=sortsub):
            startNum += 1
            writefields()
        print("Writing out posts results for the search '" + search.strip() + "' in 'r/all'\r\n")
    file.close
