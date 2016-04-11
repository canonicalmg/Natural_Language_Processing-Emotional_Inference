import zlib
import re
from twython import Twython
from properties import APP_SECRET

APP_KEY = 'xpaIs2y73iJGzRftnMQalSFNV'
#APP_SECRET = 'secret key'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

#________________________________________________________________
#test

def populateDBTwitter(file,searchTerm): #scrape tweets and write them to text file
	search = twitter.search(q=searchTerm+" -Retweet -RT -ReTweet",   #**supply whatever query you want here**
                  count=100)
	tweets = search['statuses']
	fh = open(file, "a")

	for tweet in tweets:
		tweetID = tweet['id_str'].encode('utf-8')
		tweet = tweet['text'].encode('utf-8')
		if not "http" in tweet:
			if not searchText(tweetID, file):
				tweet = tweet.replace('\n','')
				tweet = tweet.replace('\t','')
				if "@" in tweet:
					try:
						tweet = re.sub('@\w*', '', tweet)
					except Exception as err:
						print err
					#else:
						#
					#finally:
						#
				fh.writelines([tweetID, " -&- ", tweet, "\n"])
		
	fh.close()

	
def searchText(textID, file):	#make sure tweet ID isn't found more than once
	f = open(file, 'r')
	lines = f.read()
	answer = lines.find(textID)
	if answer == -1:
		return False
	else:	
		return True
	
def getString(file): #compiles text file into compressable string
	returnString = ""
	with open(file, 'r') as inF:
		for line in inF:
			try:
				returnString += line.split("-&-")[1]
			except:
				1==1 #redundant boolean. Try needs the except clause
	return returnString
	
def findEmotion(arbString, happyString, sadString, scaredString):

	emotionStrings = [{'name':"happy", 'val':happyString},{'name':"sad", 'val':sadString},{'name':"Scared", 'val':scaredString}]
	newEmotionStrings = []
	arbStrings = []
	compressedArbStrings = []
	compressedStrings = []
	arbDiffEmotions = []
	minObj = {'name':"indeterminate", 'val':0}
	minLength = len(min(emotionStrings))
	print "minLength = ", minLength
	for emotion in emotionStrings:
		#print emotion
		newEmotionString = (emotion['val'][0:minLength])
		newEmotionStrings.append(newEmotionString)

		arbStringToAppend = (emotion['val'][0:minLength] + arbString)
		arbStrings.append(arbStringToAppend)

		compressedArbString = (zlib.compress((emotion['val'][0:minLength] + arbString)))
		compressedArbStrings.append(compressedArbString)

		compressedString = (zlib.compress(emotion['val'][0:minLength]))
		compressedStrings.append(compressedString)

		arbDiffEmotion = (len(compressedArbString) - len(compressedString))
		#arbDiffEmotion = (len((zlib.compress((emotion['val'][0:minLength] + arbString)))) - len((zlib.compress(emotion['val'][0:minLength]))))
		arbDiffEmotions.append({'name':emotion['name'], 'val':arbDiffEmotion})
		if arbDiffEmotion > minObj['val']:
			minObj['val'] = arbDiffEmotion
			minObj['name'] = emotion['name']
		#print arbDiffEmotion
	print "emotion =", newEmotionStrings
	emotionStrings = newEmotionStrings
	print "arbStrings =", arbStrings

	print "minEmotion = ", minObj

	
	minLength = min(len(happyString), len(sadString), len(scaredString))
	happyString = happyString[0:minLength]
	sadString = sadString[0:minLength]
	scaredString = scaredString[0:minLength]
	
	print "minLength = ", minLength
	
	arbStringHappy = happyString + arbString
	arbStringSad = sadString + arbString
	arbStringScared = scaredString + arbString
	
	compressedArbHappy = zlib.compress(arbStringHappy)
	compressedArbSad = zlib.compress(arbStringSad)
	compressedArbScared = zlib.compress(arbStringScared)
	
	compressedHappy = zlib.compress(happyString)
	compressedSad = zlib.compress(sadString)
	compressedScared = zlib.compress(scaredString)
	
	arbDiffHappy = len(compressedArbHappy) - len(compressedHappy)
	arbDiffSad = len(compressedArbSad) - len(compressedSad)
	arbDiffScared = len(compressedArbScared) - len(compressedScared)
	
	print "Uncompressed =", len(arbString)
	print "Happiness =", arbDiffHappy
	print "Sadness =", arbDiffSad
	print "Scaredness =", arbDiffScared

	minEmotion = min(arbDiffHappy, arbDiffSad, arbDiffScared)
	if(arbDiffSad == arbDiffHappy == arbDiffScared):
		print arbString, "is indeterminate"
	elif(minEmotion == arbDiffSad):
		print arbString, "is a SAD phrase"
	elif(minEmotion == arbDiffScared):
		print arbString, "is a SSCARED phrase"
	elif(minEmotion == arbDiffHappy):
		print arbString, "is a HAPPY phrase"
		
		
def findEmotionRelative(arbString, happyString, sadString):
	minLength = min(len(happyString), len(sadString))
	happyString = happyString[0:minLength]
	sadString = sadString[0:minLength]
	
	print "minLength = ", minLength
	
	arbStringHappy = happyString + arbString
	arbStringSad = sadString + arbString
	
	compressedArbHappy = zlib.compress(arbStringHappy)
	compressedArbSad = zlib.compress(arbStringSad)
	
	compressedHappy = zlib.compress(happyString)
	compressedSad = zlib.compress(sadString)
	
	arbDiffHappy = len(compressedArbHappy) - len(compressedHappy) + 1
	arbDiffSad = len(compressedArbSad) - len(compressedSad) + 1
	
	print "Uncompressed =", len(arbString)
	print "Happiness =", arbDiffHappy
	print "Sadness =", arbDiffSad
	
	if(arbDiffHappy > arbDiffSad):
		print arbString, "is a SAD phrase"
	elif (arbDiffSad > arbDiffHappy):
		print arbString, "is a HAPPY phrase"	
	elif(arbDiffSad == arbDiffHappy):
		print arbString, "is indeterminate"
		
	arbHappyRelative = (float(len(arbString)) / float(arbDiffHappy)) * 100
	arbSadRelative = (float(len(arbString)) / float(arbDiffSad)) * 100
	print "Happy relative = ", arbHappyRelative, "%"
	print "Sad relative = ", arbSadRelative, "%"
	relativeArr = [arbHappyRelative, arbSadRelative]
	return relativeArr

def QueryEachWord(arbString):
	arbString = arbString.split(" ")
	percentArray = []
	for word in arbString:
		print "QUERY ON ", word
		percentArray.append(QueryRelative(word))
		print "__________"
		
	happy = 0
	sad = 0
	
	for word in percentArray:
		happy += word[0]
		sad += word[1]
		
	print "OVERALL HAPPY = ", happy
	print "OVERALL SAD = ", sad
	
def removeDupes():
	lines_seen = set() # holds lines already seen
	outfile = open('Happy.txt', "w")
	for line in open('Happy.txt', "r"):
		if line not in lines_seen: # not a duplicate
			outfile.write(line)
			lines_seen.add(line)
	outfile.close()

	lines_seen = set() # holds lines already seen
	outfile = open('Sad.txt', "w")
	for line in open('Sad.txt', "r"):
		if line not in lines_seen: # not a duplicate
			outfile.write(line)
			lines_seen.add(line)
	outfile.close()

def QueryRelative(arbString):
	return findEmotionRelative(arbString, happinessString, sadnessString)
			
def Query(arbString):
	#removeDupes()
	findEmotion(arbString, happinessString, sadnessString, scaredString)

populateDBTwitter("Happy.txt","#great") #happy, happiness, joy, fantastic, great
populateDBTwitter("Sad.txt","#terrible") #sad, sadness, depressed, unhappy, terrible
populateDBTwitter("Fear.txt", "#scared")

happinessString = getString("Happy.txt")
sadnessString = getString("Sad.txt")
scaredString = getString("Fear.txt")

print "Size of happy = ", len(happinessString)
print "Size of sad = ", len(sadnessString)
print "Size of scared =", len(scaredString)
#findEmotion("what a great day to be alive", happinessString, sadnessString)
