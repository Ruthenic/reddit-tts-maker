import praw
from praw.models import MoreComments
def getRedditPosts(subreddit, commentCount=100, postid=None):
    botinfo = open('id.txt').read().split("\n")
    reddit = praw.Reddit(
        client_id=botinfo[0],
        client_secret=botinfo[1],
        password=botinfo[2],
        username=botinfo[3],
        user_agent=botinfo[4]
    )
    commentCount += 1
    info = []
    if postid == None:
        for post in reddit.subreddit(subreddit).hot(limit=1):
            info.append(post.title)
            i=0
            for comment in post.comments:
                if isinstance(comment, MoreComments):
                    continue
                if i >= commentCount:
                    break
                if not comment.author == 'AutoModerator':
                    info.append({'User': comment.author, 'Content': comment.body})
                i+=1
    else:
        i=0
        info.append(reddit.submission(id=postid).title)
        for comment in reddit.submission(id=postid).comments:
            if isinstance(comment, MoreComments):
                continue
            if i >= commentCount:
                break
            if not comment.author == 'AutoModerator':
                info.append({'User': comment.author, 'Content': comment.body})
            i+=1
    print(info)
    return info
