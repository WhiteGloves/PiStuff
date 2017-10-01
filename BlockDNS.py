# Procedure:
#
#   1) Make local copies of various lists
#   2) 
#
#

import urllib 

class BlockDNS:
    
    def __init__(self):
        self.blacklists = {}
        self.compiled = set()

    def fetch_lists(self):
        with open('blocklist_info.txt', 'r') as f:
            i = 0
            for line in f:
                self.blacklists["blacklist"+str(i)] = line.strip()
                i += 1
        www = urllib.URLopener()
        for key in self.blacklists:
            www.retrieve(self.blacklists[key], key)
        print("Downloaded {} Blocklists.".format(len(self.blacklists)))

    def build_blocklist(self):
        with open('whitelist.txt','r') as f:
            whitelist = set(f.read().split())
        for filename in self.blacklists:
            with open(filename, 'r') as f:
                for line in f:
                    if line[0] == "#":
                        continue
                    for url in line.split():
                        if self.domain_check(url):
                            if url not in whitelist:
                                self.compiled.add(url)
                            else:
                                print("Attempted Blocking ({}): {}".format(filename, url))
        print("Blacklisted Domains: {}".format(len(self.compiled)))
        with open('compiled.txt', 'w') as outfile:
            outfile.write("\n".join(sorted(self.compiled)))

    @staticmethod
    def domain_check(url):
        parts = url.split('.')
        if len(parts) < 2 or parts[-1].isdigit():
            return False
        return True

def clean_whitelist():
    whitelist = None
    with open('my_whitelist.txt','r') as f:
        whitelist = set(f.read().split())
    with open('whitelist.txt', 'w') as outfile:
        outfile.write("\n".join(sorted(whitelist)))
        
def main():
    blocker = BlockDNS()
    blocker.fetch_lists()
    blocker.build_blocklist()

if __name__ == "__main__":
    main()
