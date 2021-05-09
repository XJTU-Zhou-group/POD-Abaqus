# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

Mdb()

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.2)
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(
    center=(0.0, 0.0), 
    direction=CLOCKWISE, 
    point1=(0.0, 0.05), 
    point2=(0.05, 0.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, 0.05), 
    point2=(0.0, 0.1))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.0, 0.1), 
    point2=(0.1, 0.1))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.1, 0.1), 
    point2=(0.1, 0.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(0.1, 0.0), 
    point2=(0.05, 0.0))
mdb.models['Model-1'].Part(
    dimensionality=THREE_D, 
    name='Part-1', 
    type=DEFORMABLE_BODY)

mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(
    depth=0.02, 
    sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Conductivity(table=((15.0, ), ))
mdb.models['Model-1'].materials['Material-1'].SpecificHeat(table=((125.0, ), ))
mdb.models['Model-1'].materials['Material-1'].Density(table=((7800.0, ), ))

mdb.models['Model-1'].HomogeneousSolidSection(
    material='Material-1', 
    name='Section-1', 
    thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(
    cells=mdb.models['Model-1'].parts['Part-1'].cells, 
    name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(
    offset=0.0, 
    offsetField='', 
    offsetType=MIDDLE_SURFACE, 
    region=mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], 
    sectionName='Section-1', 
    thicknessAssignment=FROM_SECTION)

mdb.models['Model-1'].rootAssembly.Instance(
    dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])

mdb.models['Model-1'].HeatTransferStep(
    initialInc=1.0, 
    maxNumInc=1000, 
    name='Step-1', 
    previous='Initial', 
    timeIncrementationMethod=FIXED, 
    timePeriod=750.0)

mdb.models['Model-1'].rootAssembly.Surface(
    name='Surf-1', 
    side1Faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.00963, 0.065078, 0.02), )))
mdb.models['Model-1'].FilmCondition(
    createStepName='Step-1', 
    definition=EMBEDDED_COEFF, 
    filmCoeff=200.0, 
    filmCoeffAmplitude='', 
    name='Int-1', 
    sinkAmplitude='', 
    sinkDistributionType=UNIFORM, 
    sinkFieldName='', 
    sinkTemperature=100.0, 
    surface=mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'])
mdb.models['Model-1'].setValues(absoluteZero=-273.15, stefanBoltzmann=5.669e-08)

mdb.models['Model-1'].Temperature(
    createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, 
    distributionType=UNIFORM, 
    magnitudes=(50.0, ), 
    name='Predefined Field-1', 
    region=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-1'])

mdb.models['Model-1'].rootAssembly.Set(
    faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.049893, 0.003265, 0.013333), )), 
    name='Set-1')
mdb.models['Model-1'].TemperatureBC(
    amplitude=UNSET, 
    createStepName='Step-1', 
    distributionType=UNIFORM, 
    fieldName='', 
    fixed=OFF, 
    magnitude=200.0, 
    name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-1'])

mdb.models['Model-1'].parts['Part-1'].seedPart(
    deviationFactor=0.1, 
    minSizeFactor=0.1, 
    size=0.005)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=DC3D8, elemLibrary=STANDARD), ), 
    regions=(mdb.models['Model-1'].parts['Part-1'].cells, ))

jobName = 'SquarePlateWithHole3D'
mdb.Job(model='Model-1', name=jobName, numCpus=8, numDomains=8 )
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()


##############################################################
## Report Nodal Heat Flux from Heat Transfer Analysis
## http://www.anning003.com/extract-reaction-force/
##############################################################

jobName = 'SquarePlateWithHole3D'
stepName = 'Step-1'
outputSetName = ' ALL NODES'

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os

odb = openOdb(path = jobName+'.odb')

os.makedirs('ResultFiles')
os.chdir('ResultFiles')

NodeTemperature = np.zeros((1685,751))

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
