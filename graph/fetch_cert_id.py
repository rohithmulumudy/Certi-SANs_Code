from streamProcessor import JsonLinesProcessor
import sys
import tqdm

def getCertId(cert):
    return (cert['certificate']['issuer']['commonName'],
           cert['certificate']['issuer']['organizationName'],
           cert['certificate']['issuer']['organizationUnitName'],
           cert['certificate']['subjectNameHash']
    )

if __name__ == "__main__":
    j = JsonLinesProcessor(sys.argv[1])
    for line in tqdm.tqdm(j):
        print(line['host'], getCertId(line))