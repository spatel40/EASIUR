"""
Shivani Patel
11/25/2023
Code Description: 
This script will extract long/lat from a .csv file extracted online called egucems and egunoncems
Input: .csv file with emission information of facilites in the USA 
        file will have columns consisting of facility id/name/long/lat starting around row 7 
        egucems= continious emissions recording
        egunoncems=noncontinious emissions recording
Output: this code will output a .csv file keyword+longlat.csv into the current working directory

        
ALL functions are created such that they can be run in Python and the Dataframes
can be seen if any changes/additions need to be made
"""
#%%
import pandas as pd

"""
Function Description
Input: name of .csv file to parse (egucems/egunoncems)
        make sure .csv file is in the current working directory
        if not input needs to the full address
Function reads file and extracts Facility ID, Longitude, and Latitude
Longitude and Latitude values are rounded to the nearest 0.001
The resulting DF containing Facility ID, Long/Lat is returned

if only one file is being considered, follow this order: 
        fileconfirm->dropduplicates->converttocsv
if 2 or more files: all of the defs in order
"""
def fileconfirm(filename):

        longlat=pd.read_csv(filename, 
                            skiprows=7, # might have to change this depending on file, look at excel to make sure
                            usecols= ['facility_id','longitude','latitude'])
        longlatDF=pd.DataFrame(longlat)

        longlatDF.longitude=longlatDF.longitude.round(3)
        longlatDF.latitude=longlatDF.latitude.round(3)

        longlatDF.rename(columns={"longitude": "Longitude", "latitude": "Latitude"},inplace=True)

        return longlatDF
"""
Function Description
Input: Dataframe 1 and Dataframe 2 
The 2 dataframes corresponds to the 2 .csv files (egucems/egunoncems) that are returned
from the fileconfirm function above

Output: combines the DFs and returns a singular DF
** function can be changed to accomodate more than 2 DFs 
(just define them and add to the concat function)**
"""
def combineDF(DF1,DF2):
        combine=pd.concat([DF1,DF2])
        return combine
"""
Function Description
Input: dataframe resulting from the combineDF or fileconfirm function 
(dependent on number of .csv files to parse; more than 1 needs to go through 
combineDF)
This function drops duplicates by only keeping unique facility IDs
Output: dataframe with unique facility IDs/no duplicates
"""
def dropduplicates(DF):
        DF=DF.drop_duplicates(subset=['facility_id'])
        DF=DF.reset_index()
        return DF
"""
Function Description
Input: the Dataframe being converted to a .csv file with keyword of choice
Final .csv file will be named keyword+longlat.csv 
Output: dataframe in .csv format 
        output will be in the current working directory 
"""
def converttocsv(DF,name):
        DF.to_csv(name+'longlat.csv')
        print('Resulting .csv is in current working directory')

#%%
"""
main section of code
** make sure .csv with egu information in the current working directory 
if not, full address needs to be within quotations ** 
"""
cemsfile=input('Enter the cems .csv file name or path:')
noncemsfile=input("Enter the noncems .csf file name or path:")
finaloutput=input('Enter keyword/name for output file:')

cemsDF=fileconfirm(cemsfile)
noncemsDF=fileconfirm(noncemsfile)

combinedDF=combineDF(cemsDF,noncemsDF)


finalDF=dropduplicates(combinedDF)
converttocsv(finalDF,finaloutput)


# %%
