#%%
"""
Shivani Patel 

Script Description: 
This python script takes longitude/latitude values and converts them to CMAQ grid values.
It also extracts information from a .ncf SMOKE file. Emissions of interest (NH3,NOX,PEC,SO2)
are put into an array and parsed. The emission values are converted such that they give
an average based on user input (daily average or monthly)

The output of this script will be a .csv file in NCF_output folder. The .csv will be the 
average values of the emissions given a time period

The script also takes EASIUR values and multiplies it with the .ncf SMOKE emissions
to get a social cost value ($). The output of this will be in a new folder called
NCF_output
"""
import numpy as np
import netCDF4
import pandas as pd
import os 



# %%
"""
Function Description
This section of code takes longitude and latitude values 
and converts to CMAQ grid values 

This section of the code is called on by the function longlatconversion
"""
from pyproj import Proj, transform

# Define the LCC projection based on parameters in the GRIDDESC file
lcc_proj = Proj(proj='lcc', lat_1=33, lat_2=45, lon_0=-97, lat_0=40)

# Convert projected coordinates to latitude and longitude
longitude, latitude = lcc_proj(-2556000, -1728000, inverse=True)


# Convert latitude and longitude to x and y in the projected coordinate system
def latlon_to_xy(lon,lat):
    return lcc_proj(lon, lat)

# Determine grid indices from projected coordinates
def xy_to_row_col(x, y, x_origin=-2556000, y_origin=-1728000, cell_size=12000):
    col = int((x - x_origin) / cell_size)
    row = int((y - y_origin) / cell_size)
    return row, col

#%%
"""
Function Description 

Input: .csv file containing long and lat of egu's 
        column title should be 'Longitude' and 'Latitude'
        (use Easiur report .csv since it contains facilityID, long,lat)
        (the .csv file output from dataextract.py can also be used)

Output: DF of facilityID/long/lat/gridX CMAQ/grixY CMAQ 
        all of the values are seperate dicts in this function and can be extracted
        if needed

This function goes through a file of long/lat and converts it to CMAQ grid values 
"""
#%%
def longlatconversion(filename):
    longlat=pd.read_csv(filename, usecols=['facility_id','Longitude','Latitude'])
    

    longitude=longlat['Longitude'].to_dict()
    latitude=longlat['Latitude'].to_dict()
    facility=longlat['facility_id'].to_dict()
    X={} #[] for list
    Y={} #[] for list
    gridx={}
    gridy={}
    i=0
   
    for i in longitude and latitude:
        X[i],Y[i]=latlon_to_xy(longitude[i],latitude[i]) #latitude/long to grid
        gridx[i],gridy[i]=xy_to_row_col(X[i],Y[i])
        gridx[i]=round(gridx[i])
        gridy[i]=round(gridy[i])

    return(facility,longitude,latitude,gridx,gridy)

"""
Function Description
Input: dict/list of FacilityID, long, lat, CMAQ xval, CMAQ yval 
Outout: compiles all of the dicts into a DF and labels them 
        Returns a DF with Facility ID,Long,Lat,Xval,Yval 
"""

def compilelonglattogrid(facility,long,lat,gridX,gridY):
    coordlist=[facility,long,lat,gridX,gridY]
    longlatgridDF=pd.DataFrame(coordlist)
    longlatgridDF=longlatgridDF.T
    longlatgridDF.rename(columns={longlatgridDF.columns[0]: "Facility_ID",longlatgridDF.columns[1]: "Longitude", longlatgridDF.columns[2]: "Latitude", longlatgridDF.columns[3]: "GridX", longlatgridDF.columns[4]: "GridY"},inplace=True)
    return(longlatgridDF)

#%%

"""
This section of the code has function definitions for the .ncf file 
"""



"""
Function Description 
Input: name or path of the .ncf file that will be analyzed 
Output: the function will print the dict keys (emissions) that are in this file 
This function is called in EmissionArray to double check that the file contains the 
emissions needed (double check)
"""
def NCFfile(filename):
    
    file = netCDF4.Dataset(filename,'r')
    keys=file.variables.keys()
    print(keys)
    return(file)


# extracts emission vals and turns them into array 
# 3D array with (time, x grid, y grid )
"""
Function Description 
Input: .ncf file to be analyzed 
Output: Arrays of the emissions (NOx,PEC,SO2,NH3)

This function extracts data of the emissions and turns it into a 3D array 
this file only contained ground emission information so that column of values 
was removed and a 3D array (25,299,459)=(time,Xgrid,Ygrid) was formed for each emission type 
NO2 and NO are added together to create NOX
"""
def EmissionArray(ncffile):

    file=NCFfile(ncffile)
    no2=file.variables['NO2']
    no=file.variables['NO']
    PEC=file.variables['PEC']
    so2=file.variables['SO2']
    nh3=file.variables['NH3']


    no2Array=np.array(no2)
    noArray=np.array(no)
    PECArray=np.array(PEC)
    SO2Array=np.array(so2)
    NH3Array=np.array(nh3)

    #lay is 1 
    # originally lay,tstep,x,y
    no2Array=np.reshape(no2Array,(25,299,459))
    noArray=np.reshape(noArray,(25,299,459))
    NOXArray=np.add(no2Array,noArray)
    PECArray=np.reshape(PECArray,(25,299,459))
    SO2Array=np.reshape(SO2Array,(25,299,459))
    NH3Array=np.reshape(NH3Array,(25,299,459))  

    return(NOXArray,PECArray,SO2Array,NH3Array)
#%%
#returns the average emission of the day per grid location
"""
Function Description:
This function takes a X,Y of CMAQ corresponding to the long/lat and extracts emission value
The function will add 24 values per X,Y for a daily emission average 
(use this function for each type of emission)

Input: Xgrid values and Y grid values from the compilelonglattogrid function
        also the emission type
Output: for each x and y grid value, emissions for 24hr is extracted and added
        for a daily average 

"""
def dailyemissionavg(Xgridvals,Ygridvals,em):
    vals={}
    dailyavg={}

    for i in range (len(Xgridvals)): 
        x=Xgridvals[i].astype(int)
        y=Ygridvals[i].astype(int)

      
        for j in range (0,24):
            vals[j]=em[j][x][y]
  

        
        dailyavg[i]=sum(vals.values())
    
        #avg value is of grid location for a day 

    return(dailyavg)

"""
Function Description:
This function takes the average emission for each XY for the day and then makes a 
complete DF depending on daily AVG or monthly AVG needed

Input: the different emissions averages from dailyemission function along with labels
        for the emission
        also asks if analysis is for daily for monthly 
Output: an average emission DF of all emissions/their labels


"""
def EmissionDF(em1,em2,em3,em4,label1,label2,label3,label4):
    avglist=[em1,em2,em3,em4]
    dailyAvgDF=pd.DataFrame(avglist)
    dailyAvgDF=dailyAvgDF.T
    dailyAvgDF.rename(columns={dailyAvgDF.columns[0]: label1.upper()+'_Daily', dailyAvgDF.columns[1]: label2.upper()+'_Daily', dailyAvgDF.columns[2]: label3.upper()+'_Daily', dailyAvgDF.columns[3]: label4.upper()+'_Daily'},inplace=True)
    avgType=input('Daily or Monthly averages?')
    if avgType.lower() == 'daily':
        dailyAvgDF=dailyAvgDF*86400
        return dailyAvgDF
    
    elif avgType.lower()=='monthly':
        days=input('How many days in the month?')
        days=int(days)
        monthlyAVGdf=dailyAvgDF*(days*86400)
        monthlyAVGdf.rename(columns={monthlyAVGdf.columns[0]: label1.upper()+'_Monthly', monthlyAVGdf.columns[1]: label2.upper()+'_Monthly', monthlyAVGdf.columns[2]: label3.upper()+'_Monthly', monthlyAVGdf.columns[3]: label4.upper()+'_Monthly'},inplace=True)
        return monthlyAVGdf

"""
Function Descpription:
This function creates an output folder in the current working directory
It also combines long/lat DF with the emission DF and converts to .csv

Input: DF from compilelonglattogrid DF and DF returned from EmissionDF

Output: .csv file in NCF_output file
        2 files: one in grams and another in tons
        returns the DF in tons so it can be used to multiply with EASIUR vals

"""
def compileDF(locationDF,AVGemissionDF,finalname):
    
    cwd=os.getcwd()
    path=os.path.join(cwd,'NCF_Output')

    finalDFgrams=pd.concat([locationDF,AVGemissionDF],axis=1)
    gramsoutput=finalname.capitalize()+'_NCF_Averages_grams.csv'
    finalDFgrams.to_csv(os.path.join(path,gramsoutput))
    
    gramstotons=1.0*(10**-6)
    AVGinTons=AVGemissionDF*gramstotons
    finalDFtons=pd.concat([locationDF,AVGinTons],axis=1)
    tonsoutput=finalname.capitalize()+'_NCF_Averages_tons.csv'
    finalDFtons.to_csv(os.path.join(path,tonsoutput))
    print('Output in folder NCF_output')
    return(finalDFtons)




#%%
"""
This section of the code contains function definitions that will 
multiply EASIUR vals (t/$) by .ncf emissions vals (g) to get a $ amount
"""


"""
Function Description 
Input: Easiur file to parse (this file should contain Easiur Values for all 
long/lat for the facilites. Comes from Easiur Code)
        ncfTONS is the DF of emissions values from .ncf file in Tons 
Output: a single .csv file of dollar amount corresponding to the season and level 

"""
def easiurfile(easiurfilename,ncfTONS,finalname):
    season=input('Enter season or annual to analyze EASIUR file: ')
    level=input('Enter level to analyze (Gnd, 150m, or 300m): ')
    analysis=level.capitalize()+'_'+season.capitalize()
    emList={
        0: 'PEC_',
        1: 'SO2_',
        2: 'NOX_', 
        3: 'NH3_',
    }
    easiurdata={} 
    namelist={}
    #the code above asks for level and season needed for analysis, using that info 
    #the loop will extract those specific columns and put them into easiurdata
    for i in emList: 
        easiurdata[i]=pd.read_csv(easiurfilename,usecols=[emList[i]+analysis])
        easiurdata[i]=pd.DataFrame(easiurdata[i])
        namelist[i]=emList[i]+analysis

    #easiurdata is combined into one and sorted alphabetically, 
    # ncfdata [5:9] is extracted and sorted alphabetically
    # ncfdata [0:3] is facility, long, lat 

    # the columns of easiur and ncf will be multiplied and inserted into multDF
    # facility,long,lat is added to multDF for a complete .csv 
    easiurdataDF=pd.concat([easiurdata[0],easiurdata[1],easiurdata[2],easiurdata[3]],axis=1)
    easiurdataDF=easiurdataDF.sort_index(axis=1)
    ncfdata=ncfTONS.iloc[:,5:9]
    ncfdata=ncfdata.sort_index(axis=1)
    ncflocation=ncfTONS.iloc[:,0:3]

    multDF=pd.DataFrame()

    for i in namelist:
 
        multDF[easiurdataDF.columns[i]]=ncfdata.iloc[:,i]*easiurdataDF.iloc[:,i]
   
   # .csv is created and added to ncf folder
    multDF=pd.concat([ncflocation,multDF],axis=1)
    print(multDF)
    cwd=os.getcwd()
    path=os.path.join(cwd,'NCF_Output')

    outputfilename=finalname.capitalize()+"_DollarVal_"+level+'_'+season.capitalize()+'.csv'
    multDF.to_csv(os.path.join(path,outputfilename))
    print('output .csv file is in NCF_Output folder')

    return(ncfdata,easiurdataDF,multDF)



# %%
"""
Main section of code
"""
# %%

filename=input('Enter .ncf filename or path: ')

nox,pec,so2,nh3=EmissionArray(filename)

# %%
#get facility_id/long/lat info from EASIUR file (can use report from dataextract.py if needed)
#run the file through longlatconversion function and then compile function

easiurfilename=input('Enter filename or path of EASIUR .csv report: ')


facility,long,lat,gridX,gridY=longlatconversion(easiurfilename)
coordDF=compilelonglattogrid(facility,long,lat,gridX, gridY)

#%%
#get xval and yval CMAQ for each long/lat and get the daily emissions 
noxavg=dailyemissionavg(coordDF['GridX'],coordDF['GridY'],nox)
pecavg=dailyemissionavg(coordDF['GridX'],coordDF['GridY'],pec)
so2avg=dailyemissionavg(coordDF['GridX'],coordDF['GridY'],so2)
nh3avg=dailyemissionavg(coordDF['GridX'],coordDF['GridY'],nh3)
# %%
#compile all the averages into a DF 
AVGdf=EmissionDF(noxavg,pecavg,so2avg,nh3avg,'NOX','PEC','SO2','NH3')
finaloutputname=input('Enter a keyword/name of final output files: ')

# %%
#compile coordinate/location DF and the average DF
#run it through this function to extract it into a .csv 
tonsDF=compileDF(coordDF,AVGdf,finaloutputname)

easiurfile(easiurfilename,tonsDF,finaloutputname)


