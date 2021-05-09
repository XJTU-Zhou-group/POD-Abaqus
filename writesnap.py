jobName = 'mesh'
stepName = 'Step-1'
outputSetName = ' ALL NODES'

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

odb = openOdb(path = jobName+'.odb')

os.makedirs('ResultFiles')
os.chdir('ResultFiles')

NodeTemperature = np.zeros((26901,201))
for fm in range(0, len(odb.steps[stepName].frames)):
    timeFrame = odb.steps[stepName].frames[fm]
    readNode = odb.rootAssembly.nodeSets[outputSetName]
    Temperature = timeFrame.fieldOutputs['NT11']  # Remember to set field outputs manually
    readNodeTemperature = Temperature.getSubset(region=readNode)
    readNodeTemperatureValues = readNodeTemperature.values
    count=len(readNodeTemperatureValues)
    for i in range(0, count):
        NodeTemperature[i][fm]=readNodeTemperatureValues[i].data
    
np.savetxt("NodeTemperature.csv", NodeTemperature, delimiter=",")

odb.close()
