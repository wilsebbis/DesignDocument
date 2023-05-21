# This gives you the number of things called "B" which have a F value of more than v (which is 10 in this case)
# and which are in between an A and a Z

#Specifically, it first gets the between function, which gives all values between A and Z,
#including the values of A and Z, but excluding everything not in between.
#Then, it searches for values of F > v. This applies to all values,
#So A's and Z's which are less than v will now disappear, so it is
#important to use between first and search second for the results to
#be correct. Then we export that log to show what the results are
#which we are grouping by. We then group by B and return the number
#of B values which meet the specifications. In this case, there
#are three B values which have F > v and come between an A and a Z.

from DataClasses.search_settings import SearchSettings
from Loafr import Loafr
import pandas

newLoafr = Loafr()
newSearch = SearchSettings()
newSearch.Load("groupbysearch.csv")
newLoafr.searchSettings = newSearch
newLoafr.dataLog = pandas.read_csv("groupbyinput.csv")
newLoafr.between()
newLoafr.search()
newLoafr.exportLog("tests/betweentest")
newLoafr.groupBy()
print(newLoafr.masterString)