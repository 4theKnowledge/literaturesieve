"""
Script for filtering key term matched documents from S2 corpus.

inCitations -> citations
outCitations -> references


@author: Tyler Bikaun
"""

import os
import json
import codecs
import re
from langdetect import detect
import pandas as pd

def readTxtFile(filePath):
    fileObject = codecs.open(filePath,"r", "utf-8") 
    fileContents = fileObject.readlines()
    fileObject.close()
    return fileContents


def cleanDocsQuotes(doc):
    doc = doc.replace('\n', '')
    doc = doc.replace("'", '"')
    doc = doc.replace("\\", '')

    return doc


def cleanDocEscapesQuotes(doc):
    doc = doc.replace('\n', '')
    doc = doc.replace("'", '"')
    doc = doc.replace('\\"', '')
    doc = doc.replace('\\', '')
    doc = re.sub(' " | "[.]', '', doc)

    return doc


def convertToJson(file):
    # print(file)
    try:
        docJSON = json.loads(file)
        return docJSON
    except:
        try:
            file = re.sub('\w"s', '', file)  # cant apply to cleanDocQuotes as it's not at the right transformation (problem occurs with docs like: "Textual Silence and (Male) Homosexual Panic in Nuria Amat"s La intimidad (1997)")
            docJSON = json.loads(file)
            return docJSON
        
        except Exception as e:
            print(f'ERROR: {e}')
            print(file)
            pass


def extractContents():
    pass


def main():
    directory = r"C:\Users\22917746\Desktop\Semantic Scholar EDA\keyterm matched all"

    compSciTitleYearDict = {}
    otherFieldsDict = {}

    compSciCount = 0
    otherFieldsCount = 0
    nonEnglishCount = 0

    docsProcessed = 0
    filesProcessed = 0
    fileLimit = 100

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):

            filePath = os.path.join(directory, filename)
            print(f'Processing: {filename}')

            fileContents = readTxtFile(filePath)

            # print(f'Number of Docs: {len(fileContents)}')

            for docContents in fileContents:

                # check if english, if not, pass, otherwise problems...
                try:
                    indexAbstract = docContents.find('paperAbstract')
                    docAbstract = docContents[indexAbstract:indexAbstract+50]
                    docLang = detect(docAbstract)

                    if docLang != 'en':
                        # print(f'\nNOT ENGLISH - Language Detected {docLang}')
                        # print(f'{docAbstract}\n')
                        nonEnglishCount += 1
                        pass

                    else:
                        # strip away 'venue' as it's too problematic; has '10 etc. cannot replace easily.
                        indexVenue = docContents.find('venue')
                        docContents = docContents.replace(docContents[indexVenue-3:], '}')

                        if ' " ' in docContents:   # special document; 
                            try:
                                docContentsJSON = convertToJson(cleanDocEscapesQuotes(docContents))

                                if (1 <= len(docContentsJSON["fieldsOfStudy"])) and ('Computer' in ' '.join(docContentsJSON["fieldsOfStudy"])):
                                    # print(f'{docContentsJSON["title"]} - {docContentsJSON["fieldsOfStudy"]}')
                                    compSciTitleYearDict[docContentsJSON["title"]] = [docContentsJSON["paperAbstract"], docContentsJSON["year"], docContentsJSON["fieldsOfStudy"], docContentsJSON["journalName"], docContentsJSON["s2Url"], len(docContentsJSON["inCitations"]), len(docContentsJSON["outCitations"])]
                                    compSciCount += 1

                                elif len(docContentsJSON["fieldsOfStudy"]) == 0:    # No fields of study defined.
                                    otherFieldsDict[docContentsJSON["title"]] = [docContentsJSON["paperAbstract"], docContentsJSON["year"], docContentsJSON["fieldsOfStudy"]]
                                    otherFieldsCount += 1

                                else:
                                    otherFieldsDict[docContentsJSON["title"]] = [docContentsJSON["paperAbstract"], docContentsJSON["year"], docContentsJSON["fieldsOfStudy"]]
                                    otherFieldsCount += 1

                            except Exception as e:
                                print(e)
                                print(docContents)
                                pass

                        else:       # standard document, doesn't have special stuff in it.
                            try:
                                docContentsJSON = convertToJson(cleanDocsQuotes(docContents))

                                # print(f'{docContentsJSON["fieldsOfStudy"]}\n{docContentsJSON["fieldsOfStudy"][0]}')

                                if (1 <= len(docContentsJSON["fieldsOfStudy"])) and ('Computer' in ' '.join(docContentsJSON["fieldsOfStudy"])):
                                    # print(f'{docContentsJSON["title"]} - {docContentsJSON["fieldsOfStudy"]}')
                                    compSciTitleYearDict[docContentsJSON["title"]] = [docContentsJSON["paperAbstract"], docContentsJSON["year"], docContentsJSON["fieldsOfStudy"], docContentsJSON["journalName"], docContentsJSON["s2Url"], len(docContentsJSON["inCitations"]), len(docContentsJSON["outCitations"])]
                                    compSciCount += 1

                                elif len(docContentsJSON["fieldsOfStudy"]) == 0:    # No fields of study defined.
                                    otherFieldsDict[docContentsJSON["title"]] = [docContentsJSON["paperAbstract"], docContentsJSON["year"], docContentsJSON["fieldsOfStudy"]]
                                    otherFieldsCount += 1

                                else:
                                    otherFieldsDict[docContentsJSON["title"]] = [docContentsJSON["paperAbstract"], docContentsJSON["year"], docContentsJSON["fieldsOfStudy"]]
                                    otherFieldsCount += 1

                            except Exception as e:
                                print(e)
                                print(docContents)
                                pass

                    docsProcessed += 1
                except Exception as e:
                    print('FINAL EXCEPTION')
                    print(e)
                    pass

            filesProcessed += 1

            if fileLimit == filesProcessed:
                break

            # break   # for development; only goes through one doc

        else:
            continue

    print(f'Processed {docsProcessed} Documents | Comp. Sci. {compSciCount} | Other {otherFieldsCount} | Non-English {nonEnglishCount} || Not Captured {docsProcessed-compSciCount-otherFieldsCount-nonEnglishCount}')

    papersOfInterstDataFrame = pd.DataFrame.from_dict(compSciTitleYearDict)
    papersOfInterstDataFrame.T.to_csv('papers_of_interest.csv')

    papersNOTOfInterstDataFrame = pd.DataFrame.from_dict(otherFieldsDict)
    papersNOTOfInterstDataFrame.T.to_csv('papers_NOT_of_interest.csv')

if __name__ == '__main__':
    main()