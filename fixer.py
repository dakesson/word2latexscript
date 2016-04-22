# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:23:04 2016

@author: danielakesson
"""

import bibtexparser
from fuzzywuzzy import fuzz
import fileinput


#from fuzzywuzzy import process

class ReferenceParser():
    def __init__(self,bibtexFileName, referenceTextFile, outputFileName):
        self.outputFileName = outputFileName
        with open(bibtexFileName) as bibtex_file:
            bibtex_str = bibtex_file.read()
        self.bibDatabase = bibtexparser.loads(bibtex_str)
    
        with open(referenceTextFile) as g:
            self.wordRef = g.readlines()
        print("Reference parser init...")

        
    def searchThroughText(self):
        for wordRow in self.wordRef:
            searchTitle = wordRow.split("]")[1] #Remove start [xx]
            searchString = wordRow.split("	")[0] #[1].. etc
            
            replaceString = "\cite{" + self.getKeyFor(searchTitle) + "}" #\
            
            if len(replaceString) > 0:
                self.replace(searchString,replaceString)
            
    def replace(self,searchString, replaceString):
        print("Replace:\"" + searchString + "\” with \”" + replaceString + "\”")
        with fileinput.FileInput(self.outputFileName, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(searchString, replaceString), end='')
        
    def getKeyFor(self,searchTitle):
        bestMatch = ""
        bestRatio = 0.0
        for entry in self.bibDatabase.entries:
            ratio = (fuzz.ratio(searchTitle, entry['title']))
            
            if ratio > 20 and ratio > bestRatio:
                bestMatch = entry['ID']
                bestRatio = ratio
        
        if bestRatio == 0.0:
            print("Not found: \n”" + searchTitle + "\"")
        else:
            return bestMatch
    
    
    #Open bibtex file
    
    
referenceParser = ReferenceParser("bibtex.bib","referenser.txt","text.tex")
referenceParser.searchThroughText()



#    bibList.append(entry['title'])

#foundString = (