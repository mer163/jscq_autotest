#!/bin/python
#encoding=utf-8

import os
import logging
import sys

try:
    import xlrd
except:
    os.system('pip install -U xlrd')
    import xlrd

def readExcelBySheets(caseFile,sheetList):
    sheets = []
    file = os.path.join(os.getcwd(), caseFile)
    if not os.path.exists(file):
        logging.error("case file not exist")
        sys.exit()
    workbook = xlrd.open_workbook(caseFile)
    for i in range(len(sheetList)):
        try:
            sheet = workbook.sheet_by_index(int(sheetList[i]))  # 指定通过下标读取excelsheet表
        except Exception:
            sheet = workbook.sheet_by_name(sheetList[i])  # 指定通过名字读取excelsheet表
        sheets.append(sheet)

    return sheets



def readExcelByName(caseFile,sheetName):
    file = os.path.join(os.getcwd(), caseFile)
    if not os.path.exists(file):
        logging.error("case file not exist")
        sys.exit()
    workbook = xlrd.open_workbook(caseFile)
    sheet = workbook.sheet_by_name(sheetName)  # 指定读取excelsheet表
    return sheet


def readExcelAllSheets(caseFile):
    sheets = []
    file = os.path.join(os.getcwd(), caseFile)
    if not os.path.exists(file):
        logging.error("case file not exist")
        sys.exit()
    workbook = xlrd.open_workbook(caseFile)
    allSheets = workbook.sheets()
    return allSheets
