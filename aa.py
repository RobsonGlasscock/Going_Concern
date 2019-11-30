%reset -f
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# I teach undergraduate and graduate Auditing and wanted to update my lecture examples of various audit report modifications. In my opinion, showing students real life examples of various audit reports is more effective than just looking at textbook examples. All of my prior example audit reports with going concern an dual dated audit reports are prior to 2014 and are now obsolete as the public company audit report format has changed. The goal of this code is to find current examples of going concern and dual dated audit reports using the Audit Analytics Audit Opinions data.


# Code below read in the first 10 rows of the data since this file is huge. I am just doing visual inspections here before further processing.
# An error is thrown wihtout including: 'encoding= 'ISO-8859-1''
# https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python.

df= pd.read_csv("aa_opinions.csv", nrows= 10, encoding = "ISO-8859-1")
df.head(2)
df.columns

###################### Exceprts from the Audit Analytics Data Dictionaries ##########################################
# Additional Signature Date 1;	additional_signature_date_1;	Date of the first opinion signature note. (i.e. March 6, 20XX, except for note 17 which is April 10, 20XX)

# Going Concern;	going_concern;	Indicates the going concern assumption has been qualified by the auditor. ** see notes**

# AUDIT_OPINIONS;	NOTE_1_DATE	NOTE_1_DATE	Y;	char(10)	N/A	Date of first opinion signature note - This field is not guaranteed to be an accurate date

# Is Additional Opinion;	is_additional_opinion;	Identifies additional opinions for the same period by the same auditor.

###################################################################################################################

# Per the above, it appears that additional_signature_date_1 will identify dual dated audit reports and going_concern will identify going concern report modifications. Each of these is shown as being lower-case variable names in the data dictionary, but the output of df.columns above outputs all caps column names.

# Note that data dictionary has "audit_opinion_key" and "fiscal_year_of_opinion", but these are both shortened to "op"
# in the actualy data. Due to these differences, I am goign to look at an alphabetically sorted list of column names.
list=[]
for i in df.columns:
    print(i)
    list.append(i)

# sort the list
list.sort()

print(list)




# The variables "IS_ADDITIONAL_OPINION", "ADDITIONAL_SIGNATURE_DATE_1", and "NOTE_1_DATE" are not in this dataset.However, "GOING_CONCERN" is present.

# Pull in data to identify going concern opinions.
df= pd.read_csv("aa_opinions.csv", usecols=["COMPANY_FKEY", "BEST_EDGAR_TICKER", "NAME", "SIC_CODE_FKEY", "FISCAL_YEAR_OF_OP", "FILE_DATE", "GOING_CONCERN"], encoding = "ISO-8859-1")

# Summary stats for the fiscal year of the opinions.
df['FISCAL_YEAR_OF_OP'].describe()

# Convert all column names to lowercase.
df.columns= df.columns.str.lower()

# Shape gives the rows and cols dimensions of the df.
df.shape

# look at values for going_concern and file date.
df['going_concern'].value_counts()
df['file_date'].value_counts()

df.info()

# Above, actual file dates are all over the place. Isolate search to the year.
df['fiscal_year_of_op'].value_counts()

# Create a boolean if the year is 2017
df['bool']=df['fiscal_year_of_op']==2017

df['bool'].value_counts()

# Create a second dataframe with only 2017 opinions
df2= df[(df['bool']==1)]

# look at values of the opinion and going_concern on the new dataframe.
df2['fiscal_year_of_op'].value_counts()
df2['going_concern'].value_counts()

# Examine rows where going_concern is not equal to zero (i.e., firms with going concern opinions) that have non-missing ticker values.
df2[['company_fkey', 'best_edgar_ticker', 'file_date', 'going_concern']].loc[(df['going_concern']!=0) & (df['best_edgar_ticker'].notnull())]

# Use the below example of a modern going concern audit report modification for class.
# https://www.sec.gov/Archives/edgar/data/1505512/000162828018002874/rgls20171231-10k.htm
