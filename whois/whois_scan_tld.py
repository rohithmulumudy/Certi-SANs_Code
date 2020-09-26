import multiprocessing
import subprocess

def run_one_scan(url):
    parts = url.split(".")
    toplevel = ".".join(parts[-2:])
    print(f"Whois on {toplevel}")
    p = subprocess.Popen([f"whois {toplevel} > whois_tld/{toplevel}.whoistld"], shell=True)
    while p.poll() is None:
        p.wait()

    return p.poll()

if __name__ == "__main__":
    urls = [a.replace("\n", "") for a in open("all_nodes_unique.txt", "r").readlines()]
    i = 0
    while i < len(urls):
        with multiprocessing.Pool(100) as pool:
            print(pool.map(run_one_scan, urls[i: (i+100)]))

        i += 100
