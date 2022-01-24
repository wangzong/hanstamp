from ipchecktoken import IP_TOKEN
import requests
import json
import os
import re
import csv
from urllib.parse import unquote

LOG_FILE = 'D:\\Dropbox\\Project\\hanstamp\\hs_env\\analyzelog\\access.log';

# The column in IP_MAPPING_CSV is
# ip, location, people
IP_MAPPING_CSV = 'D:\\Dropbox\\Project\\hanstamp\\hs_env\\analyzelog\\ipmapping.csv';

def ip2city_via_api(ip, IP_TOKEN):
    'https://api.ip138.com/ip/?ip=58.16.180.3&datatype=jsonp&token=cc87f3c77747bccbaaee35006da1ebb65e0bad57'
    url = 'https://api.ip138.com/ip/?ip=' + ip + '&datatype=jsonp&token=' + IP_TOKEN;
    r = requests.get(url);
    if r.status_code == 200:
        result = r.json();
        city = result['data'][1] + result['data'][2]
        return city;
    else:
        return -1;

if __name__ == "__main__":

    # 1. Read /var/log/nginx/access.log, select the entries of search
    #    get ip/time/search_content, save to log_entries list,
    #    each item in list is a dict
    # 1.1 convert search_content into character, save to logs_no_duplication list

    with open(LOG_FILE, mode='r', encoding='utf-8') as f:
        lines = f.readlines();

    log_entries = []
    entry = {}

    for line in lines:
        # A sample of request in log:
        # 183.192.121.209 - - [15/Jan/2022:14:51:23 +0800] "GET /search/?search=%E4%B9%8B HTTP/1.1" 200 2916 "http://47.96.124.27/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36" "-"
        # reg = re.compile('^(\d+.\d+.\d+.\d+) - - (\[.*\])\w+(\"http://47.96.124.27/search/?search=\w+\")')
        reg = re.compile('^(\d+.\d+.\d+.\d+) - - \[(.*)\].*\"GET /search/\?search=(.*?)\sHTTP/1.1\"\s+\d+\s+\d+\s+\"http://47.96.124.27/.*\"')
        reg_match = reg.findall(line)
        if len(reg_match):
            entry['ip'] = reg_match[0][0]
            entry['datetime'] = reg_match[0][1]
            entry['content'] = reg_match[0][2]
            entry['char'] = unquote(entry['content'])
            log_entries.append(entry)
            entry = {}

    logs_no_duplication = []

    for log in log_entries:
        if log not in logs_no_duplication:
            logs_no_duplication.append(log)

    # 2. Read ip-mapping file IP_MAPPING_CSV, save to ip_mappings list, each item is a dict {ip:<ip_address>, location:<location>, people:<people>}

    ip_mappings_list = []

    with open(IP_MAPPING_CSV, newline='', encoding='utf-8') as csv_file:
        ip_reader = csv.reader(csv_file, delimiter=',')
        for row in ip_reader:
            element={}
            element['ip'] = row[0]
            element['location'] = row[1]
            element['people'] = row[2]
            ip_mappings_list.append(element)

    # 3. search the ip of the log_entries,
    # 3.1 if the ip exist in ip_mapping dict, get the location from ip_mapping dict, write to log_entries
    # 3.2 if the ip doesn't exist in ip_mapping dict, get the location by send request to ip138.com
    #     and add the new ip entry to ip_entries, write to IP_MAPPING_CSV

    for entry in logs_no_duplication:
        ip = entry['ip']
        ip_exist = False
        for ip_entry in ip_mappings_list:
            if ip_entry['ip'] == ip:
                print(f'{ip} exist in ip mapping.')
                entry['location'] = ip_entry['location']
                entry['people'] = ip_entry['people']
                ip_exist = True

        if not ip_exist:
            print(f'{ip} doesn\'t exist in ip mapping, need to get via api')
            entry['location'] = ip2city_via_api(ip,IP_TOKEN)
            entry['people'] = ''
            new_ip_mapping = {'ip':ip,
                              'location':entry['location'],
                              'people':entry['people']}
            ip_mappings_list.append(new_ip_mapping)

            print(f'Writing {ip} to {IP_MAPPING_CSV}')
            with open(IP_MAPPING_CSV, newline='',mode='a', encoding='utf-8') as csv_file:
                ip_writer = csv.writer(csv_file, delimiter=',')
                ip_writer.writerow([new_ip_mapping['ip'],
                                 new_ip_mapping['location'],
                                 new_ip_mapping['people']])

    # 4. save log_entries into a csv file

    print(f'Writing to log.csv...')
    labels = ['ip', 'datetime', 'char','location', 'people','content']
    try:
        with open('log.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=labels)
            writer.writeheader()
            for log in logs_no_duplication:
                writer.writerow(log)
    except IOError:
        print("I/O error")