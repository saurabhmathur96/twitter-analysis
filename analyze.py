import tweepy
import sys
import re
import csv

def get_api():
    '''authorization'''
    with open('config') as f:
        api_key = f.readline().strip()
        api_secret = f.readline().strip()
        access_token = f.readline().strip()
        access_token_secret = f.readline().strip()
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
    return auth

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        super(CustomStreamListener, self).__init__(*args,**kwargs)
        self.count = 0
        self.hashtag = r'#\w+'
        self.freq = dict()
        
    def on_status(self, status):
        print 'tweet!'
        self.count += 1
        if '#' in status.text :
            print status.text
            tags = re.findall(self.hashtag, status.text)
            for tag in tags :
                if tag not in self.freq :
                   self.freq[tag] = 1
                else :
                    self.freq[tag] += 1
        print self.freq
    def on_error(self, status_code):
        print >> sys.stderr, 'error ' + str(status_code)
        return True
    def on_timeout(self):
        print >> sys.stderr, 'timeout...'
        return True

def write_dict_to_csv(data):
    with open('datafile.csv','wb') as f:
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)

def main():
    
    if len(sys.argv) != 2:
        print 'error: usage python analyze.py [topic]'
    else:
        topic = sys.argv[1]
        
        csl = CustomStreamListener()
        try:
            auth = get_api()
            streaming_api = tweepy.Stream(auth, csl)
            streaming_api.filter(track=[topic])
        except KeyboardInterrupt:
            print '-'*4 + 'TOTAL TWEETS' + '-'*4
            print csl.count
            print '-'*20
            write_dict_to_csv(csl.freq)
if __name__ == "__main__":
    main()
