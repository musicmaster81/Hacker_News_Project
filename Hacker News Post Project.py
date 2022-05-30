# As we mentioned in the project description, our goal is to answer the following 2 questions:
# 1: Do posts asking questions or imparting information garner the most comments?
# 2: Is there an optimal time for posts to be created to have the best chance of receiving more comments?
# To do this, we examine a data set of posts from the Hacker News website in 2016.

# First, we import our required modules.
from csv import reader
import datetime as dt

# Next, we define the path of our dataset on our computer.
path = r'C:\Python\Data Sets\Hacker News 2016.csv'

# We then read our dataset into a list of lists.
file = open(path, encoding='Latin-1')
read_file = reader(file)
hn = list(read_file)

# Let's isolate our header row, then remove it from our dataset since it won't provide pertinent info for analysis.
headers = hn[0]
hn = hn[1:]

# We then instantiate empty lists for the 2 types we wish to analyze and single empty lists for all other types.
ask_posts = []
show_posts = []
other_posts = []

# We then iterate through each post in our data set to place them into our list "buckets".
for row in hn:
    title = row[1]
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)

# We now loop through each list that stores either a post asking a question or a post imparting information.
total_ask_comments = 0
for row in ask_posts:  # Looping through the list containing question related posts.
    num_comments = int(row[4])
    total_ask_comments += num_comments
total_ask_posts = len(ask_posts)
avg_ask_comments = total_ask_comments/total_ask_posts
print('Average number of comments for question posts:', avg_ask_comments)

total_show_comments = 0
for row in show_posts:  # Looping through the list containing informational posts.
    num_comments = int(row[4])
    total_show_comments += num_comments
total_show_posts = len(show_posts)
avg_show_posts = total_show_comments/total_show_posts
print('Average number of comments for informational posts:', avg_show_posts)

# We can see from our analysis that posts asking a question receive well over double the amount of comments on average
# than posts imparting information. This suggests that people use the Hacker News website to ask a lot of questions.

# The second question we wish to answer is at what time do posts garner the most comments on average?
result_list = []  # First, we create an empty list to hold our answers.
for row in ask_posts:  # We then loop through our list to isolate the post time and the number of comments.
    created_at = row[6]
    num_comments = int(row[4])
    result_list.append([created_at, num_comments])  # We then add our findings to the list.

# We now instantiate two empty dictionaries to hold key, value pairs, obviously.
counts_by_hour = {}
comments_by_hour = {}  # Keys are the hours, values are the number of comments.
date_format = '%m/%d/%Y %H:%M'

for row in result_list:
    date_str = row[0]
    num_comments = row[1]
    hour = dt.datetime.strptime(date_str, date_format).strftime('%H')
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = num_comments
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += num_comments

# Let's see what our dictionary looks like.
print(comments_by_hour)

# Now we are getting somewhere. While this is good information, it is very unordered. Let's instead resort to computing
# the averages for the amount of comments per hours.
avg_by_hour = []
for hour in counts_by_hour:
    avg_by_hour.append([hour, comments_by_hour[hour]/counts_by_hour[hour]])
print(avg_by_hour)

# Let's instead place the averages first.
swap_avg_by_hour = []
for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
print(swap_avg_by_hour)

# Lastly, let's select the top 5 hours that have the most comments.
sorted_swaps = sorted(swap_avg_by_hour, reverse=True)

print("Top 5 Hours for Ask Posts Comments")
for average, hour in sorted_swaps[:5]:
    print("{}: {:.2f} average comments per post.".format(hour, average))

# The answer to our second query is that posts in the afternoon, specifically 3pm EST.
