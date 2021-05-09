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
import os
import numpy
Mdb()


Lengthx = 4.2
Widthz = 0.7
Heighty = 0.6
yPowder = 0.05
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
mdb.models['Model-1'].setValues(absoluteZero=0, stefanBoltzmann=5.6703e-11)
#Part
mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=200.0)

mdb.models['Model-1'].sketches['__profile__'].rectangle(
    point1=(0.0, 0.0), 
    point2=(Lengthx, Heighty))

mdb.models['Model-1'].Part(
    dimensionality=THREE_D, 
    name='Part-Solid', 
    type=DEFORMABLE_BODY)

mdb.models['Model-1'].parts['Part-Solid'].BaseSolidExtrude(
    depth=Widthz, 
    sketch=mdb.models['Model-1'].sketches['__profile__'])

del mdb.models['Model-1'].sketches['__profile__']

####
mdb.models['Model-1'].ConstrainedSketch(
    gridSpacing=0.18, 
    name='__profile__', 
    sheetSize=8.61, 
    transform=mdb.models['Model-1'].parts['Part-Solid'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt((Lengthx/2, Heighty/2, Widthz), ), 
    sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt((Lengthx, Heighty, Widthz), ), 
    sketchOrientation=RIGHT, 
    origin=(0.0, 0.0, 0.0)))

##################################################################################################################################
#--------------------------------------------------
#transverse line
for i in range(5):
   mdb.models['Model-1'].sketches['__profile__'].Line(
      point1=(0.0, Heighty-i*0.0125), 
      point2=(Lengthx, Heighty-i*0.0125))

for i in range(3):
   mdb.models['Model-1'].sketches['__profile__'].Line(
      point1=(0.0, 0.55-i*0.025), 
      point2=(Lengthx, 0.55-i*0.025))

for i in range(11):
   mdb.models['Model-1'].sketches['__profile__'].Line(
      point1=(0.0, 0.5-i*0.05), 
      point2=(Lengthx, 0.5-i*0.05))

mdb.models['Model-1'].parts['Part-Solid'].PartitionFaceBySketch(
    sketchUpEdge=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt(coordinates=(Lengthx, Heighty/2, Widthz)), 
    faces=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((Lengthx/2, Heighty/2, Widthz), )), 

    sketch=mdb.models['Model-1'].sketches['__profile__'])
#------------------------------------------------------
mdb.models['Model-1'].parts['Part-Solid'].Set(
    cells=mdb.models['Model-1'].parts['Part-Solid'].cells, 
    name='Set-Solid')
mdb.models['Model-1'].parts['Part-Solid'].Set(
    faces=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((Lengthx/2, 0.0, Widthz/2), )), 
    name='Set-SolidBotFace')

face1=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((Lengthx/2, Heighty/2, 0.0), ))
face2=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((Lengthx, Heighty/2, Widthz/2), ))
face3=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((Lengthx/2, Heighty, Widthz/2), ))
face4=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((0.0, Heighty/2, Widthz/2), ))
mdb.models['Model-1'].parts['Part-Solid'].Surface(
    name='Surf-SolidRadFaces', 
    side1Faces=face1+face2+face3+face4)
mdb.models['Model-1'].parts['Part-Solid'].Surface(
    name='Surf-SolidTop', 
    side1Faces=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((Lengthx/2, Heighty, Widthz/2), )))
#Material
mdb.models['Model-1'].Material(name='Material-Solid')
mdb.models['Model-1'].materials['Material-Solid'].Density(table=((1.6904e-08, ), ))
mdb.models['Model-1'].materials['Material-Solid'].Conductivity(table=((97.1, ), ))
mdb.models['Model-1'].materials['Material-Solid'].SpecificHeat(table=((209223821.8, 
    ), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-Solid', 
    material='Material-Solid', thickness=None)


mdb.models['Model-1'].parts['Part-Solid'].SectionAssignment(region=mdb.models['Model-1'].parts['Part-Solid'].Set(
    cells=mdb.models['Model-1'].parts['Part-Solid'].cells.findAt(((Lengthx/2, Heighty/2, Widthz/2), )), name='Set-Solid'), 
    sectionName='Section-Solid', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

###################################################################################
mdb.models['Model-1'].ConstrainedSketch(name='__profile__',  sheetSize=200.0)

mdb.models['Model-1'].sketches['__profile__'].rectangle(
    point1=(0.0, 0.0), 
    point2=(Lengthx, yPowder))

mdb.models['Model-1'].Part(
    dimensionality=THREE_D, 
    name='Part-Powder', 
    type=DEFORMABLE_BODY)

mdb.models['Model-1'].parts['Part-Powder'].BaseSolidExtrude(
    depth=Widthz, 
    sketch=mdb.models['Model-1'].sketches['__profile__'])

del mdb.models['Model-1'].sketches['__profile__']
#-----------------------------------------------------
mdb.models['Model-1'].parts['Part-Powder'].Set(
    cells=mdb.models['Model-1'].parts['Part-Powder'].cells, 
    name='Set-Powder')


facep1=mdb.models['Model-1'].parts['Part-Powder'].faces.findAt(((Lengthx/2, yPowder/2, 0.0), ))
facep2=mdb.models['Model-1'].parts['Part-Powder'].faces.findAt(((Lengthx, yPowder/2, Widthz/2), ))
facep3=mdb.models['Model-1'].parts['Part-Powder'].faces.findAt(((Lengthx/2, yPowder, Widthz/2), ))
facep4=mdb.models['Model-1'].parts['Part-Powder'].faces.findAt(((0.0,  yPowder/2, Widthz/2), ))
mdb.models['Model-1'].parts['Part-Powder'].Surface(
    name='Surf-RadPowderFaces', 
    side1Faces=facep1+facep2+facep3+facep4)

mdb.models['Model-1'].parts['Part-Powder'].Surface(
    name='Surf-PowderBottom', 
    side1Faces=mdb.models['Model-1'].parts['Part-Powder'].faces.findAt(((Lengthx/2, 0.0, Widthz/2), )))
#-----------------------------------------------------
#Material
mdb.models['Model-1'].Material(name='Material-Powder')
mdb.models['Model-1'].materials['Material-Powder'].Density(table=((1.36024e-08, ), ))
mdb.models['Model-1'].materials['Material-Powder'].Conductivity(table=((38.636, ), ))
mdb.models['Model-1'].materials['Material-Powder'].SpecificHeat(table=((209223821.8,  
    ), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-Powder', 
    material='Material-Powder', thickness=None)


mdb.models['Model-1'].parts['Part-Powder'].SectionAssignment(region=mdb.models['Model-1'].parts['Part-Powder'].Set(
    cells=mdb.models['Model-1'].parts['Part-Powder'].cells.findAt(((Lengthx/2, yPowder/2, Widthz), )), name='Set-Powder'), 
    sectionName='Section-Powder', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
#======================================================

mdb.models['Model-1'].parts['Part-Powder'].setElementType(
    elemTypes=(ElemType(elemCode=DC3D8, elemLibrary=STANDARD), ElemType(elemCode=DC3D6, 
      elemLibrary=STANDARD), ElemType(elemCode=DC3D4, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['Part-Powder'].cells, ))
mdb.models['Model-1'].parts['Part-Powder'].setMeshControls(
    regions=mdb.models['Model-1'].parts['Part-Powder'].cells, 
    technique=SWEEP)

mdb.models['Model-1'].parts['Part-Powder'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Powder'].edges.findAt(((Lengthx/2, yPowder, Widthz), )), 
    size=0.07)

mdb.models['Model-1'].parts['Part-Powder'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Powder'].edges.findAt(((Lengthx/2, yPowder, 0.0), )), 
    size=0.07)


mdb.models['Model-1'].parts['Part-Powder'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Powder'].edges.findAt(((Lengthx/2, 0.0, 0.0), )), 
    size=0.07)

mdb.models['Model-1'].parts['Part-Powder'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Powder'].edges.findAt(((Lengthx/2, 0.0, Widthz), )), 
    size=0.07)


mdb.models['Model-1'].parts['Part-Powder'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Powder'].edges.findAt(((Lengthx, yPowder, Widthz/2), )), 
    size=0.035)

mdb.models['Model-1'].parts['Part-Powder'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Powder'].edges.findAt(((Lengthx, yPowder/2, 0.0), )), 
    size=0.0125)

mdb.models['Model-1'].parts['Part-Powder'].generateMesh(
    regions=mdb.models['Model-1'].parts['Part-Powder'].cells)


#mdb.models['Model-1'].parts['Part-Solid'].PartitionFaceBySketch(
#    faces=mdb.models['Model-1'].parts['Part-Solid'].faces.findAt(((Lengthx/2, Heighty/2, 0.0), ), ((Lengthx/2, Heighty/4, 0.0), ), ), 
#    sketch=mdb.models['Model-1'].sketches['__profile__'],
#    sketchUpEdge=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt((Lengthx/2, Heighty/2, 0.0), )) 

#Assembly
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-Solid-1', 
    part=mdb.models['Model-1'].parts['Part-Solid'])

mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-Powder-1', 
    part=mdb.models['Model-1'].parts['Part-Powder'])

mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-Powder-1', ), 
	vector=(0.0, Heighty, 0.0))
sum_cells = mdb.models['Model-1'].rootAssembly.instances['Part-Solid-1'].cells + mdb.models['Model-1'].rootAssembly.instances['Part-Powder-1'].cells
mdb.models['Model-1'].rootAssembly.Set(cells=sum_cells, name='Set-All')


mdb.models['Model-1'].Tie(
    adjust=ON, 
    master=mdb.models['Model-1'].rootAssembly.instances['Part-Solid-1'].surfaces['Surf-SolidTop'], 
    name='Constraint-1', 
    positionToleranceMethod=COMPUTED, 
    slave=mdb.models['Model-1'].rootAssembly.instances['Part-Powder-1'].surfaces['Surf-PowderBottom'], 
    thickness=ON, 
    tieRotations=ON)

#Step
mdb.models['Model-1'].HeatTransferStep(
    name='Step-1', 
    previous='Initial', 
    timeIncrementationMethod=FIXED, 
    initialInc=0.000042,
    timePeriod=0.0084,
    maxNumInc=300)


mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'NT', ))
mdb.models['Model-1'].RadiationToAmbient(
      ambientTemperature=1123.15, 
        ambientTemperatureAmp='', 
        createStepName='Step-1', 
        distributionType=UNIFORM, 
        emissivity=0.3, 
        field='', 
        name='Int-SolidRadiation', 
        radiationType=AMBIENT, 
        surface=mdb.models['Model-1'].rootAssembly.instances['Part-Solid-1'].surfaces['Surf-SolidRadFaces'])

mdb.models['Model-1'].RadiationToAmbient(
      ambientTemperature=1123.15, 
        ambientTemperatureAmp='', 
        createStepName='Step-1', 
        distributionType=UNIFORM, 
        emissivity=0.3, 
        field='', 
        name='Int-PowderRadiation', 
        radiationType=AMBIENT, 
        surface=mdb.models['Model-1'].rootAssembly.instances['Part-Powder-1'].surfaces['Surf-RadPowderFaces'])
#Load
mdb.models['Model-1'].BodyHeatFlux(
    createStepName='Step-1', 
    distributionType=USER_DEFINED, 
    magnitude=1.0, 
    name='Load-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-All'])
mdb.models['Model-1'].TemperatureBC(
    amplitude=UNSET, 
    createStepName='Step-1', 
    distributionType=UNIFORM, 
    fieldName='', 
    fixed=OFF, 
    magnitude=1123.15, 
    name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.instances['Part-Solid-1'].sets['Set-SolidBotFace'])
mdb.models['Model-1'].Temperature(
    createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, 
    distributionType=UNIFORM, 
    magnitudes=(1123.15, ), 
    name='Predefined Field-1', 
    region=mdb.models['Model-1'].rootAssembly.instances['Part-Solid-1'].sets['Set-Solid'])

mdb.models['Model-1'].Temperature(
    createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, 
    distributionType=UNIFORM, 
    magnitudes=(1123.15, ), 
    name='Predefined Field-2', 
    region=mdb.models['Model-1'].rootAssembly.instances['Part-Powder-1'].sets['Set-Powder'])
#==============================================================================
#Mesh
mdb.models['Model-1'].parts['Part-Solid'].setElementType(
    elemTypes=(ElemType(elemCode=DC3D8, elemLibrary=STANDARD), ElemType(elemCode=DC3D6, 
      elemLibrary=STANDARD), ElemType(elemCode=DC3D4, elemLibrary=STANDARD)), 
    regions=(mdb.models['Model-1'].parts['Part-Solid'].cells, ))
mdb.models['Model-1'].parts['Part-Solid'].setMeshControls(
    regions=mdb.models['Model-1'].parts['Part-Solid'].cells, 
    technique=SWEEP)

mdb.models['Model-1'].parts['Part-Solid'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Solid'].edges, 
    size=1)

mdb.models['Model-1'].parts['Part-Solid'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt(((Lengthx/2, Heighty, Widthz), )), 
    size=0.07)

mdb.models['Model-1'].parts['Part-Solid'].seedEdgeBySize(
    constraint=FINER, 
    edges=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt(((0.0, 0.0, Widthz/2), )), 
    size=0.035)

mdb.models['Model-1'].parts['Part-Solid'].PartitionCellByPlanePointNormal(
	point=mdb.models['Model-1'].parts['Part-Solid'].vertices.findAt(coordinates=(Lengthx, 0.55, Widthz)), 
	normal=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt(coordinates=(Lengthx, Heighty/2, Widthz)), 
	cells=mdb.models['Model-1'].parts['Part-Solid'].cells.findAt(((Lengthx/2, Heighty/2, Widthz/2), )))

mdb.models['Model-1'].parts['Part-Solid'].PartitionCellByPlanePointNormal(
	point=mdb.models['Model-1'].parts['Part-Solid'].vertices.findAt(coordinates=(4.2, 0.5, 0.7)), 
    normal=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt(coordinates=(4.2, 0.51875, 0.7)), 
    cells=mdb.models['Model-1'].parts['Part-Solid'].cells.findAt(((0.0, 0.541667, 0.466667), )))

#mdb.models['Model-1'].parts['Part-Solid'].PartitionCellByPlanePointNormal(
#	point=mdb.models['Model-1'].parts['Part-Solid'].vertices.findAt(coordinates=(Lengthx, 0.5, Widthz)), 
#    normal=mdb.models['Model-1'].parts['Part-Solid'].edges.findAt(coordinates=(Lengthx, Heighty/2, Widthz)), 
#    cells=mdb.models['Model-1'].parts['Part-Solid'].cells.findAt(((Lengthx/2, Heighty/3, Widthz/2), )))


mdb.models['Model-1'].parts['Part-Solid'].generateMesh(
    regions=mdb.models['Model-1'].parts['Part-Solid'].cells)


jobName = 'Powder_WithRadiation'
mdb.Job(model='Model-1', name=jobName, numCpus=8, numDomains=8, userSubroutine=os.path.realpath("Goldak_dflux_Tungsten.for") )
mdb.saveAs(pathName=jobName)
