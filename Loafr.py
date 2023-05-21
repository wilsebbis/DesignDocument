import os
# Pandas does not need to be implemented - carries over

class Loafr:
    def __init__(self,dataLog=None,searchSettings=None, masterString = None):
        self.dataLog=dataLog                                                            #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
        self.searchSettings = searchSettings                                            #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
        self.masterString = masterString
    
    '''
    Can search by exact, greater, or lesser. Each search returns a new dataframe which can once again
    be searched, allowing for more and more specificity.

    Return Type: None
    Parameters: None
    Return value: None
    Pre-condition: Dataframe being used
    Post-condition: A dataframe with the values of the searched log.
    Attributes read/used: self.searchSettings, self.dataLog
    '''
    #Traceability: Method 'Search': Design Document 4.2.1.2
    def search(self):                                                                    
        data = self.dataLog                                                              #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
        if(self.searchSettings.searchStrings == ['']):                                   #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
            return
        for i in range(len(self.searchSettings.searchStrings)):
            lessGreatEqual = self.searchSettings.lessGreatEqual[i]
            searchCols = self.searchSettings.searchCols[i]
            searchStrings = self.searchSettings.searchStrings[i]
            if (lessGreatEqual == "equal"):
                data = data[data[searchCols] == searchStrings]
            elif (lessGreatEqual == "greater"):
                data = data[data[searchCols] > int(searchStrings)]
            elif (lessGreatEqual == "lesser"):
                data = data[data[searchCols] < int(searchStrings)]
            self.dataLog = data

   
    '''
    Can sort by any column's values, by greater or lowest first. Each sort returns a new dataframe
    which can be sorted by another column, so you can have highest net worth people sorted by first
    name, so people who both have $1 billion will be at the top, but Alex the billionaire
    will come before Zander the billionaire.

    Return Type: None
    Parameters: None
    Return value: None
    Pre-condition: Dataframe being used.
    Post-condition: A dataframe with the values of the sorted log.
    Attributes read/used: self.searchSettings, self.dataLog
    '''
    #Traceability: Method 'Sort': Design Document 4.2.1.2
    def sort(self):
        data = self.dataLog                                                              #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
        if(self.searchSettings.sortColumns == ['']):                                     #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
            return
        for i in range(len(self.searchSettings.sortColumns)):
            sortCol = self.searchSettings.sortColumns[i]
            sortAsc = bool(self.searchSettings.sortAscending[i])
            data = data.sort_values(sortCol, ascending = sortAsc)
        self.dataLog = data

   
    '''
    Can filter by row, so if you only want to see the testing_environment of
    data with a test_output of "Bork" you can do that.

    Return Type: None
    Parameters: None
    Return value: None
    Pre-condition: Dataframe being used.
    Post-condition: A dataframe with the values of the filtered log.
    Attributes read/used: self.dataLog
    '''
    #Traceability: Method 'Filter': Design Document 4.2.1.2
    def filter(self):
        data = self.dataLog                                                             #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
        if(self.searchSettings.filters == ['']):                                        #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
            return
        data = data.filter(items=self.searchSettings.filters)
        self.dataLog = data

   
    '''
    Exports the dataframe values to a .CSV file.

    Return Type: None
    Parameters: fileSaveLocation
    Return value: None
    Pre-condition: Log file being looked at.
    Post-condition: A file with the values of the log.
    Attributes read/used: self.dataLog
    '''
    #Traceability: Method 'ExportLog': Design Document 4.2.1.2
    def exportLog(self, fileSaveLocation):
        data = self.dataLog                                                            #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
        i = 0
        newfileLocation = fileSaveLocation
        if (os.path.exists(newfileLocation + ".csv") == False):
            data.to_csv(newfileLocation + ".csv",index=False)
        else:
            while(os.path.exists(newfileLocation + ".csv")):
                newfileLocation = fileSaveLocation
                i = i + 1
                newfileLocation = newfileLocation + str(i)
            fileSaveLocation = fileSaveLocation + str(i) + ".csv"
            data.to_csv(fileSaveLocation,index=False)

    
    '''
    We haven't fully figured out what to do with this part yet, may be scrapped in the next build.
    '''
    #Traceability: Method 'GenerateReport': Design Document 4.2.1.2
    def generateReport(self, fileSaveLocation):
        i = 0
        newfileLocation = fileSaveLocation
        if (os.path.exists(newfileLocation + ".csv") == False):
            with open(newfileLocation + ".csv", "x") as f:
                f.write("space holder")
        else:
            while(os.path.exists(newfileLocation + ".csv")):
                newfileLocation = fileSaveLocation
                i = i + 1
                newfileLocation = newfileLocation + str(i)
            fileSaveLocation = fileSaveLocation + str(i) + ".csv"
            with open(fileSaveLocation, "x") as f:
                f.write("space holder")


    # Groups labels by terms. So "Operator" and "Dog" gives you 2 because there are two
    # instances of Dog Operators. "Operator" and "Cat" gives you 1 because there is one
    # instance of a Cat Operator.
    
    #Traceability: Method 'groupBy': Design Document 4.2.1.2
    def groupBy(self):
        stringList = []
        if(self.searchSettings.groupLabel == ['']):
            return
        if(self.searchSettings.searchStrings != ['']):
            for i in range(len(self.searchSettings.searchStrings)):
                stringList.append("You searched for " + self.searchSettings.searchStrings[i] + " in the column " + self.searchSettings.searchCols[i] + " and wanted results which were " + self.searchSettings.lessGreatEqual[i] + " to that search term.\n")

        if(self.searchSettings.sortColumns != ['']):
            for i in range(len(self.searchSettings.sortColumns)):
                stringList.append("You sorted the column " + self.searchSettings.sortColumns[i] + " and you wanted it ascending: " + self.searchSettings.sortAscending[i]+"\n")

        if(self.searchSettings.filters != ['']):
            stringList.append("You filtered by " + self.searchSettings.filters + " to only see those specific columns."+"\n")

        if(self.searchSettings.groupLabel != ['']):
            for i in range(len(self.searchSettings.groupLabel)):
                stringList.append("You grouped the following column: " + self.searchSettings.groupLabel[i] + " by the following value: " + self.searchSettings.groupTerm[i]+"\n")

        if(self.searchSettings.betweenFirst != ['']):
            for i in range(len(self.searchSettings.betweenFirst)):
                stringList.append("You looked between " + self.searchSettings.betweenFirst[i] + " and " + self.searchSettings.betweenLast[i] + " in the following column: " + self.searchSettings.betweenCol[i]+"\n")

        for i in range(len(self.searchSettings.groupLabel)):
            stringList.append("Your result is: " + str(self.dataLog.groupby(by=[self.searchSettings.groupLabel[i]]).count().loc[self.searchSettings.groupTerm[i]][0]))
    
        self.masterString = "".join(stringList)

    #TODO:
    # For example, keep all entries between A and Z, as well as A and Z.

    #Done when between function is functional. If you have "A B C D Z E Z B" and the between function references "A" as start and "Z" as end, it should return "A B C D Z."

    #References "scenario-start and scenario-end events" mentioned in Canvas.

    #Traceability: Method 'between': Design Document 4.2.1.2
    
    def between(self):
        data = self.dataLog  
        if(self.searchSettings.betweenFirst == ['']):
            return
        for i in range(len(self.searchSettings.betweenFirst)):
            betweenFirst = self.searchSettings.betweenFirst[i]
            betweenLast = self.searchSettings.betweenLast[i]
            betweenCol = self.searchSettings.betweenCol[i]
            firsts = data.index[data[betweenCol] == betweenFirst].tolist()
            lasts = data.index[data[betweenCol] == betweenLast].tolist()
            list = []
            m = 0
            n = 0
            twiceThrough = False
            while firsts[m] != None and lasts[n] != None:
                if (firsts[m] < lasts[n]):
                    for j in range(firsts[m], lasts[n] + 1):
                        list.append(j)
                while (firsts[m] < lasts[n] and m != len(firsts) - 1):
                    m += 1
                while (n != len(lasts) - 1):
                    n += 1
                if (twiceThrough == True):
                    break
                if (m == len(firsts) - 1 or n == len(lasts) - 1):
                    twiceThrough = True
        self.dataLog = self.dataLog.iloc[list]
