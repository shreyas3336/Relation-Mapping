import tweepy
import csv
import json
import unicodedata

# load Twitter API credentials
countryinfo = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegowina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, the Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Cote d'Ivoire", 'Croatia (Hrvatska)', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'France Metropolitan', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard and Mc Donald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao, People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libyan Arab Jamahiriya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia, The Former Yugoslav Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia (Slovak Republic)', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'St. Helena', 'St. Pierre and Miquelon', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen Islands', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Virgin Islands (British)', 'Virgin Islands (U.S.)', 'Wallis and Futuna Islands', 'Western Sahara', 'Yemen', 'Yugoslavia', 'Zambia', 'Zimbabwe']
leader_handlers = ['realDonaldTrump','Pontifex','narendramodi','PMOIndia','POTUS','WhiteHouse','RT_Erdogan','SushmaSwaraj','jokowi','QueenRania','HHShkMohd','ImranKhanPTI','KingSalman','tcbestepe','10DowningStreet','StateDept','MedvedevRussia','lopezobrador_','mauriciomacri','rashtrapatibhvn','JustinTrudeau','ABZayed','RoyalFamily','EmmanuelMacron','KremlinRussia','NicolasMaduro','jairbolsonaro','AdelAljubeir','AlsisiOfficial','Elysee','MohamedBinZayed','sebastianpinera','KSAMOFA','SMQureshiPTI','MEAIndia','moonriver365','MBuhari','ArifAlvi','GOVUK','Presidencia_Ec','jaarreaza','saadhariri','m_ebrard','netanyahu','IndianDiplomacy','PaulKagame','TC_Disisleri','MevlutCavusoglu','NGRPresident']
consumer_key = 'fbSmYXE7x5N2nR8EAsEGF0hQq'
consumer_secret = 'SkjE6njcXvfYhKhN0MQzN6OTk1hlBAuZtyp2v20QMdwvDu5TDH'
access_key = '1863709004-UzHBCCOasESFpuMahynqILQLHhQbFVLvdGuwAdz'
access_secret = 'HE0325hGugzotmEZFKGNPNj4ncbQXAodhKinmMY1XhukJ'
tmp = []
def get_all_tweets(screen_name):

	# Twitter allows access to only 3240 tweets via this method
	# Authorization and initialization

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	# initialization of a list to hold all Tweets

	all_the_tweets = []

	# We will get the tweets with multiple requests of 200 tweets each

	new_tweets = api.user_timeline(screen_name=screen_name, count=200)

	# saving the most recent tweets

	all_the_tweets.extend(new_tweets)

	# save id of 1 less than the oldest tweet

	oldest_tweet = all_the_tweets[-1].id - 1

	# grabbing tweets till none are left

	while len(new_tweets):
		# The max_id param will be used subsequently to prevent duplicates
		new_tweets = api.user_timeline(screen_name=screen_name,
		count=200, max_id=oldest_tweet)

		# save most recent tweets

		all_the_tweets.extend(new_tweets)

		# id is updated to oldest tweet - 1 to keep track

		oldest_tweet = all_the_tweets[-1].id - 1
		print ('...%s tweets have been downloaded so far' % len(all_the_tweets))

		# transforming the tweets into a 2D array that will be used to populate the csv
		outtweets = [[tweet.id_str, tweet.created_at,
		unicodedata.normalize('NFKD',tweet.text).encode('ascii','ignore').decode('ascii')] for tweet in all_the_tweets]

		# writing to the csv file

		with open("Tweet_Data/"+screen_name + '_tweets.csv', 'w', encoding='utf8') as f:
			writer = csv.writer(f)
			writer.writerow(['id', 'created_at', 'text'])
			writer.writerows(outtweets)

if __name__ == '__main__':

	# Enter the twitter handle of the person concerned
	for i in leader_handlers:
		print('Tweet Extraction of @'+str(i))
		get_all_tweets(i)#input("Enter the twitter handle of the person whose tweets you want to download:- "))
