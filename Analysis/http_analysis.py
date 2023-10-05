import json
from nturl2path import url2pathname
from weakref import proxy
from bs4 import BeautifulSoup



url_list = ["", "", "", "", "", "", ""]
correct_http_page = 'http\n'


with open('', 'r') as f:
    line = f.readline()
    country_count = {}
    suspicious_vps = {}
    suspicious_country_count = {}
    
    while line is not None and line != '':
        data = json.loads(line)
        
        
        
        country = data['proxy']['country']
        if country not in country_count.keys():
            country_count[country]=1
        else:
            country_count[country]=country_count[country]+1
                    

        # for domain in data['domain']:
        #     if domain is None and domain == '':
        #         continue
        #     else:
        #         for url in url_list:
        #             vp_response = data['domain'][domain][url]['text']
                    
        #             if vp_response == correct_http_page:
        #                 data['domain'][domain][url] = "no censorship"
                        
        #             else:
        #                 data['domain'][domain][url] = "detect censorship"
        webpage_title_dic = dict()
        with open('') as file:
            for entry in file:
                entry_dic = json.loads(entry.strip())
                domain = list(entry_dic.keys())[0]
                title = entry_dic[domain]
                webpage_title_dic[domain] = title

        for domain in data['domain']:           
            for url in url_list:
                vp_response = data['domain'][domain][url]['text']

                if vp_response == correct_http_page:
                    data['domain'][domain][url] = "no censorship - correct http"
                        
                else:
                    while True:
                    try:

                        vp_title = BeautifulSoup(vp_response, "html.parser").title.string
                        local_title = webpage_title_dic[domain]
                        if vp_title == local_title and local_title != '':
                            data['domain'][domain][url] = "no censorship - correct title"
                        else:
                            
                            data['domain'][domain][url] = "detect censorship - wrong title"
                            break
                    except:
                        data['domain'][domain][url] = "detect censorship - wrong http"
                        

                    
                
        suspicious_vps = {"proxy": data['proxy']['country'], "query": data['proxy']['query'], "domain": data['domain']}
        
        
        
        # tmp = suspicious_vps.copy()           
        for domain in suspicious_vps['domain'].copy():
            Delete = True
            for i in range(5):
                
                # if suspicious_vps['domain'][domain][url] not in url_list:
                #     suspicious_vps['domain'][domain][url] = {}
                # print(suspicious_vps['domain'][domain][url_list[i]])
                # print(suspicious_vps['domain'][domain][url_list[i+1]])
                if suspicious_vps['domain'][domain][url_list[i]] != suspicious_vps['domain'][domain][url_list[i+1]]:
                    Delete = False
                
            if Delete == True:
                suspicious_vps["domain"].pop(domain)
                # del suspicious_vps['domain'][domain]
                
                    
        
        if len(suspicious_vps["domain"]) != 0:
            country = suspicious_vps['proxy']
            if country not in suspicious_country_count.keys():
                suspicious_country_count[country]=1
            else:
                suspicious_country_count[country]=suspicious_country_count[country]+1
                        

                        
        # print(json.dumps(country_count, indent=4))      
        # print(json.dumps(suspicious_country_count, indent=4))      
        line = f.readline()
        print(json.dumps(suspicious_vps, indent=4))
