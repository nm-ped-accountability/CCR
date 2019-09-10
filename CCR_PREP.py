# Jeanho Rodriguez
# 08.22.2019
# CCR

import pandas as pd
import numpy as np

# how to set display
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# increase column width
pd.set_option('display.max_colwidth', 1000)

# Stack Perkins_Files
df_CTE_151617 = pd.ExcelFile("Perkins Student Listing_SY1617_15CAR.xlsx")
df_CTE_151617 = df_CTE_151617.parse("Perkins Student Listing_SY1617_")
# N = 100361
df_CTE_1718 = pd.read_csv('Perkins Student Listing_SY1718CAR.csv',header=0, low_memory=False,encoding = 'unicode_escape')
# N = 100454
df_CTE_1518 = pd.concat([df_CTE_151617,df_CTE_1718])
# N = 200815

# Rename Variable
df_CTE_1518.rename(columns={'Student_ID':'STID'}, inplace=True)

# Keep specified columns
df_CTE_1518 = df_CTE_1518[['STID','CAR_Indicator_2S1_Denominator','CAR_Indicator_2S1_Numerator']]

#Select students who completed CTE.
#2S1=Technical Skill Attainment.
#2S1 Numerator=# of CTE concentrators who completed their program in a course sequence and earned a cumulative GPA of C (2.0) or better in their technical coursework.
#2S1 Denominator=# of CTE concentrators who completed their programs in a course sequence.
df_CTE_1518 = df_CTE_1518[df_CTE_1518.CAR_Indicator_2S1_Denominator == 1.0]


# Denominator = 14144
# Numerator = 13220 / 924
# N = 14144 with Dupes


# Remove Duplicates
df_CTE_1518= df_CTE_1518.groupby(['STID','CAR_Indicator_2S1_Denominator','CAR_Indicator_2S1_Numerator']).first().reset_index()
# Denominator = 14125
# Numerator = 13201 / 924
# N = 14125 No Dupes


df_CTE_1518['Success'] = str
df_CTE_1518['Test'] = 'CTE'
df_CTE_1518['Score'] = int
df_CTE_1518.loc[df_CTE_1518['CAR_Indicator_2S1_Numerator'] == 1.0, 'Score'] = 100
df_CTE_1518['Subtest'] = str
df_CTE_1518.loc[df_CTE_1518['CAR_Indicator_2S1_Numerator'] == 1.0, 'Success'] = '1'


# Dual Credit Report  N = 194780
df_DC_1415 = pd.ExcelFile("Dual Credit District School Student 4 Digit Course With Grades List_SY1415.xlsx")
df_DC_1415 = df_DC_1415.parse("Dual Credit District School Stu")
# N = 32300

df_DC_1516 = pd.ExcelFile("Dual Credit District School Student 4 Digit Course With Grades List_SY1516.xlsx")
df_DC_1516 = df_DC_1516.parse("Dual Credit District School Stu")
# N = 37519

df_DC_1617 = pd.ExcelFile("Dual Credit District School Student 4 Digit Course With Grades List_SY1617.xlsx")
df_DC_1617 = df_DC_1617.parse("Dual Credit District School Stu")
# N = 40460

df_DC_1718_40 = pd.read_csv('Dual Credit District School Student 4 Digit Course With Grades List_SY1718_40D.csv',header=0, low_memory=False,encoding = 'unicode_escape')
# N = 21443

df_DC_1718_80 = pd.read_csv('Dual Credit District School Student 4 Digit Course With Grades List_SY1718_80D.csv',header=0, low_memory=False,encoding = 'unicode_escape')
# N = 21162

df_DC_1718_120 = pd.read_csv('Dual Credit District School Student 4 Digit Course With Grades List_SY1718_120D.csv',header=0, low_memory=False,encoding = 'unicode_escape')
# N = 19825

df_DC_1718_EOY = pd.read_csv('Dual Credit District School Student 4 Digit Course With Grades List_SY1718_EOY.csv',header=0, low_memory=False,encoding = 'unicode_escape')
# N = 22071


df_DC_1718 = pd.concat([df_DC_1718_40,df_DC_1718_80,df_DC_1718_120,df_DC_1718_EOY])
# N = 84501

# Collection Years - not sure if I'll need later
#df_DC_1415['SY'] = '2015'
#df_DC_1516['SY'] = '2016'
#df_DC_1617['SY'] = '2017'
#df_DC_1718['SY'] = '2018'

df_DC_1518 = pd.concat([df_DC_1415,df_DC_1516,df_DC_1617,df_DC_1718])
# N = 194780

df_DC_1518 = df_DC_1518[['Student_ID','State_Course_ID','State_Course_Name','District_Course_Name','Snap_40_day_low_grade',
                         'Snap_40_day_high_grade','Snap_40_day_grade_count','Snap_80_day_low_grade','Snap_80_day_high_grade',
                         'Snap_80_day_grade_count','Snap_120_day_low_grade','Snap_120_day_high_grade','Snap_120_day_grade_count',
                         'Snap_EOY_low_grade','Snap_EOY_high_grade','Snap_EOY_grade_count','Grade_High','Grade_Count']]

df_DC_1518['Numeric_Grade'] = int


# Mapping Function
score_map = {'A':95,'B':85,'C':75,'D':65,'F':55,'':1,'NaN':1,'not rptd':1,'Withdrawal':1,'Incomplete':1,'N':1,'I':1,'S':1}

df_DC_1518['Numeric_Grade'] = df_DC_1518['Grade_High'].map(score_map) #map function applied with map rules

df_DC_1518 = df_DC_1518[df_DC_1518.Numeric_Grade != 1]


df_DC_1518.rename(columns={'Student_ID':'STID'}, inplace=True)

df_DC_1518 = df_DC_1518.groupby(['STID','State_Course_ID','Numeric_Grade']).first().reset_index()

df_DC_1518['Test'] = 'DUAL'
df_DC_1518['Subtest'] = str
df_DC_1518['Success'] = str

df_DC_1518.rename(columns={'Numeric_Grade':'Score'}, inplace=True)

print(df_DC_1518.info())
#df_DC_1518 = df_DC_1518[['STID','Test','Subtest','Score','Success']]


# Stack List Assessment Tests
df_AT_1415 = pd.ExcelFile("List Assessment Tests_SY1415.xlsx")
df_AT_1415 = df_AT_1415.parse("List Assessment Tests")
# N = 125457

df_AT_1516 = pd.ExcelFile("List Assessment Tests_SY1516.xlsx")
df_AT_1516 = df_AT_1516.parse("List Assessment Tests")
# N = 96128

df_AT_1617 = pd.ExcelFile("List Assessment Tests_SY1617.xlsx")
df_AT_1617 = df_AT_1617.parse("List Assessment Tests")
# N = 97483

df_AT_1718 = pd.read_csv('List Assessment Tests_SY1718.csv',header=0, low_memory=False,encoding = 'unicode_escape')
# N = 96816


# SY Not sure we will need later
#df_AT_1415['SY'] = '2015'
#df_AT_1516['SY'] = '2016'
#df_AT_1617['SY'] = '2017'
#df_AT_1718['SY'] = '2018'

df_AT_1518 = pd.concat([df_AT_1415,df_AT_1516,df_AT_1617,df_AT_1718])
# N = 415884


df_AT_1518.rename(columns={'Student_ID':'STID'}, inplace=True)
df_AT_1518.rename(columns={'Assessment_ID':'Test'}, inplace=True)
df_AT_1518.rename(columns={'Subtest_Identifiers':'Subtest'}, inplace=True)
df_AT_1518.rename(columns={'Raw_Score':'Score'}, inplace=True)


df_AT_1518 = df_AT_1518.reset_index() # fixes the ValueError: Cannot reindex from duplicate axis

df_AT_1518.loc[df_AT_1518['Scaled_Score'] >= df_AT_1518['Score'], 'Score'] = df_AT_1518['Scaled_Score']
df_AT_1518['Success'] = str
df_AT_1518 = df_AT_1518.loc[df_AT_1518['Score'] == df_AT_1518['Scaled_Score']]

#print(df_AT_1518['Score'].value_counts())

df_AT_1518 = df_AT_1518[['District_Code','Location_ID','STID','Test','Subtest','Score','Success']]
print(df_AT_1518.head(3))
#df_CTE_1518 = df_CTE_1518[['District_Code','']]
#print(df_AT_1518.info())
#print(df_DC_1518.info())
#print(df_CTE_1518.info())

#All_CCR = pd.concat(df_AT_1518,df_DC_1518,df_CTE_1518)

#print(All_CCR.info())












