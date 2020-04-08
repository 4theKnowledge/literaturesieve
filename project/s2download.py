"""
@author: Tyler Bikaun
@info: http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/download/
"""

import requests
from tqdm import tqdm

# Get list of .gz documents from S2 manifest
manifestFile = open("../data/sample/semantic scholar manifest 2020-03.txt", "r")
manifestFile = manifestFile.read()
manifestFileList = manifestFile.split('\n')
manifestFileList = [file for file in manifestFileList if 's2' in file]

for manifestFile in tqdm(manifestFileList):
    file = requests.get(f'https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-03-01/{manifestFile}')
    open(f'../data/raw/{manifestFile}', 'wb').write(file.content)