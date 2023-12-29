##########################################################
# Imports.
import sys
import System
import traceback
import clr
import os
import datetime
import shutil
import itertools
import time
import hashlib
from timeit import default_timer as timer
##########################################################
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
##########################################################
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
##########################################################
clr.AddReference('System')
from System.Collections.Generic import List
from System import String
##########################################################
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)
##########################################################
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
####################################################################################################
# Assign document, documentUI, application.
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
app = doc.Application
####################################################################################################
# Append the path to the RevitFamilyClass module then import it.
sys.path.append(r'D:\Dropbox\Work_Shared\UTILITY_FILES\Dynamo\PythonNodeScripts\Resources')
from RevitFamilyClass import *
####################################################################################################
# Get all inputs from the dynamo script.
INPUTFAMILIES = UnwrapElement(IN[0])
####################################################################################################
# LOG Variable for outputs.
OUTPUTLOG = []
# Error check trigger.
ERRORTRIGGER = False
# Creation trigger.
CREATETRIGGER = False
# Timer Log.
TIMERLOG = []
# Create variables for timing the script.
TIMERSTART = None
TIMEREND = None
# Temporary output. No purpose in function of script.
TEMPOUT = []
#
PARAMETERCOUNT = []
#
PARAMETERNAMES = []
#
BASICDATAEXPORT = []
#
FULLDATAEXPORT = []
#
PARAMETERLIST = []
####################################################################################################
# Define functions for the script.

def StartTimeItTimer():
    global TIMERSTART
    TIMERSTART = timer()
    
def EndTimeItTimer(name,output):
    global TIMEREND
    TIMEREND = timer()
    output.append((name,TIMERSTART-TIMEREND))

def Collect_ElementsByClass(Document,RevitClass,OutputList):
    CollectorObject = FilteredElementCollector(Document)
    FilterObject = ElementClassFilter(RevitClass)
    Objects = CollectorObject.WherePasses(FilterObject).ToElements()
    OutputList.append(Objects)

class FamilyOption(IFamilyLoadOptions):
    def OnFamilyFound(self,familyInUse,overwriteParameterValues):
		overwriteParameterValues = True
		return True
		
    def OnSharedFamilyFound(self, sharedFamily, familyInUse, FamilySource, overwriteParameterValues):
		return True
####################################################################################################
StartTimeItTimer()
####################################################################################################
SPFILE = app.OpenSharedParameterFile()
SPDEFS = list(itertools.chain(*[groups.Definitions for groups in SPFILE.Groups]))
SPDEFS_DICT = {x.Name: x for x in SPDEFS}
SPDEFNAMES = [x.Name for x in SPDEFS]
####################################################################################################
# MATERIALSPGROUP = [x for x in SPFILE.Groups if x.Name == "Material"][0]
# PARAMETRICSPGROUP = [x for x in SPFILE.Groups if x.Name == "Parametrics"][0]
# DATAPGROUP = [x for x in SPFILE.Groups if x.Name == "Data"][0]
####################################################################################################
BUILTINPARAMGROUPNAMES = System.Enum.GetNames(BuiltInParameterGroup)
BUILTINPARAMGROUPSOBJECTS = System.Enum.GetValues(BuiltInParameterGroup)
BUILTINPARAMGROUPS = zip(BUILTINPARAMGROUPNAMES,BUILTINPARAMGROUPSOBJECTS)
BUILTINPARAMGROUPSDICT = {x: y for x, y in BUILTINPARAMGROUPS}
####################################################################################################
FAMILYLIST = [RevitFamily(x) for x in INPUTFAMILIES]
####################################################################################################
for RevitFamilyObject in FAMILYLIST:
    parameterSet = RevitFamilyObject.FamilyParameters
    for ParameterObject in parameterSet:
        PARAMETERLIST.append(RevitFamilyParameter(ParameterObject, RevitFamilyObject))
####################################################################################################
for param in PARAMETERLIST:
    param.Report_ParameterNames(PARAMETERNAMES)
for param in PARAMETERLIST:
    param.Report_ParameterCount(PARAMETERNAMES,PARAMETERCOUNT)
####################################################################################################
for param in PARAMETERLIST:
    param.Report_BasicData(BASICDATAEXPORT)
    param.Report_FullData(FULLDATAEXPORT)
####################################################################################################
BASICDATAEXPORT = sorted(BASICDATAEXPORT,key=lambda x: x[1])
BASICDATAEXPORT = sorted(BASICDATAEXPORT,key=lambda x: x[2], reverse=True)
####################################################################################################
FULLDATAEXPORT = set(FULLDATAEXPORT)
FULLDATAEXPORT = sorted(FULLDATAEXPORT,key=lambda x: x[7], reverse=True)
FULLDATAEXPORT = sorted(FULLDATAEXPORT,key=lambda x: x[6])
FULLDATAEXPORT = sorted(FULLDATAEXPORT,key=lambda x: x[1])
FULLDATAEXPORT = sorted(FULLDATAEXPORT,key=lambda x: x[4])
####################################################################################################
EndTimeItTimer('Test1',TIMERLOG)
####################################################################################################
OUT = BASICDATAEXPORT,TIMERLOG,FULLDATAEXPORT,BUILTINPARAMGROUPNAMES,[(x.Name,x.OwnerGroup.Name,x.ParameterType) for x in SPDEFS]
####################################################################################################