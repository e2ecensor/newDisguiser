import sys, os 
import json

def prettyJson(jsonString): 
	return json.dumps(jsonString, indent=4)

def main(): 
	with open("http_overall.txt", "r") as f:
		lines = f.read().split("\n")
	
	domainlist = {}
	for line in lines: 
		if not line:
			continue
		data = json.loads(line)
		country = data["country"]
		domains = data["domain"]
		for domain in domains: 
			if domain not in domainlist.keys(): 
				domainlist[domain] = []
			domainlist[domain].append(country)

	with open("allDomain.txt", "w") as f: 
		f.write(prettyJson(domainlist))
	return 0 

if __name__ == '__main__':
	main()