"""
@author: Tyler Bikaun
"""

from tqdm import tqdm
import gzip
import json
from langdetect import detect
import time
from pprint import pprint
import concurrent.futures
import codecs
import re

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f seconds' % (method.__name__, (te - ts)))
        return result
    return timed

@timeit
def unzipS2Contents(url):
    f = gzip.open(url, 'rb')
    file_content = f.read().decode('utf-8')
    f.close()
    fileContentsList = file_content.split('\n')
    return fileContentsList

def getManifest(fileLocation):
    # Get list of .gz documents from S2 manifest
    manifestFile = open(fileLocation, "r")
    manifestFile = manifestFile.read()
    manifestFileList = manifestFile.split('\n')
    manifestFileList = [file for file in manifestFileList if 's2' in file]

    return manifestFileList


def convertToJson(file):
    try:
        docJSON = json.loads(file)
        return docJSON
    except Exception as e:
        # print(f'ERROR: {e}')
        pass


def getEnglishDoc(file):
    try:
        docJSON = json.loads(file)

        if detect(docJSON["title"]) == 'en':    # can have errors if there isn't a title specified.
            return docJSON
            # return f'Year: {docJSON["year"]} - Title: {docJSON["title"]} - ID: {docJSON["id"]}'

    except Exception as e:
        # print(f'ERROR: {e}')
        pass


def matchDocWithKeyTerms(file):
    # print(file)

    # keyTermsList = ['summarisation', 'summarization', 'nlg', 'extractive', 'summeries', 'summarizatio']    # spelling problems...; removed automatic as it's too general when it matches by itself

    docJSON = json.loads(json.dumps(file))      # dumps if input is dict...

    # keyTermsMatched = set(docJSON["title"].lower().split(' ')).intersection(set(keyTermsList))
    
    pattern = "(summarization|summarisation|text|nlg|nlp)|(automatic)[^.]*(generation|summary|summarization|summarisation)|(abstractive|extractive)[^.]*(model|summary|modelling|modeling|summarization|summarisation|processing)|(semantic)[^.]*(retrieval|graph|model|modelling|modeling|summarization|summarisation|processing|representations)|(natural|language)[^.]*(language|generation|processing)|(information)[^.]*(retrieval|graph|summary|summarization|summarisation)"

    if (re.match(pattern, docJSON["title"].lower())) or (re.match(pattern, docJSON["paperAbstract"].lower())):
        print(f'DOC MATCHED: {docJSON["title"]}')
        return docJSON
    else:
        pass


@timeit
def main():

    s2CorpusList = getManifest(r"data/sample/semantic scholar manifest 2020-03.txt")

    for s2Corpus in s2CorpusList:
        print(f'Processing: {s2Corpus}')
        s2CorpusUrl = fr"C:\Users\22917746\Desktop\Semantic Scholar EDA\data\raw\{s2Corpus}"

        fileContentsList = unzipS2Contents(s2CorpusUrl)

        print(f'Number of files: {len(fileContentsList)}')

        # Batch processing files rather than distributing massive amounts to each core
        batchSize = 10000
        chunks = (len(fileContentsList)-1) // batchSize + 1
        batchCount = 1
        
        for i in range(chunks):
            start = time.time()
            batch = fileContentsList[i*batchSize:(i+1)*batchSize]
            print(f'\nProcessing batch {batchCount} - Size: {len(batch)}')
        
            # # English Sieving
            # docListEnglish = []
            # with concurrent.futures.ProcessPoolExecutor() as executor:
            #     results = executor.map(getEnglishDoc, batch)

            #     # resultCount = 1
            #     for result in results:
            #         if result is not None:
            #             # print(f'{resultCount} - {result}')
            #             docListEnglish.append(result)
            #         else:
            #             # print(f'{resultCount} - Non-English Title')
            #             pass
            #         # resultCount += 1
            # finishCheckEng = time.time()

            # outputFileEnglishDoc = codecs.open(f"englishDocs_{batchCount}.txt", "w", "utf-8")
            # for englishDocContent in docListEnglish:
            #     outputFileEnglishDoc.writelines(f'{englishDocContent}\n')
            # outputFileEnglishDoc.close()

            # finishWriteToDisk = time.time()
            # print(f'Time to check english {finishCheckEng-start:0.1f}')
            # print(f'Time to write to disk {finishWriteToDisk-start:0.1f}')

            docListJSON = []
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = executor.map(convertToJson, batch)
                for result in results:
                    if result is not None:
                        docListJSON.append(result)
                    else:
                        pass
            finishJSONConvert = time.time()
            print(f'Time to convert to JSON {finishJSONConvert-start:0.1f}')
            

            # Key Term Matching
            start1 = time.time()
            docKeyTermMatched = []
            for doc in docListJSON: #docListEnglish:
                result = matchDocWithKeyTerms(doc)
                if result is not None:
                    # print(result)
                    docKeyTermMatched.append(result)

            s2CorpusFname = s2Corpus.split('.')[0]
            outputFileKeyTermMatched = codecs.open(f"englishDocsKeyTermMatched_{s2CorpusFname}_{batchCount}.txt", "w", "utf-8")
            for docMatched in docKeyTermMatched:
                outputFileKeyTermMatched.writelines(f'{docMatched}\n')
            outputFileKeyTermMatched.close()

            finish1 = time.time()
            print(f'Time to extract keyterms {finish1-start1:0.1f}')

            batchCount += 1

if __name__ == '__main__':
    main()