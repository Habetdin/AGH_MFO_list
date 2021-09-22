#!/usr/bin/python3

import idna.codec
import re
import sys
from datetime import datetime

class MfoParser:
    def __init__(self, source, mirror, result):
        self.list_source = source
        self.list_mirror = mirror
        self.list_result = result

        self.regex_split = re.compile(r'[^\w\-\.:/\?=]+', re.UNICODE)
        self.regex_clean = re.compile(r'(?:^(?:[a-z]*(?:://|//|:)(?:www\.)?|www\.)|/.*$)')
        self.regex_owner = re.compile(r'\.([^\.]+\.[^\.]+)$')

        self.domain_fixes = {
            'vk.com': 'vk-dot-com',  # special: skip
            'atrium.djsun.ru': 'djsun.ru',
            'che.lombardini.pro': 'lombardini.pro',
            'fmoo.msb-orel.ru': 'msb-orel.ru',
            'fond.udbiz.ru': 'udbiz.ru',
            'gatchina.813.ru': '813.ru',
            'kirsfond.wixset.com': 'kirsfond.wixsite.com',
            'lk.udbiz.ru': 'udbiz.ru',
            'new.vv174.ru': 'vv174.ru',
            'nn.ketfinans.ru': 'ketfinans.ru',
            'v.credit.ru': 'v.credit',
            'vsevolozhsk.813.ru': '813.ru',
        }

        self.known_domains = [
            'finx.com.ru',
            'moe.ru.com',
            'бц.подосиновец.рф',
        ]

        self.known_suffixes = [
            '1c-umi.ru', 'umi.ru',
            'beget.tech',
            'blogspot.com',
            'karelia.ru',
            'mya5.ru',
            'nethouse.ru',
            'tomsk.ru',
            'ucoz.ru', 'ucoz.net', 'my1.ru',
            'upgrade14.ru',
            'vov.ru',
            'webnode.ru',
            'wix.com', 'wixsite.com',
            'крым.рус',
        ]

        self.data_result = []
        self.data_suffix = {}


    def extract_domains(self, line):
        line = line.strip()
        urls = re.split(self.regex_split, line.lower())
        for url in urls:
            if url not in ['', 'нет', 'отсутствует']:
                host = re.sub(self.regex_clean, '', url)
                if host in self.domain_fixes:
                    host = self.domain_fixes[host]
                dots = host.count('.')
                if dots > 0:
                    self.data_result.append(host.encode('idna').decode('utf-8'))
                    if dots > 1 and host not in self.known_domains:
                        m = re.search(self.regex_owner, host)
                        if m:
                            suffix = m.group(1)
                            if suffix not in self.known_suffixes:
                                if suffix in self.data_suffix:
                                    self.data_suffix[suffix] = data_suffix[suffix] + 1
                                else:
                                    self.data_suffix[suffix] = 1
                                print('Hostname to check manually: "{}"'.format(host))
                        else:
                                print('Could not find 2nd-level domain: "{}"'.format(host), file=sys.stderr)
                else:
                    print('Not a hostname: "{}" in "{}" line'.format(host, line), file=sys.stderr)


    def execute(self):
        with open(self.list_source, 'r', encoding='utf-8-sig') as f:
            print('Parsing source list...')
            line = f.readline()
            while line:
                line = line.strip()
                if line:
                    if 'Адреса официальных сайтов' in line:
                        print('Skipped line: "{}"'.format(line))
                    else:
                        self.extract_domains(line)
                line = f.readline()
            print('- - -')

        if len(self.data_suffix):
            print('Top 2nd-level domains:')
            for key, value in sorted(self.data_suffix.items(), key=lambda x: x[1], reverse=True):
                print(key, value)
            print('- - -')

        with open(self.list_mirror, 'r', encoding='utf-8-sig') as f:
            print('Parsing mirrors list...')
            line = f.readline()
            while line:
                line = line.strip()
                if line:
                    self.extract_domains(line)
                line = f.readline()
            print('- - -')

        for host in self.data_result:
            if '.1c-umi.ru' in host:
                twin = host.replace('.1c-umi.ru', '.umi.ru')
            elif '.umi.ru' in host:
                twin = host.replace('.umi.ru', '.1c-umi.ru')
            elif '.wix.com' in host:
                twin = host.replace('.wix.com', '.wixsite.com')
            elif '.wixsite.com' in host:
                twin = host.replace('.wixsite.com', '.wix.com')
            else:
                continue
            if twin not in self.data_result:
                self.data_result.append(twin)

        self.data_result = sorted(set(self.data_result))
        print('Found {} unique hostnames'.format(len(self.data_result)))
        with open(self.list_result, 'w', encoding='utf-8') as f:
            f.write('! Title: Microfinancing Organizations Blocklist for AdGuard Home\n')
            f.write('! Updated: {}\n'.format(datetime.now().astimezone().replace(microsecond=0).isoformat()))
            f.write('! Expires: 30 days\n')
            f.write('! Homepage: https://github.com/Habetdin/AGH_MFO_list\n')
            f.write('! License: The Unlicense\n')
            f.write('! Source: https://cbr.ru/vfs/finmarkets/files/supervision/list_MFO.xlsx\n')
            for host in self.data_result:
                f.write('||{}^\n'.format(host))
