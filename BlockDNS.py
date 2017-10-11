# Procedure:
#
#   1) Make local copies of various lists
#   2) 
#
#

import urllib 

class BlockDNS:
    RAW = 'raw_blocklist.txt'
    INFO = 'blocklist_info.txt'
    TEMP = 'tmp_raw.dat'
    WHITE = 'my_whitelist.txt'
    BLACK = 'my_blacklist.txt'
    COMPILED = 'compiled.txt'
    
    def __init__(self):
        self.compiled = set()
        self.whitelist = None
        self.num_list = 0

    def fetch_lists(self):
        blocklists = None
        www = urllib.URLopener()
        with open(self.INFO, 'r') as f:
            blocklists = f.read().split()
        with open(self.RAW, 'w') as output:
            with open(self.BLACK, 'r') as f:
                output.write(f.read())
            for blist in blocklists:
                print("Downloading: {}".format(blist))
                www.retrieve(blist, "tmp_raw.dat")
                with open(self.TEMP, 'r') as f:
                    for line in f:
                        if line[0] not in "#![":
                            output.write(line)
        self.num_list = len(blocklists)
        print("Downloaded {} Blocklists.".format(self.num_list))        

    def build_blocklist(self):
        self.clean_lists()
        for filename in [self.RAW, self.BLACK]:
            with open(filename, 'r') as f:
                for url in f.read().split():
                    if self.domain_check(url):
                        self.compiled.add(url)
        for url in self.whitelist:
            if url in self.compiled:
                self.compiled.remove(url)
        print("Blacklisted Domains: {}".format(len(self.compiled)))

    def fetch_hostfiles(self):
        pass

    def filter_file(self, line):
        for line in [x for x in f if line[0] != "#"]:
            pass

    def clean_lists(self):
        with open(self.WHITE,'r') as f:
            self.whitelist = set(f.read().split())

    def save_blocklists(self):
        with open(self.COMPILED, 'w') as outfile:
            outfile.write("\n".join(sorted(self.compiled)))
        with open(self.WHITE, 'w') as outfile:
            outfile.write("\n".join(sorted(self.whitelist)))

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
    blocker.fetch_lists()
    blocker.build_blocklist()
    blocker.save_blocklists()

if __name__ == "__main__":
    main()
