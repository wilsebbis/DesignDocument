from DataClasses.search_settings import SearchSettings
from Loafr import Loafr
import pandas

class Experiment():
	
	# This holds the general strucure of the main program. It is currently hard-coded for one input file: example_input.csv,
	# which is included in the LOAFR code pack. Currently, this main program executes our goal function:
		# Take in a file, find all items that have value 'dog', then return a formatted log file
	# All error checking is completed within the calls to these functions. Traceability to requirements expressed in the design file
	# are included in comments below. 
	
	# Load the Loafr program and search settings
	# This accounts for the 'set-up' portion of the program
    newLoafr = Loafr() 								#Traceability: Class 'Main Program': Design Document 4.2.1
    newSearch = SearchSettings()						#Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
	
    # Load and import data for a given file
    # Fills requirements for loading and importing data
    searchFileName = str(input("Enter in a search file to process: "))
    newSearch.Load(searchFileName)						#Traceability: Method 'Load': Design Document 4.2.2.2
    newLoafr.searchSettings = newSearch						#Traceability: Attribute 'SearchSettings': Design Document 4.2.1.1
    logFileName = str(input("Enter in a log file to process: "))
    newLoafr.dataLog = pandas.read_csv(logFileName)				#Traceability: Attribute 'DataLogList': Design Document 4.2.1.1

    # Apply all methods onto the csv file
    # Fills requirements for a search, sort and filter implementation
    newLoafr.search()								#Traceability: Method 'Search': Design Document 4.2.1.2
    newLoafr.sort()								#Traceability: Method 'Sort': Design Document 4.2.1.2
    newLoafr.filter()								#Traceability: Method 'Filter': Design Document 4.2.1.2
	
	# Generate a new file containing the results of the search, sort, and filter methods
	# Fills requirements for creating a new log file
    searchFileName = str(input("Enter in an export file name (don't include .csv ending or 'tests/'): "))
    newLoafr.exportLog("tests/" + searchFileName)				#Traceability: Method 'ExportLog': Design Document 4.2.1.2
	
	# Let the user know that MainProgram() is done executing
    print("Report created.")
