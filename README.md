# SOCIAL MARGINAL COST ($) USING EASIUR OUTPUT AND .NCF SMOKE EMISSIONS

The reduced complexity model EASIUR can find the marginal social costs {$/mtons} due to emissions for a given location in the United States. The EASIUR model can be found online and the contents can be downloaded. To find the social cost {$}, the EASIUR model is used along with a .ncf SMOKE file containing emissions. This project contains 3 major python scripts. The scripts are developed such that they can be used seperately or together depending on the data needed. The scripts can also be used in Visual Studio using the interactive window to see the output and DataFrames. 

This project specifically measures the social cost of EGUs in the United States. However, the scripts in this project can be used for any Longitude/Latitude within the EASIUR grid. The EASIUR grid is a 36km grid that spans across the USA. More information on the grid can be found in the [Easiur documentation](https://barney.ce.cmu.edu/~jinhyok/easiur/EASIUR-Tutorial-20050521-Jinhyok.pdf). 



This project uses SMOKE .ncf files to make the final social cost calculations. _emis20150101.ncf_ is a SMOKE file for a single day in January. _jan2015.ncf_ is an average of all SMOKE emissions for the month of January. The NCEA function of NCO was used to calculate the average of the SMOKE files. For this project, 31 daily SMOKE files for the month of January were averaged to make jan2015.ncf. The values in this file would be the average emissions for a single day in January. The files are too large for this repository but they can be downloaded from this [Google Drive](https://drive.google.com/drive/folders/1082GUrb6EhxLl5CNpQfqdv4CtyCrDKsF?usp=sharing). **If downloaded make sure the .ncf files are in the same current working directory as this repository.** 


EGUCEMS/EGUNONCEMS for 2015 are also included in this repository. Since the files were large they are in a .zip folder. They will need to be downloaded and the contents will need to be placed in the same directory as the scripts.


Also included in this repository is the output for the state of Texas. EGU files for Texas are included as well as the final output in the NCF_output folder. The .csv file for Texas EGUs are a little different. _In EGUdataextract.py, the skiprow will need to be commented out in the fileconfirm function definition_ if user decides to run the .csv file for Texas. 



### The following libraries are used: 
Pandas version 1.5.0

Numpy version 1.23.2

netCDF4 version 1.6.4

deepdish version 0.3.7

h5py version 3.9.0

pyproj version 3.6.0

os from Python version 3.10 

csv from Python version 3.10



# EGUdataextract.py
This python script extracts the Facility ID and Longitude/Latitude of EGUs in the USA. The data is an EQUATES dataset for SMOKE emissions. They can be easily found by requesting data access on the [EPA website](https://www.epa.gov/cmaq/equates). A short survey might be have to filled out or just submit an empty request. 

The data can also be found in this [Google Drive](https://drive.google.com/drive/folders/1vEm5bOimwqO1T9G_P3QLqJ2tw-kNqhAj). The files in this drive are in a tar.gz format. Once downloaded they will have to be unzipped to look at the contents. The content should consist of two main folders, inputs and scripts. 

The tar.gz downloaded folder will contain EGUCEMS and EGUNONCEMS in an Excel format. EGUCEMS are facilities that continiously monitor output and EGUNONCEMS are facilities that do not continiously monitor emissions. The files will contain information such as Facility ID, Zipcode, Facility Name, Longitude, Latitude, etc. 
_It must be converted to a .csv file for this script to work_. 


To find the Excel spreadsheet of EGUCEMS and EGUNONCEMS from the tar.gz file, navigate to input->ptegu->egucems/egunoncems


**Make sure to convert the spreadsheets to .csv and save them to the current working directory of the script**


The script takes the two .csv files (EGUCEMS and EGUNONCEMS), extracts Facility IDs and their corresponding Longitude/Latitude. The script also removes any duplicates and rounds the Longitude and Latitude value to the closest 0.001. The EGUCEMS/EGUNONCEMS record Longitude/Latitude for every facility but the values differ. Rounding to the nearest 0.001 ensures that all of the Longitude/Latitude values of the facilities are being considered. 

### Script Input
* EGUCEMS .csv file 
* EGUNONCEMS .csv file
* keyword for output file


The output of the script is a .csv file containing Facility ID, Longitude, and Latitude of the EGUs. The .csv file will placed in the current working directory. The naming of this .csv file will be dependent on the user. The script will ask for a keyword/name for the final output file.


Example: if keyword is 2015 -> 2015longlat.csv 



### If looking for specific location 
If the user needs data for a specific location, it is recommended to open the EGUCEMS/EGUNONCEMS data in Excel and filter based on zipcode. The file can then be saved as a .csv in the current working directory. 

** Depending on how filtered results are saved, skiprows in the definition fileconfirm will have to change ** 

### If only using 1 .csv file 
If the user is only using 1 .csv file to extract data from, then the script will need to be changed. It currently asks for EGUCEMS and EGUNONCEMS. The user can comment out the line that asks for the second file and change the combineDF function accordingly.


## Input Example 
<p align="center">     
<img width="1170" alt="image" src="https://media.github.ncsu.edu/user/11488/files/45180d9a-782a-4afd-8a97-483da710859f">
   </p>
   <h5 align="center">
Snippet of EGUCEMS in Excel
</h5>
                   


## Output Example
The output contains Facility_ID and Longitude/Latitude of the EGUs. This information is extracted from EGUCEMS/EGUNONCEMS. The output file of this script will most likely be the input file of EasiurShivani.py. An example of the output is shown below. 

<p align="center">
<img width="269" alt="image" src="https://media.github.ncsu.edu/user/11488/files/8ab0cda8-3b69-44b0-8667-a273cf24e08b">
  </p>
   <h5 align="center">
Facility_ID, Longitude, and Latitude of EGUs from EGUCEMS/EGUNONCEMS 
</h5>



# EasiurShivani.py
EasiurShivani.py contains the code from pyeasiur.py along with new functions created for this project. 
Multiple definitions are added such that a .csv file containing Longitude and Latitude can be parsed and the EASIUR model can derive the associated marginal cost ($/mton).

The EASIUR model can be downloaded online. The folder containg the code for the model is in a Google drive. It contains the python script pyeasiur.py along with the directories/subfolders it uses. For the scope of this project, those directories and subfolders containing data are used as well. In this GitHub repository, all Easiur contents are included except for pyeasiur.py. Since EasiurShivani.py contains the code from pyeasiur.py, it is not included. The user will not have to download anything from the Easiur Google drive but it is included under Links of Interest if needed. 


The script is automated, meaning that it will ask the user for the .csv file input containing Longitude/Latitude values to parse, the income year, and population year. The .csv file must be in the current working directory, if not then the full address will need to be entered into the input prompt. The current EASIUR model caps the dollar year at 2010 so the script does not ask for dollar year.
**Direct changes in the code will have to be made if the dollar year needs to be lower than 2010.**

### Script Input
* longitude/latitude .csv file (from EGUdataextract.py or other)
* population year
* income year
* keyword for output file


Once the user enters all of the inputs needed the script will run through the Longitude/Latitude values. It will convert those values to the EASIUR grid and calculate the corresponding social marginal costs for all of the emissions.

The output file will be placed in a folder called EasiurOutput. It will be a .csv file containing EASIUR values for PEC, SO2, NOX, and NH3 emission for ground, 150m, and 300m for all seasons including an annual average. The script will ask for a keyword for the final output report. 

Example: if keyword is 2015 -> 2015_EasiurReport.csv 



**If EGUdataextract.py is not used and a seperate .csv file is being used as the input for this script, make sure there is a unique Facility_ID column. It can be indexed (1,2,3,..etc) if data does not have applicable IDs**



## Input Example
The input will be a .csv containing at Facility ID, Longitude and Latitude. For this project, a .csv containing EGU Facility IDs and their Longitude/Latitude values are used. The input for this script is the output of EGUdataextract.py. An example is shown below. 

<p align="center">
<img width="269" alt="image" src="https://media.github.ncsu.edu/user/11488/files/8ab0cda8-3b69-44b0-8667-a273cf24e08b">
  </p>
   <h5 align="center">
.csv file containing EGU information (output report from EGUdataextract.py)
</h5>


## Output Example 
The output will be a .csv file in an output folder called EasiurOutput. The file will contain Facility_ID, Longitude, Latitude, Emissions values for Ground, 150m and 300m. A snippet of the output is shown below.

<p align="center">
<img width="793" alt="image" src="https://media.github.ncsu.edu/user/11488/files/8739c428-43e9-4d90-a54c-7ac3b4310d53">
  </p>
   <h5 align="center">
EASIUR Report of EGUs from 2015
</h5>
  


### Links of Interest 
[Easiur Tutorial](https://barney.ce.cmu.edu/~jinhyok/easiur/EASIUR-Tutorial-20050521-Jinhyok.pdf)

[Easiur Online Tool](https://barney.ce.cmu.edu/~jinhyok/easiur/online/)

[Easiur Background Information](https://barney.ce.cmu.edu/~jinhyok/easiur/)

[Easiur Google Drive](https://drive.google.com/drive/folders/1HQtREJ5MBDBM3wXYJNvQA_qkapZc91bX) (download if needed)



# NETcdf.py
### This script does 3 main things:
1. Convert Longitude/Latitude to the CMAQ grid (X,Y) 
2. Given a .ncf SMOKE file, extract emissions NH3, NOX, PEC, and SO2 for the given longitude/latitude. An output .csv report is created containing averages of the emissions (daily or monthly)
3. A final .csv report of social costs per longitude/latitude given a .ncf SMOKE file and EASIUR file 

### To run this script in its entirety, 2 files are needed:
1. A .ncf SMOKE file containing emissions/data to extract (from [Google Drive](https://drive.google.com/drive/folders/1082GUrb6EhxLl5CNpQfqdv4CtyCrDKsF?usp=sharing) or other)
2. EASIUR .csv report (from [EasiurShivani.py](https://github.ncsu.edu/spatel34/EASIUR/blob/main/README.md#easiurshivanipy) or other) 

This script is also automated, meaning it will ask for input from the user. 


### Script Input
* .ncf filename or path to extract emissions
* .csv Easiur report filename or path (most likely EasiurOutput/'keyword'EasiurReport.csv)
* Daily or Monthly analysis
* If monthly, how many days in a month? (Can also be used if doing analysis for a week or a set number of days)
* Keyword for output filename
* Season for analysis (winter, spring, summer, fall, or annual)
* Level for analysis (gnd, 150, or 300)

The output of this script will be 3 different .csv files. The first two are created once all the .ncf SMOKE emissions are extracted and calculated for the given analysis (daily or monthly). The files will be in both grams and mtons placed in the NCF_output folder in the current working directory. 
Once season and level of analysis is entered, the social costs for each emission at the given location is calculated. This file is also placed in the NCF_output folder. 

All functions in this script are created such that it can be used in Visual Studio or something similar. The function definitions returns Arrays or DataFrames containing data so it is easy for the user to see. The user would easily be able to use these functions with the Visual Studio interactive window if desired.

## Input Example 


<h3 align="center">
  EASIUR .csv File
</h3>
<p align="center">
<img width="859" alt="image" src="https://media.github.ncsu.edu/user/11488/files/8739c428-43e9-4d90-a54c-7ac3b4310d53">
  </p>
   <h5 align="center">
EASIUR Report of EGUs from 2015
</h5>


## Output Example

<h3 align="center">
  .csv SMOKE Emissions Averages
</h3>
<p align="center">
<img width="859" alt="image" src="https://media.github.ncsu.edu/user/11488/files/4da54d3f-62cb-484e-a9f7-2273717ea0e1">
  </p>
   <h5 align="center">
Monthly SMOKE Emission Averages for January 2015 in Grams
</h5>



<p align="center">
<img width="859" alt="image" src="https://media.github.ncsu.edu/user/11488/files/4abbbf02-bac2-4571-8cc3-10121b1efb40">
  </p>
   <h5 align="center">
Monthly SMOKE Emission Averages for January 2015 in Metric Tons
</h5>




<h3 align="center">
  Final Social Cost Report
</h3>
<p align="center">
<img width="859" alt="image" src="https://media.github.ncsu.edu/user/11488/files/b4df9168-8158-4fb3-a15f-2161d8e46be6">
  </p>
 <h5 align="center">
Social Cost Report of January 2015 Emissions 
</h5>



# Limitations


This project and the code contains some limitations. 
1. The SMOKE .ncf files has to be extracted from another source that is not in the EQUATES Google drive. If an average is needed, the user has to compute this using NCO functions within an HPC or the user's bash/terminal. Once the .ncf SMOKE file is computed, then it can be used in the script for this project.
2. The SMOKE .ncf files for this project all contain just one level, ground. The script was made under the assumption all SMOKE files would only have one level. If there are multiple levels, then the emissions array in NETcdf.py will have to stay as a 4D array. The script currently reshapes the emissions array into a 3D array and disregards the level dimension since it was one value throughout.
3. This project uses EASIUR code which has its own limitations. For example, the dollar year is capped at 2010 which would have to be taken into account when final dollar values are calculated for a year that is above 2010. 
4. EASIUR grid is 36kmx36km while the SMOKE/CMAQ grid is a 12km grid. CMAQ has a higher resolution, therefore more data. Since the two grids are not the same size, the final data is not as accurate as it could be.
5. The script assumes if the user does not use EGUCEMS/EGUNONCEMS, then they will use a .csv file containing some sort of Facility_ID and the Longitude/Latitude of interest. 
6. EGUdataextract.py is currently set up to extract EGU data from 2 .csv files. If more files are being used, the script will have to change accordingly. The functions are all set up and could be quickly changed to account for multiple files. 
7. NETcdf.py only extracts emissions for PEC, SO2, NO, NO2, and NH3. If other emissions need to be extracted from the SMOKE file, it will need to be added to the function EmissionArray and the changes will need to be made throughout the script. 



# Publications and Other Resources

### EASIUR Related Publications 
* [Reduced-form modeling](https://www.sciencedirect.com/science/article/pii/S1352231016303090?via%3Dihub)
* [Public Health Cost of Primary PM2.5](https://pubs.acs.org/doi/10.1021/acs.est.5b06125)
* [Comparison of Social Costs Derived from Reduced Complexity Models](https://iopscience.iop.org/article/10.1088/1748-9326/ab1ab5)

### Social Health Costs Due to Emissions
* [Social Health Costs in the USA from 2008-2017](https://iopscience.iop.org/article/10.1088/1748-9326/ac00e3)
* [Air Quality and Health Benefits from Coal Power Plants Closures in Texas](https://www.tandfonline.com/doi/full/10.1080/10962247.2018.1537984)
* [Power Sector Decarbonization in Texas](https://pubs.acs.org/doi/10.1021/acs.est.2c00881)


### NCO Resources 
* [Download Instruction on Bash](https://nco.sourceforge.net/#bld)
* [NCO Commands](http://research.jisao.washington.edu/data/nco/)

