from pprint import pprint
from bs4 import BeautifulSoup
import re
from nltk.tokenize import WordPunctTokenizer
import os
import joblib
import pandas as pd

country_leaders = {'United States':['realDonaldTrump','POTUS','WhiteHouse','StateDept'], 'Vatican':['Pontifex'], 'India':['narendramodi','PMOIndia','SushmaSwaraj','rashtrapatibhvn','MEAIndia','IndianDiplomacy'], 'Turkey':['RT_Erdogan','tcbestepe','TC_Disisleri','MevlutCavusoglu'], 'Indonesia':['jokowi'], 'Jordan':['QueenRania'], 'United Arab Emirates': ['HHShkMohd','ABZayed','MohamedBinZayed'], 'Pakistan':['ImranKhanPTI','SMQureshiPTI','ArifAlvi'], 'Saudi Arabia':['KingSalman','AdelAljubeir','KSAMOFA'], 'United Kingdom':['GOVUK','10DowningStreet','RoyalFamily'], 'Russia': ['MedvedevRussia', 'KremlinRussia'], 'Mexico':['lopezobrador_','m_ebrard'], 'Argentina':['mauriciomacri'], 'Canada':['JustinTrudeau'], 'France':['EmmanuelMacron', 'Elysee'], 'Venezuela':['NicolasMaduro','jaarreaza'], 'Brazil': ['jairbolsonaro'], 'Egypt':['AlsisiOfficial'], 'Chile':['sebastianpinera'], 'South Korea': ['moonriver365'], 'Nigeria': ['MBuhari','NGRPresident'], 'Ecuador':['Presidencia_Ec'], 'Lebanon':['saadhariri'], 'Israel':['netanyahu'], 'Rwanda': ['PaulKagame']}
countryinfo = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegowina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, the Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Cote d'Ivoire", 'Croatia (Hrvatska)', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'France Metropolitan', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard and Mc Donald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao, People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libyan Arab Jamahiriya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia, The Former Yugoslav Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia (Slovak Republic)', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'St. Helena', 'St. Pierre and Miquelon', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen Islands', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Virgin Islands (British)', 'Virgin Islands (U.S.)', 'Wallis and Futuna Islands', 'Western Sahara', 'Yemen', 'Yugoslavia', 'Zambia', 'Zimbabwe']
BASE_PATH = 'Tweet_Data/'
EXT = '_tweets.csv'
MODEL_DIR = "models"

#Importing Pre-Trined Model
if os.path.exists(os.path.join(MODEL_DIR,'model.pkl')):
    sentiment_pipeline = joblib.load(os.path.join(MODEL_DIR,'model.pkl'))
else:
    print("Model Not Found")


#Cleaning the tweet text
tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))
def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()


for i in country_leaders.keys():
	final = {}
	print('Mapping Relations of',i)
	for j in country_leaders[i]:
		tweet_file = os.path.join(BASE_PATH,j+EXT)
		names = ('id', 'created_at', 'text')
		df = pd.read_csv(tweet_file, encoding='latin1', names=names)
		for t in df['text']:
			for x in range(len(countryinfo)):
				if type(countryinfo[x]) == type(t) and countryinfo[x] in t:
					stmt = tweet_cleaner(t)
					val = int(sentiment_pipeline.predict([stmt]))
					if countryinfo[x] not in final:
						final[countryinfo[x]] = val
					else:
						final[countryinfo[x]]+=val
	pprint(final)