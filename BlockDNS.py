# Procedure:
#
#   1) Make local copies of various lists
#   2) 
#
#

import re
import urllib2

class AdblockParser:
    URL = 'https://fanboy.co.nz/r/fanboy-ultimate.txt'
    RAW = 'abp_ultimate.txt'
    REX = '\|\|([a-zA-Z0-9-.]+\.[a-zA-Z]+)\^\$'
    BAD = 'abp_domains.txt'
    
    def __init__(self):
        self.fetch_list()
        self.bad_url = set()
        self.raw_file = None

    def fetch_list(self):
        req = urllib2.Request(AdblockParser.URL, headers={'User-Agent' : "Magic Browser"}) 
        con = urllib2.urlopen(req)
        with open(AdblockParser.RAW, 'w') as output:
            output.write(con.read())

    def parse_list(self):
        regex = re.compile(AdblockParser.REX)
        with open(AdblockParser.RAW, 'r') as blocklist:
            for line in blocklist:
                domain = regex.match(line)
                if domain:
                   self.bad_url.add(domain.group(1))
        print "Bad Domains: {}".format(len(self.bad_url))

    def save_list(self):
        with open(AdblockParser.BAD, 'w') as output:
            output.write('\n'.join(sorted(self.bad_url)))

class BlockDNS:
    WHITE = 'my_whitelist.txt'
    BLACK = 'my_blacklist.txt'
    COMPILED = 'compiled.txt'
    URL_HEADER = {'User-Agent' : "Magic Browser"}
    BLOCKLISTS = {'host': 'hostfiles.txt',
                  'adblock': 'adblocklists.txt'}
    
    def __init__(self):
        self.blacklist = None
        self.whitelist = None
        self.blocklist = None
        self.regex = {
            'host': '(\d+\.\d+\.\d+\.\d+\s+)?([a-z0-9][a-z0-9-.]*\.[a-z]+)',
            'adblock': '(\|\|)([a-z0-9][a-z0-9-.]*\.[a-z]+)\^\$'
            }
        for key, pattern in self.regex.iteritems():
            self.regex[key] = re.compile(pattern, re.IGNORECASE)

    def load_lists(self):
        self.blocklist = []
        for key, filename in BlockDNS.BLOCKLISTS.iteritems():
            with open(filename, 'r') as f:
                for line in f:
                    self.blocklist.append((line.strip(), key))
            
    def parse_lists(self):
        self.clean_lists()
        ban = self.blacklist.add
        print "Parsing Blocklists:"
        i = 0
        for url, key in self.blocklist:
            print("{}: {}".format(i, url))
            for line in BlockDNS.load_url(url):
                domain = self.regex[key].match(line)
                if domain:
                    ban(domain.group(2))
            i = i + 1
        print("Blacklisted Domains: {}".format(len(self.blacklist)))
        with open(BlockDNS.COMPILED, 'w') as outfile:
            outfile.write("\n".join(sorted(self.blacklist)))

    def clean_lists(self):
        with open(BlockDNS.WHITE, 'r') as f:
            self.whitelist = set(f.read().split())
        with open(BlockDNS.WHITE, 'w') as f:
            f.write('\n'.join(sorted(self.whitelist)))
        with open(BlockDNS.BLACK, 'r') as f:
            self.blacklist = set(f.read().split())
        with open(BlockDNS.BLACK, 'w') as f:
            f.write('\n'.join(sorted(self.blacklist)))
    
    @staticmethod
    def load_url(url):
        req = urllib2.Request(url, headers=BlockDNS.URL_HEADER)
        return urllib2.urlopen(req)

    @staticmethod
    def domain_check(url):
        is_domain = True
        dots = url.count('.')
        if dots < 1:
            is_domain = False
        elif dots == 3 and url.replace('.','').isdigit():
            is_domain = False
        return is_domain
        
def main():
    blocker = BlockDNS()
    blocker.load_lists()
    blocker.parse_lists()

if __name__ == "__main__":
    main()
