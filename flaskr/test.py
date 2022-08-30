
import re

test_url = 'https://www.youtube.com/embed/wiwKlTalWg8'


def youtube_url_parser(url):
    regExp = '^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*'
    match = re.match(regExp, url)
    return match

print(youtube_url_parser(test_url)[7])
