from streamProcessor import JsonLinesProcessor

PATH = "finalData/{}-round/3.cert.hosts.json"
REDIR_PATH = "finalData/{}-round/2.total.hosts.after.substituting.redirection.json"

with open("edgelist.txt", "a") as f:
    for i in range(1, 14):
        source = JsonLinesProcessor(PATH.format(str(i).zfill(2)))
        redir = {}
        try:
            r = JsonLinesProcessor(REDIR_PATH.format(str(i + i).zfill(2)))
            for row in r:
                redir[row["host"]] = row["final_redir"]
        except:
            pass
        print("Processing", PATH.format(str(i).zfill(2)))
        for row in source:
            host = row["host"]
            sans = row["certificate"]["san"]
            for san in sans.split("; "):
                san = san.replace("DNS:", "")
                san = san.replace("URL:", "")
                san = san.replace("*.", "")
                
                if san in redir:
                    san = redir[san]
                    print("Redirect edge", end=" ")
                print(i, "Adding edge", host, san)
                f.write("%s %s\n" % (host, san))
