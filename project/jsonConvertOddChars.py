import json
import codecs
import re

text = """{'entities': [], 'journalVolume': '', 'journalPages': '263-274', 'pmid': '', 'fieldsOfStudy': ['Computer Science'], 'year': 2010, 'outCitations': ['236ad7612b46079c8efd6f88d5e2ae946bd6fe93', '017ddb7e815236defd0566bc46f6ed8401cc6ba6', '7889b0b8f02330a310869f10fc9a953479371d16', '868ac9cd5849336fcdcabfa3dea22867ee4661e5', '6d9794be1073b41855d9962983b8956e35baa7e1', '99ea0f3d8c210a0d1a042ad92ad5d7e26fd0942b', 'cea70b3921ddbaf2cdb54dd1e447a639772c512a', 'abcbb8e00bff6cd3f5147a4970292e784bb5d34b'], 's2Url': 'https://semanticscholar.org/paper/b56c5cac50ddbc4d58d34f4d8a38abcb21ba72d2', 's2PdfUrl': '', 'id': 'b56c5cac50ddbc4d58d34f4d8a38abcb21ba72d2', 'authors': [{'name': 'Jozo J. Dujmovic', 'ids': ['1768707']}], 'journalName': '', 'paperAbstract': 'In this tutorial, we describe techniques for automatic generation of benchmark and test workloads. Generated programs have adjustable parameters that are used to select the program size and structure, as well as the relative frequencies of basic operations (or program modules) that characterize the workload.', 'inCitations': ['248dd025a7c3451d803642a0db70f336d4076b3a', 'f7f3b24ac83ceb80ba58ef07b5ce399619fc5f51', '1eecd92a73f9e492cee34ca0b4a05e41770c759d', 'a070e1a5c739d6e189719a0fd7abfca1bdc033c8', '0e718a2d0c05a3b9143273253ea0221f2d2ca70f', '53099d3668c35531088160c22e672e0925cf262f'], 'pdfUrls': ['https://research.spec.org/icpe_proceedings/2010/p263.pdf', 'https://doi.org/10.1145/1712605.1712654'], 'title': 'Automatic generation of benchmark and test workloads', 'doi': '10.1145/1712605.1712654', 'sources': ['DBLP'], 'doiUrl': 'https://doi.org/10.1145/1712605.1712654', 'venue': "WOSP/SIPEW '10"}"""

index = text.find('venue')


text = text.replace(text[index-3:], '}')

print(text)