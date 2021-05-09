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
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=8.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(
    point1=(0.0, 0.0), 
    point2=(3.1415926, 3.1415926))
mdb.models['Model-1'].Part(
    dimensionality=TWO_D_PLANAR, 
    name='Part-1', 
    type=DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Conductivity(table=((1.0, ), ))
mdb.models['Model-1'].materials['Material-1'].SpecificHeat(table=((1.0, ), ))
mdb.models['Model-1'].materials['Material-1'].Density(table=((1.0, ), ))

mdb.models['Model-1'].HomogeneousSolidSection(
    material='Material-1', 
    name='Section-1', 
    thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(
    faces=mdb.models['Model-1'].parts['Part-1'].faces, 
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
    initialInc=0.02, 
    maxNumInc=1000, 
    name='Step-1', 
    previous='Initial', 
    timeIncrementationMethod=FIXED, 
    timePeriod=3.0)

mdb.models['Model-1'].rootAssembly.Set(
    edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges, 
    name='Set-1')
mdb.models['Model-1'].TemperatureBC(
    createStepName='Initial', 
    distributionType=UNIFORM, 
    fieldName='', 
    magnitude=0.0, 
    name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-1'])

mdb.models['Model-1'].ExpressionField(
    description='', 
    expression='10*sin (  X  )*sin (  Y  )', 
    localCsys=None, 
    name='AnalyticalField-1')
mdb.models['Model-1'].Temperature(
    createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, 
    distributionType=FIELD, 
    field='AnalyticalField-1', 
    magnitudes=(1.0, ), 
    name='Predefined Field-1', 
    region=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-1'])

mdb.models['Model-1'].parts['Part-1'].seedPart(
    deviationFactor=0.1, 
    minSizeFactor=0.1, 
    size=0.157)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(
    elemTypes=(ElemType(
        elemCode=DC2D4, elemLibrary=STANDARD), ), 
    regions=(mdb.models['Model-1'].parts['Part-1'].faces, ))

jobName = 'SquareDomain2D'
mdb.Job(model='Model-1', name=jobName, numCpus=8, numDomains=8 )
