import sys, os 
import json

def main(): 
	with open("allDomain.txt", "r") as f: 
		data = f.read()

	domainJson = json.loads(data)
	domainList = domainJson.keys()
	
	for domain in domainList:
		print(domain)

	return 0 

if __name__ == '__main__':
	main()