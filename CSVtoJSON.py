#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:19:29 2022

@author: berkoztas

"""
#Sukru Berk Oztas 2019510096
from blist import sorteddict
import csv
import json

def columnName(query,keys,SQLstatement):
    #method to split columnname
    beforeFrom=query.find("FROM")
    column_name=query[len(SQLstatement)+1:beforeFrom-1].strip()
    #slices string between SELECT and FROM
    if column_name=="ALL":
        return "ALL"
    for i in range(len(keys)):
        if column_name==keys[i]:
            return keys[i]
    else:
        return print("Column name invalid.")
    
def filterName(query,keys,SQLstatement):
    #method to split filer after WHERE statement
    beforeWhere=query.find("WHERE")
    afterWhere=beforeWhere+6
    if SQLstatement=="SELECT":
        if "ORDER BY" in query:
            beforeOrder=query.find("ORDER BY")
            where_column=query[afterWhere:beforeOrder-1].strip()
        else:
            return print("ORDER BY statement is missing")
    else:
        where_column=query[afterWhere:].strip()
    split=where_column.split()
    for i in range(len(keys)):
        if split[0]==keys[i]:
            return where_column
          
    return print("Filter statement after WHERE invalid")

def filterNameAndOr(query,keys,SQLstatement):
    if "AND" in query:
        indexAfter=query.find("AND")
        indexAfter=indexAfter+4
    elif "OR" in query:
        indexAfter=query.find("OR")
        indexAfter=indexAfter+3
    if SQLstatement=="SELECT":
        if "ORDER BY" in query:
            beforeOrder=query.find("ORDER BY")
            filter2=query[indexAfter:beforeOrder-1].strip()
        else:
            return print("ORDER BY statement is missing")
    else:
        filter2=query[indexAfter:].strip()
    split=filter2.split()
    for i in range(len(keys)):
        if split[0]==keys[i]:
            return filter2
   

def Filter(filtername,filter_column,sorted_records):
    #Method to filter dictionary according to filtername
    split=filtername.split()
    #split[1] is operators
    filteredID=[]
    if split[1]== "=":
        for i in sorted_records:
            if sorted_records[i][filter_column]== split[2]:
                filteredID.append(sorted_records[i])
    elif split[1]== "!=":
        for i in sorted_records:
            if sorted_records[i][filter_column]!= split[2]:
                filteredID.append(sorted_records[i])
    elif split[1]== "<":
        for i in sorted_records:
            if sorted_records[i][filter_column] < split[2]:
                filteredID.append(sorted_records[i])
    elif split[1]== ">":
        for i in sorted_records:
            if sorted_records[i][filter_column]> split[2]:
                filteredID.append(sorted_records[i])
    elif split[1]== "<=":
        for i in sorted_records:
            if sorted_records[i][filter_column]<= split[2]:
                filteredID.append(sorted_records[i])
    elif split[1]== ">=":
        for i in sorted_records:
            if sorted_records[i][filter_column]>= split[2]:
                filteredID.append(sorted_records[i])
    elif split[1]== "!<":
        for i in sorted_records:
            if not sorted_records[i][filter_column] < split[2]:
                filteredID.append(sorted_records[i])
    elif split[1]== "!>":
        for i in sorted_records:
            if not sorted_records[i][filter_column]> split[2]:
                filteredID.append(sorted_records[i])
    return filteredID

def Select(columnname,filtered_ids,sorted_records):
    #Method to Select and print Filtered Dictionary
    Selected=[]
    if columnname== "ALL":
        for i in range(len(filtered_ids)):
            filtered_id=int(filtered_ids[i]['id'])
            Selected.append(sorted_records[filtered_id].values())
    elif columnname=="id":
        for i in range(len(filtered_ids)):
            filtered_id=int(filtered_ids[i]['id'])
            Selected.append(int(sorted_records[filtered_id][columnname]))
    elif columnname=="grade":
        for i in range(len(filtered_ids)):
            filtered_id=int(filtered_ids[i]['grade'])
            Selected.append(int(sorted_records[filtered_id][columnname]))
            
    else:
        for i in range(len(filtered_ids)):
            filtered_id=int(filtered_ids[i]['id'])
            Selected.append(sorted_records[filtered_id][columnname])
    return Selected

def Order(query,returnList,columnname):
    #Ordering the dictionary in acsending or decsending order
    words=query.split()
    if words[-3]=="ORDER":
        if words[-2]=="BY":
            if not columnname=="ALL":
                if words[-1]=="ASC":
                    returnList.sort()
                elif words[-1]=="DSC":
                    returnList.sort(reverse=True)
                else:
                    "ORDER Statement is invalid."
           # else:
    return returnList
                
def delete(filtered_ids,sorted_records):
    #Deleting according to the id
    for i in range(len(filtered_ids)):
        filtered_id=int(filtered_ids[i]['id'])
        del sorted_records[filtered_id]
    return sorted_records
    

def insert(SQLvalues,sorted_records):
    #Insert Statement
    SQLvalues=SQLvalues[1:-1]
    valueList=SQLvalues.split(",")
    if len(valueList)==5:
        ID=int(valueList[0])
        sorted_records[ID]['id']=ID
        sorted_records[ID]['name']=valueList[1]
        sorted_records[ID]['lastname']=valueList[2]
        sorted_records[ID]['email']=valueList[3]
        sorted_records[ID]['grade']=valueList[4]
        
    else:
        return print("There must be 5 values.")
    return sorted_records
    
        
def selectValidation(query,keys,sorted_records):
    #Calling above methods after validatin syntax
    SQLstatement="SELECT"
    if "FROM" in query:
        if "WHERE" in query:
            if "STUDENTS" in query:
                Selected=[]
                returnList= []
                columnname=columnName(query,keys,SQLstatement)
                filtername=filterName(query,keys,SQLstatement)
                filters=filtername.split()#list of each word
                filter_column=filters[0]#column_name
                filtered_ids=Filter(filtername,filter_column,sorted_records)
                Selected=Select(columnname, filtered_ids, sorted_records)
                returnList=Selected
                
                if " AND " in filtername or " OR " in filtername:
                    Selected2=[]
                    
                    filter2=filterNameAndOr(query,keys,SQLstatement)
                    filters2=filter2.split()
                    filter_column2=filters2[0]
                    filtered_ids2=Filter(filter2,filter_column2,sorted_records)
                    Selected2=Select(columnname,filtered_ids2,sorted_records)
                    if "OR" in filtername:
                        returnList=list(set(Selected) | set(Selected2))
                    elif "AND" in filtername:
                        for i in range(len(Selected2)):
                            if Selected2[i] in Selected:
                                returnList.append(Selected2[i])
                    
            else:
                return print("Table name is invalid")
        else:
            return print("WHERE statements is missing")
    else:
        return print("FROM statement is missing.")
    OrderedList=Order(query,returnList,columnname)
    
    OrderedDictList=[dict(zip([columnname],[i])) for i in OrderedList]
    
    
    return OrderedDictList
        
    
        
def insertValidation(query,keys,sorted_records):
    #calling insert method after validating syntax
    #SQLstatement="INSERT"
    words=query.split()
    if words[1]=="INTO":
        if words[2]=="STUDENTS":
            if words[3].startswith("VALUES"):
                sorted_records=insert(words[4],sorted_records)
            else:
                print("Syntax is wrong.")
    return sorted_records
    
def deleteValidation(query,keys,sorted_records):
    #calling delete method after necessary filters
    SQLstatement="DELETE"
    if "FROM" in query:
        if "WHERE" in query:
            if "STUDENTS" in query:
                #columnname=columnName(query,keys,SQLstatement)
                filtername=filterName(query,keys,SQLstatement)
                filters=filtername.split()#list of each word
                filter_column=filters[0]#column_name
                filtered_ids=Filter(filtername,filter_column,sorted_records)
                sorted_records=delete(filtered_ids,sorted_records)
                
                
            else:
                print("Table name is invalid.")
        else:
            print("WHERE statements is missing")
    else:
        print("FROM statement is missing.")
    return sorted_records

file=open("students.csv")
csvreader=csv.DictReader(file,delimiter=';')
records=list(csvreader)
ids=[]
keys=list(records[0].keys())
print(keys)

for row in range(len(records)):
    ids.append(int(records[row]['id']))
    #recording ids in a list


sorted_records=sorteddict(zip((ids), (records)))



flag=True
while(flag):
    query=input("Enter a query: ")
    if query=="exit":
        with open("sorted.json", "w") as outfile:
            json.dump(dict(sorted_records), outfile)
        quit()
    if query.startswith("SELECT"):
        Selection=selectValidation(query,keys,sorted_records)
        print(Selection)
        with open("sample.json", "w") as outfile:
            json.dump(Selection, outfile)
       
        
    elif query.startswith("INSERT"):
        insertValidation(query,keys,sorted_records)
        
    elif query.startswith("DELETE"):
        deleteValidation(query,keys,sorted_records)
        
    else:
        print("Please use one of the SELECT, INSERT or DELETE statements.")





