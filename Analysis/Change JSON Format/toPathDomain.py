import sys, os 
import json
from bs4 import BeautifulSoup

def prettyJson(jsonString): 
	return json.dumps(jsonString, indent=4)

def main(): 

	correct_http_page = 'http\n'
	url_list = ["3.110.30.127", "18.133.196.172", "54.197.194.180", \
				"18.228.203.42", "50.18.245.54", "157.175.188.96", "13.244.77.102"]

	webpage_title_dic = {}
	with open('domain_title_dict_2021.txt', "r") as f:
		data = f.read().split("\n")
	for entry in data:
		if not entry: 
			continue
		entry_dic = json.loads(entry)
		domain = list(entry_dic.keys())[0]
		title = entry_dic[domain]
		webpage_title_dic[domain] = title

	with open('2022-08-06_http_proxyrack_censorship_attempt4.json', 'r') as f:
		lines = f.read().split("\n")

	for line in lines: 
		if not line: 
			continue
		data = json.loads(line)
		domain_list = data['domain'].keys()


		changed = {}
		changed["proxy country"] = data["proxy"]["country"]
		changed["proxy ip"] = data["proxy"]["query"]
		changed["server"] = {}
		for url in url_list: 
			changed["server"][url] = {}
			for domain in domain_list: 
				changed["server"][url][domain] = {}
		
		for domain in data['domain']:
			for url in url_list:
				response = data['domain'][domain][url]['text']

				try:
					correct_title = record_title[domain.lower()]
				except:
					correct_title = ""

				if response == correct_http_page:
					changed["server"][url][domain] = "no censorship - correct http"
				else:
					try:
						title = BeautifulSoup(response, "html.parser").title.string
						if title == correct_title and correct_title != '':
							changed["server"][url][domain] =  "no censorship - correct title"
						else:			
							changed["server"][url][domain] =  "detect censorship - wrong title"		
					except:
						changed["server"][url][domain] =  "detect censorship - wrong http"
		print(prettyJson(changed))

	return 0 

if __name__ == '__main__':
	main()