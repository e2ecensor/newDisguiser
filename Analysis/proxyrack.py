from http import server
import os
from sqlite3 import Timestamp
import sys
import json
import random
from multiprocessing.pool import ThreadPool
from urllib import response
import requests
import time
import socket
import socks
import dns.query
import dns.message
import dns.name
import dns.rdatatype
import ssl
import base64
import struct
import random
from io import BytesIO
from proxy_request import proxy_http
import urllib.parse
import os
import ipaddress
import random
import datetime

import joblib
import proxy_request


def read_domain(file):
    """
    read domain info from plain file
    args:
        file: str. full file path or relevant file path
    returns:
        dict
    raises:
        None
    """
    with open(file, "r") as f:
        data = []
        for r in f.readlines():
            # skip empty lines
            Disallowed_chars = ["(", ")", "#", ";"]
            if r == "\n":
                continue
            for x in r:
                if x in Disallowed_chars:
                    exit()
            r = r.replace("false", "False")
            r = r.replace("true", "True")
            try:
                # convert string to dictionary
                data.append(json.loads(r))
            except Exception as e:
                print(e)
    return data

def unpack_proxy_args(proxy):
    proxy_address = proxy['proxy_address']
    proxy_port = proxy['proxy_port']
    username = proxy['username']
    password = proxy['password']
    return proxy_address, proxy_port, username, password

def get_curl_cmd(proxy, url):
    proxy_address, proxy_port, username, password = unpack_proxy_args(proxy)
    Disallowed_chars = ["(", ")", "#", ";"]
    for x in proxy_address:
        if x in Disallowed_chars:
            exit()
    for x in proxy_port:
        if x in Disallowed_chars:
            exit()
    for x in username:
        if x in Disallowed_chars:
            exit()
    for x in password:
        if x in Disallowed_chars:
            exit()
    return 'curl -m 10 -s -x ' + proxy_address + ':' + str(proxy_port) + ' -U ' + username + ':' + password + ' ' + url

def get_proxy_stats(proxy, timeout = 5):
    url = 'http://api.proxyrack.net/stats'
    curl_cmd = get_curl_cmd(proxy, url)
    try:
        stats = os.popen(curl_cmd).read()
        response = json.loads(stats)
    except:
        response = None
    
    return response

def release_exit_node(proxy, timeout = 5):
    url = 'http://api.proxyrack.net/release'
    curl_cmd = get_curl_cmd(proxy, url)

    flag = False
    try:
        response = os.popen(curl_cmd).read()
        
        if 'true' in response:
            flag = True
    except:
        pass
    
    return flag

def get_proxy_info(proxy, timeout = 5):
    url = 'http://ip-api.com/json'
    curl_cmd = get_curl_cmd(proxy, url)

    try:
        response = os.popen(curl_cmd).read()
        response = json.loads(response)
    except:
        response = None

    return response

def get(proxy, url, header = {}, timeout = 5):
    proxy_address, proxy_port, username, password = unpack_proxy_args(proxy)
    proxies = {
        "https":"socks5h://{}:{}@{}".format(username, password, proxy_address + ':' + str(proxy_port)),
        "http":"socks5h://{}:{}@{}".format(username, password, proxy_address + ':' + str(proxy_port))
        }
    try:
        response = requests.get(url, proxies=proxies, headers = header, timeout = timeout) 
    except Exception as e:
        print(e)
        response = None
    
    return response

def check_response(http_result, proxy, headers, url, domain, proxy_info, is_timeout):
    headers = dict()
    headers['Host'] = domain
    headers['User-Agent'] = 'Mozilla/5.0'
    print(url, domain)

    http_result = dict()
    http_result['timestamp'] = int(time.time())
    http_result['status'] = 'success'
    http_result['status_code'] = 0
    http_result['url'] = ''
    http_result['text'] = ''
    http_result['headers'] = dict()
    http_result['is_timeout'] = is_timeout

    if not is_timeout:
        if http_result == '':
            http_result['status'] = 'fail'
            result.append(http_result)
        else:
            http_result['text'] = result.text
            http_result['url'] = result.url
            http_result['status_code'] = result.status_code
            http_result['headers'] = dict(result.headers)
            result.append(http_result)
    else:
        http_result['status'] = 'fail'
        result.append(http_result)

    # return http_result

# def check_response(result, proxy, headers, url, domain, proxy_info, timeout=5):
#     # header = {"Host": domain}
#     print(url, domain)
#     # r = get(proxy, url, header, timeout)
#     # result = process_raw_http_response(response)
#     # if r is None:
#     #     tmp = {}
#     #     tmp["domain"] = domain
#     #     tmp["status"] = 'fail'
#     #     tmp["url"] = url
#     #     tmp["is_timeout"] = True
#     #     tmp["proxy_info"] = proxy_info
#     #     result.append(tmp)
#     # else:
#     #     tmp = {}
#     #     tmp["domain"] = domain
#     #     tmp["status"] = 'success'
#     #     tmp["status_code"] = r.status_code
#     #     tmp["url"] = url
#     #     tmp["text"] = r.text
#     #     tmp["headers"] = r.headers
#     #     tmp["is_timeout"] = False
#     #     tmp["proxy_info"] = proxy_info
#     #     result.append(tmp)


# def proxy_http(domain, proxy, url, server, headers, timeout = 5):
    
#     through_proxy, proxy_address, proxy_port, username, password = unpack_proxy_args(proxy)
    
#     if through_proxy:
#         proxy = {"http":"socks5h://{}:{}@{}".format(username, password, proxy_address + ':' + str(proxy_port))}
#     else:
#         proxy = {}

#     

#     url = 'http://' + server
#     try:
#         raw_http_response = requests.get(url, proxies=proxy, headers = headers, timeout = timeout)

#         is_timeout = False
    
#     except requests.exceptions.Timeout:
#         raw_http_response = ''
#         is_timeout = True

#     except:
#         raw_http_response = ''
#         is_timeout = False

    
#     http_result = process_raw_http_response(raw_http_response, is_timeout)

#     return domain, http_result

if __name__ == "__main__":
    start = time.time()
    country_count = {}
    while True:
        end = time.time()
        if end - start > 86400 * 7:
            break
        if len(country_count) != 0:
            flag = True
            for item_count in country_count.items():
                if item_count[1]<=20:
                    flag = False
                    break
            if flag:
                break
        # read domain
        data = read_domain("./http_overall.txt")

        # read proxy info
        with open("./proxy.json") as f:
            proxy = json.loads(f.read())

        lower_port = 10000
        upper_port = 10249
        proxy["proxy_port"] = random.randint(lower_port, upper_port)
        print(proxy["proxy_port"])
        #with open("port_number_finished.txt","w") as file:
            #file.write(proxy["proxy_port"])
        
        



        
        

        
        # the url we want to test
        url_list = ["", "", "", "", "", "", ""]

    

        # test each domain in file
        result = []
        
    

        y = {}
        for http_result in data:
            # print(http_result)
            
            
            list = []
            for domain in http_result["domain"]:
                
                for url in url_list:
                    list.append([domain, url])
            
            
                
                # print(domain)
                
                
            results = joblib.Parallel(n_jobs = 50,  backend="threading") (joblib.delayed(proxy_http) (item[0], item[1]) for item in list)
            
            
                
                # print(json.dumps(results[0][2], indent=4))
            x = {}    
            for result in results:
                if result[0] not in x.keys():
                    x[result[0]] = {}
                x[result[0]][result[1]]=result[2]
               
                
                
                # for url in url_list:
                #     domain, result = proxy_http(domain, url, proxy)
                    # pool.apply_async(proxy_http, args=(result, proxy, url, domain))
                    
                    
                    
                    # x[url]=result
                    # print(json.dumps(result))
                # y[domain] = x
            print(json.dumps(x, indent=4))
        

        # z = {"domain": x}
        # print(json.dumps(z, indent=4))
        

            
        # result = json.dumps({"proxy": [proxy_info], "domain": [domain_result]})
        # print(proxy_http(domain, url))
        # print("111")
                    
        # wait until all threads finish
        # pool.close()
        # pool.join()

        # change case insensitive dict to dict
        # for http_result in result:
        #     if not http_result["is_timeout"]:
        #         http_result["headers"] = dict(http_result["headers"])

        # with open("result.json", "a") as f:
        # with open(sys.argv[1], "a") as f:
        #     f.write(json.dumps(z) + '\n')
        # exit()
