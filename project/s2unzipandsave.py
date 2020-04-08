"""
Unzip file, convert to json, and save to disk.
@author: Tyler Bikaun
"""


import gzip
import time
import codecs

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

@timeit
def unzipS2Contents(url):
    f = gzip.open(url, 'rb')
    file_content = f.read().decode('utf-8')
    f.close()
    fileContentsList = file_content.split('\n')
    return fileContentsList


if __name__ == '__main__':
    s2CorpusUrl = r"C:\Users\22917746\Desktop\Semantic Scholar EDA\data\s2-corpus-000.gz"

    fileContentsList = unzipS2Contents(s2CorpusUrl)

    # print(fileContentsList)

    file1 = codecs.open("myfile.txt","w", "utf-8") 
    for line in fileContentsList:
        file1.writelines(line) 
    file1.close() #to change file access modes