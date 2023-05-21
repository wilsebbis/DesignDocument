import unittest

from numpy.core.numeric import False_
from DataClasses.search_settings import SearchSettings
from Loafr import Loafr
import pandas                           #Traceability: 'Introduction': Design Document 2.1

# note all the tests are in this file beacuse of scoping issues in Visual Studio and we as a group would 
# like to have the tests for each class in their own seperate files
# but due to issues in Visual Studio all the tests will be contained in this file in order
# to allow for every class to be detected and not have twice as many files clogging up the file explorer

# the basic set and get variable test consitst of two parts, the first part for testing the 
# Default values of the constructor and the second part for testing non Default constructor options
# 'Def' will be added to the test names when the Default value of the constrctors is being tested

class Test_Search_Settings(unittest.TestCase):
    ss = SearchSettings()                                                                       #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
    fs = SearchSettings(["Dog"],["Operator"],["equal"],["Operator"],[True],["Product_type"],["Animals"],["Dog"],["Cat"],["Dog"],["Operator"])    #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
    
    def test_Default(self):
        self.assertEqual(self.ss.searchStrings, [])
        self.assertEqual(self.ss.searchCols, [])
        self.assertEqual(self.ss.lessGreatEqual, [])
        self.assertEqual(self.ss.sortColumns, [])
        self.assertEqual(self.ss.sortAscending, [])
        self.assertEqual(self.ss.filters, [])

    def test_Constructor(self):
        self.assertEqual(self.fs.searchStrings, ["Dog"])
        self.assertEqual(self.fs.searchCols, ["Operator"])
        self.assertEqual(self.fs.lessGreatEqual, ["equal"])
        self.assertEqual(self.fs.sortColumns, ["Operator"])
        self.assertEqual(self.fs.sortAscending, [True])
        self.assertEqual(self.fs.filters, ["Product_type"])
        self.assertEqual(self.fs.groupLabel, ["Animals"])
        self.assertEqual(self.fs.groupTerm, ["Dog"])
        self.assertEqual(self.fs.betweenFirst, ["Cat"])
        self.assertEqual(self.fs.betweenLast, ["Dog"])
        self.assertEqual(self.fs.betweenCol, ["Operator"])

    def test_Load(self):
        self.assertRaises(OSError, self.ss.Load, "invlid file path")
        self.assertRaises(FileNotFoundError, self.ss.Load, "empty file")
        self.ss.Load("example_search.csv")
        self.assertNotEqual(self.ss.searchStrings, [])
        self.assertNotEqual(self.ss.searchCols, [])
        self.assertNotEqual(self.ss.lessGreatEqual, [])
        self.assertNotEqual(self.ss.sortColumns, [])
        self.assertNotEqual(self.ss.sortAscending, [])
        self.assertNotEqual(self.ss.filters, [])
        self.assertNotEqual(self.fs.groupLabel, [])
        self.assertNotEqual(self.fs.groupTerm, [])
        self.assertNotEqual(self.fs.betweenFirst, [])
        self.assertNotEqual(self.fs.betweenLast, [])
        self.assertNotEqual(self.fs.betweenCol, [])

class Test_Lofar(unittest.TestCase):
    ss = SearchSettings()                                                               #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
    lofair = Loafr()
    hifair = Loafr(None,ss)

    fs = SearchSettings([9],["Serial_number"],["less"],["Operator"],[False],["Dog"])    #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
    lofar_wil = Loafr(searchSettings=fs)
    lofar_wil.dataLog = pandas.read_csv("test_input.csv")                               #Traceability: Attribute 'DataLog': Design Document 4.2.1.1

    def test_Default(self):
        fakefar=Loafr(dataLog=None)
        self.assertEqual(fakefar.dataLog, None)
        self.assertEqual(fakefar.searchSettings, None)

    def test_Constructor(self):
        self.assertEqual(self.hifair.dataLog, None)
        self.assertEqual(self.hifair.searchSettings, self.ss)                            #Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1

    # Proves that the length of the pandas database we read in isn't 0, therefore it isn't empty
    # Whereas the empty pandas database is length 0
    def test_importDataChange(self):
         lofairInput = Loafr()
         lofairInput.dataLog = pandas.read_csv("test_input.csv")                        #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
         self.assertNotEqual(len(lofairInput.dataLog),0)                                #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
         self.assertEqual(len(pandas.DataFrame()),0)

    def test_importDataValid(self):
        lofairInput = Loafr()
        lofairInput.dataLog = pandas.read_csv("test_input.csv")                         #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
                
        testData= {
            "TestNum":["Test1","Test2",],
            "Product_type":["Bone toy","Ball toy"],
            "Serial_number":[12347565.0,8.7],
            "Testing_Environment":["Park","Pool"],
            "Test_start_time":[float('nan'),float('nan')],
            "Test_end_time":[float('nan'),float('nan')],
            "Test_output":["Squeek","Bork"],
            "Passed":[1,0],
            "Operator":["backwards dog","Dog"]        
        }
        
        dataLogTable=pandas.DataFrame(data=testData)
        pandas.testing.assert_frame_equal(lofairInput.dataLog,dataLogTable)

    def test_search(self):
        lofarSearch=Loafr(searchSettings=self.fs)
        lofarSearch.dataLog = pandas.read_csv("test_input.csv")                          #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
        lofarSearch.search                                                               #Traceability: Method 'Search': Design Document 4.2.1.2

        testData= {
            "TestNum":["Test1","Test2",],
            "Product_type":["Bone toy","Ball toy"],
            "Serial_number":[12347565.0,8.7],
            "Testing_Environment":["Park","Pool"],
            "Test_start_time":[float('nan'),float('nan')],
            "Test_end_time":[float('nan'),float('nan')],
            "Test_output":["Squeek","Bork"],
            "Passed":[1,0],
            "Operator":["backwards dog","Dog"]        
        }

        searchFile=pandas.DataFrame(data=testData)
        pandas.testing.assert_frame_equal(lofarSearch.dataLog,searchFile)

    def test_sort(self):
        lofarSort=Loafr(searchSettings=self.fs)
        lofarSort.dataLog = pandas.read_csv("test_input.csv")                           #Traceability: Attribute 'DataLog': Design Document 4.2.1.1
        lofarSort.sort                                                                  #Traceability: Method 'Sort': Design Document 4.2.1.2

        testData= {
            "TestNum":["Test1","Test2",],
            "Product_type":["Bone toy","Ball toy"],
            "Serial_number":[12347565.0,8.7],
            "Testing_Environment":["Park","Pool"],
            "Test_start_time":[float('nan'),float('nan')],
            "Test_end_time":[float('nan'),float('nan')],
            "Test_output":["Squeek","Bork"],
            "Passed":[1,0],
            "Operator":["backwards dog","Dog"]        
        }

        sortFile=pandas.DataFrame(data=testData)

        pandas.testing.assert_frame_equal(lofarSort.dataLog,sortFile)

    def test_filter(self):
        lofarFilter=Loafr(searchSettings=self.fs)

        lofarFilter.dataLog=pandas.read_csv("test_input.csv")                           #Traceability: Attribute 'DataLog': Design Document 4.2.1.1

        lofarFilter.filter                                                              #Traceability: Method 'Filter': Design Document 4.2.1.2

        testData= {
            "TestNum":["Test1","Test2",],
            "Product_type":["Bone toy","Ball toy"],
            "Serial_number":[12347565.0,8.7],
            "Testing_Environment":["Park","Pool"],
            "Test_start_time":[float('nan'),float('nan')],
            "Test_end_time":[float('nan'),float('nan')],
            "Test_output":["Squeek","Bork"],
            "Passed":[1,0],
            "Operator":["backwards dog","Dog"]        
        }
        
        filterFile=pandas.DataFrame(data=testData)

        pandas.testing.assert_frame_equal(lofarFilter.dataLog,filterFile)

    def test_groupBy(self):
        groupSearch = SearchSettings([''],[''],[''],[''],[''],[''],["Type"],["B"],["A"],["Z"],["Type"])  
        lofarGroup=Loafr(searchSettings=groupSearch)
        lofarGroup.dataLog = pandas.read_csv("groupbyinput.csv")

        lofarGroup.groupBy()        

    def test_between(self):
        groupSearch = SearchSettings([''],[''],[''],[''],[''],[''],["Type"],["B"],["A"],["Z"],["Type"])  
        lofarBetween=Loafr(searchSettings=groupSearch)
        lofarBetween.dataLog = pandas.read_csv("groupbyinput.csv")
        
        lofarBetween.between()

        testData= {
            "Type":["A","A","B","B","Z","A","B","Z"],
            "F":["10","12","17","19","6","3","22","17"],  
        }

        betweenFile=pandas.DataFrame(data=testData)

        pandas.testing.assert_frame_equal(lofarBetween.dataLog,betweenFile)

    def test_groupBy_null(self):
        groupSearch = SearchSettings([],[],[],[],[],[],[''],[''],[''],[''],[''])  
        lofarGroupNull=Loafr(searchSettings=groupSearch)
        lofarGroupNull.dataLog = pandas.read_csv("groupbyinput.csv")

        testData=lofarGroupNull.dataLog

        lofarGroupNull.groupBy()

        pandas.testing.assert_frame_equal(lofarGroupNull.dataLog,testData)

    def test_between_null(self):
        groupSearch = SearchSettings([],[],[],[],[],[],[''],[''],[''],[''],[''])  
        lofarBetweenNull=Loafr(searchSettings=groupSearch)
        lofarBetweenNull.dataLog = pandas.read_csv("groupbyinput.csv")

        testData=lofarBetweenNull.dataLog

        lofarBetweenNull.between()

        pandas.testing.assert_frame_equal(lofarBetweenNull.dataLog,testData)
        

    def test_exportLog(self):
        self.assertEqual(self.lofar_wil.exportLog("tests/here"), None)

    def test_generateReport(self):
        # shows that new report can always be made because it will be named with number
        self.assertEqual(self.lofair.generateReport("tests/example_output"),None)

if __name__ == '__main__':
     with open('tests/log_file.txt','w') as out:
         runner = unittest.TextTestRunner(out)
         unittest.main(testRunner=runner)
