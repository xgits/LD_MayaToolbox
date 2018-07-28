__author__ = "James.N"
__version__ = "v1.8.1"

import sys
import math

import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as om

kPluginNodename = 'curveSpiral'
kPluginNodeId = om.MTypeId(0xBE8AC)


# helper function to query param range of nurbs curve
def getCurveRange(curveFn, curveObj=None):
    if not(isinstance(curveFn, om.MFnNurbsCurve)):
        raise TypeError("curveFn must be MFnNurbsCurve type!")

    if (curveObj is not None) and (not curveObj.isNull()):
        curveFn.setObject(curveObj)

    start = 0.0; end = 0.0

    # create wrappers for start and end param
    startHandle = om.MScriptUtil(); endHandle = om.MScriptUtil()
    startPtr = startHandle.asDoublePtr(); endPtr = endHandle.asDoublePtr()
    # query curve parameter range
    curveFn.getKnotDomain(startPtr, endPtr)
    # extract range values
    start = startHandle.getDouble(startPtr);
    end = endHandle.getDouble(endPtr);

    return (start, end)

# get point/normal/tangent at specify length of curve
def getPointAtLength(curveFn, length, space=om.MSpace.kObject):
    # get param first
    param = curveFn.findParamFromLength(length)
    # get point at param
    point = om.MPoint()
    curveFn.getPointAtParam(param, point, space)

    return point

def getNormalAtLength(curveFn, length, space=om.MSpace.kObject):
    # get param first
    param = curveFn.findParamFromLength(length)
    # get normal at param
    return curveFn.normal(param, space)

def getTangentAtLength(curveFn, length, space=om.MSpace.kObject):
    # get param first
    param = curveFn.findParamFromLength(length)
    # get normal at param
    return curveFn.tangent(param, space)

def getFloatRampVal(ramp, pos):
    if not isinstance(ramp, om.MRampAttribute):
        raise ValueError("Invalid ramp attribute object!")

    handle = om.MScriptUtil()
    handle.createFromDouble(1.0)
    valAtPtr = handle.asFloatPtr()
    ramp.getValueAtPosition(pos, valAtPtr)
    return handle.getFloat(valAtPtr)


# drawing methods
def drawByParameter(pointArr, curveFn, iterCount, parmRange, drawRange, step, sweep, radius, rot, radiusMap=None, worldSpace=False):
# determine param range
    paramLength = parmRange[1] - parmRange[0]
    currentParam = parmRange[0] + paramLength * drawRange[0]
    # determine space
    space = om.MSpace.kWorld if worldSpace else om.MSpace.kObject

    if iterCount > 0:
        step = paramLength * (drawRange[1] - drawRange[0]) / (iterCount - 1);

    angle = 0.0
    upAxis = om.MVector(0.0, -1.0, 0.0)
    xAxis = om.MVector(1.0, 0.0, 0.0)
    while currentParam <= (parmRange[0] + paramLength * drawRange[1]):
        # compute radius multiply
        r_mult = 1.0
        if radiusMap is not None:
            r_mult = getFloatRampVal(radiusMap, (currentParam - parmRange[0]) / paramLength)

        # get point
        pos = om.MPoint()
        curveFn.getPointAtParam(currentParam, pos, space)
        # get direction
        tangent = curveFn.tangent(currentParam, space).normal()
        sideVec = (tangent ^ upAxis).normal()
        normal = sideVec ^ tangent.normal()
        # compute rotation by tangent as axis and angle
        rotation = om.MQuaternion(math.radians(angle + rot), tangent)
        direction = normal.rotateBy(rotation) * radius * r_mult

        pos += direction
        pointArr.append(pos)

        currentParam += step
        angle += sweep

def drawByLength(pointArr, curveFn, iterCount, drawRange, step, sweep, radius, rot, radiusMap=None, worldSpace=False):
    # determine length range
    length = curveFn.length()
    currentLen = length * drawRange[0]
    # determine space
    space = om.MSpace.kWorld if worldSpace else om.MSpace.kObject

    # override length step if explicit iteration count is used
    if iterCount > 0:
        step = length * (drawRange[1] - drawRange[0]) / (iterCount - 1)

    angle = 0.0
    upAxis = om.MVector(0.0, -1.0, 0.0)
    xAxis = om.MVector(1.0, 0.0, 0.0)
    while currentLen <= (length * drawRange[1]):
        # compute radius multiply
        r_mult = 1.0
        if radiusMap is not None:
            r_mult = getFloatRampVal(radiusMap, currentLen / length)

        # get point
        pos = getPointAtLength(curveFn, currentLen, space = space)
        # get direction
        tangent = getTangentAtLength(curveFn, currentLen, space = space).normal()
        sideVec = (tangent ^ upAxis).normal()
        normal = sideVec ^ tangent.normal()
        # compute rotation by tangent as axis and angle
        rotation = om.MQuaternion(math.radians(angle + rot), tangent)
        direction = normal.rotateBy(rotation) * radius * r_mult

        pos += direction
        pointArr.append(pos)
        
        currentLen += step
        angle += sweep


class CurveSpiralNode(OpenMayaMPx.MPxNode):
    # input curve
    inputCurveAttribute = om.MObject()
    # spiral radius
    spiralRadiusAttribute = om.MObject()
    # use radius map
    useRadiusMapAttribute = om.MObject()
    # radius ramp
    radiusRampAttribute = om.MRampAttribute()
    # sweep increment
    sweepAmountAttribute = om.MObject()
    # use point count
    usePtCountAttribute = om.MObject()
    # point count
    ptCountAttribute = om.MObject()
    # sample by length
    sampleByLengthAttribute = om.MObject()
    # param increment
    paramStepAttribute = om.MObject()
    # length increment
    lengthStepAttribute = om.MObject()
    # drawing range
    drawingRangeAttribute = om.MObject()
    # rotation
    rotationAttribute = om.MObject()
    # use world space
    useWorldSpaceAttribute = om.MObject()

    # output
    outputCurveAttribute = om.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def postConstructor(self):
        # set default state of radius ramp
        thisFn = om.MFnDependencyNode(self.thisMObject())
        rampPlug = thisFn.findPlug("radiusMap")

        stHandle = rampPlug.elementByLogicalIndex(0)
        valueSlot = stHandle.child(1)   #child 0: positon, child 1: value, child 2: iterpolation method
        valueSlot.setDouble(1.0)

    def compute(self, pPlug, pDataBlock):
        if pPlug == CurveSpiralNode.outputCurveAttribute:
            # return if input curve is not given
            #if not CurveSpiralNode.inputCurveAttribute.isConnected():
            #  return

            # get input curve
            inputCurveHandle = pDataBlock.inputValue(CurveSpiralNode.inputCurveAttribute)
            inputCurve = inputCurveHandle.asNurbsCurve()

            # get use radius map
            useRadiusMap = pDataBlock.inputValue(CurveSpiralNode.useRadiusMapAttribute).asBool()
            radiusMap = None
            if useRadiusMap:
                # get radius ramp attr
                thisNode = self.thisMObject()
                radiusMapPlug = om.MPlug(thisNode, CurveSpiralNode.radiusRampAttribute)
                radiusMapPlug.setAttribute(CurveSpiralNode.radiusRampAttribute)
                #Get the atrributes as MRampAttribute
                radiusMap = om.MRampAttribute(radiusMapPlug.node(), radiusMapPlug.attribute())

            # get radius
            radius = pDataBlock.inputValue(CurveSpiralNode.spiralRadiusAttribute).asFloat()
            # get sweep
            sweep = pDataBlock.inputValue(CurveSpiralNode.sweepAmountAttribute).asDouble()
            # get use point count
            usePtCount = pDataBlock.inputValue(CurveSpiralNode.usePtCountAttribute).asBool()
            # get point count
            ptCount = pDataBlock.inputValue(CurveSpiralNode.ptCountAttribute).asLong() if usePtCount else -1
            # get sample mode
            sampleByLength = pDataBlock.inputValue(CurveSpiralNode.sampleByLengthAttribute).asBool()
            # get param step
            paramStep = pDataBlock.inputValue(CurveSpiralNode.paramStepAttribute).asDouble()
            # get length step
            lengthStep = pDataBlock.inputValue(CurveSpiralNode.lengthStepAttribute).asDouble()
            # get drawing range
            drawRange = pDataBlock.inputValue(CurveSpiralNode.drawingRangeAttribute).asFloat2()
            if not(0.0 <= drawRange[0] < drawRange[1] <= 1.0):
                raise ValueError("Invalid drawing parameter range!")
            # get rotation
            baseRot = pDataBlock.inputValue(CurveSpiralNode.rotationAttribute).asDouble()
            # get use world space
            useWorldSpace = pDataBlock.inputValue(CurveSpiralNode.useWorldSpaceAttribute).asBool()

            curveFn = om.MFnNurbsCurve(inputCurve)
            edArr = om.MPointArray()

            if not sampleByLength:
                # determine param range
                curveParamRange = getCurveRange(curveFn)
                drawByParameter(edArr, curveFn, ptCount, curveParamRange, drawRange, paramStep, sweep, radius, baseRot, radiusMap = radiusMap, worldSpace = useWorldSpace)
            else:
                drawByLength(edArr, curveFn, ptCount, drawRange, lengthStep, sweep, radius, baseRot, radiusMap = radiusMap, worldSpace = useWorldSpace)

            # output curve data
            outCurveFn = om.MFnNurbsCurve()
            outputCurveData = om.MFnNurbsCurveData().create()

            outCurveFn.createWithEditPoints(edArr, 3, om.MFnNurbsCurve.kOpen, False, False, True, outputCurveData)

            # set output attribute
            outputCurveHandle = pDataBlock.outputValue(CurveSpiralNode.outputCurveAttribute)
            outputCurveHandle.setMObject(outputCurveData)
            pDataBlock.setClean(CurveSpiralNode.outputCurveAttribute)


# node initialization
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(CurveSpiralNode())

def nodeInitializer():
    numericAttributeFn = om.MFnNumericAttribute()
    typedAttributeFn = om.MFnTypedAttribute()

    # input curve attribute
    CurveSpiralNode.inputCurveAttribute = typedAttributeFn.create('inputCurve', 'ic', om.MFnData.kNurbsCurve)
    typedAttributeFn.setStorable(False)
    typedAttributeFn.setWritable(True)
    typedAttributeFn.setReadable(False)
    typedAttributeFn.setHidden(False)
    CurveSpiralNode.addAttribute(CurveSpiralNode.inputCurveAttribute)

    # add radius attribute
    CurveSpiralNode.spiralRadiusAttribute = numericAttributeFn.create('radius', 'radius', om.MFnNumericData.kFloat, 1.0)
    numericAttributeFn.setSoftMin(0)
    numericAttributeFn.setSoftMax(10.0)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(True)
    CurveSpiralNode.addAttribute(CurveSpiralNode.spiralRadiusAttribute)

    # add use radius map attribute
    CurveSpiralNode.useRadiusMapAttribute = numericAttributeFn.create('useRadiusMap', 'useRM', om.MFnNumericData.kBoolean, False)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(False)
    CurveSpiralNode.addAttribute(CurveSpiralNode.useRadiusMapAttribute)

    # add radius ramp attribute
    CurveSpiralNode.radiusRampAttribute = om.MRampAttribute.createCurveRamp("radiusMap", "rm")
    CurveSpiralNode.addAttribute(CurveSpiralNode.radiusRampAttribute)

    # add sweep attribute
    CurveSpiralNode.sweepAmountAttribute = numericAttributeFn.create('sweep', 'sweep', om.MFnNumericData.kDouble, 10)
    numericAttributeFn.setSoftMin(0.01)
    numericAttributeFn.setSoftMax(90.0)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(True)
    CurveSpiralNode.addAttribute(CurveSpiralNode.sweepAmountAttribute)

    # add use point count attribute
    CurveSpiralNode.usePtCountAttribute = numericAttributeFn.create('usePointCount', 'usePtCnt', om.MFnNumericData.kBoolean, False)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(False)
    CurveSpiralNode.addAttribute(CurveSpiralNode.usePtCountAttribute)

    # add point count attribute
    CurveSpiralNode.ptCountAttribute = numericAttributeFn.create('pointCount', 'ptCount', om.MFnNumericData.kLong, 20)
    numericAttributeFn.setMin(3)
    numericAttributeFn.setSoftMax(200)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(True)
    CurveSpiralNode.addAttribute(CurveSpiralNode.ptCountAttribute)

    # add sample by length attribute
    CurveSpiralNode.sampleByLengthAttribute = numericAttributeFn.create('byLength', 'byLength', om.MFnNumericData.kBoolean, False)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(False)
    CurveSpiralNode.addAttribute(CurveSpiralNode.sampleByLengthAttribute)

    # add param step attribute
    CurveSpiralNode.paramStepAttribute = numericAttributeFn.create('paramStep', 'pms', om.MFnNumericData.kDouble, 0.2)
    numericAttributeFn.setMin(0.001)
    numericAttributeFn.setSoftMax(1.0)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(True)
    CurveSpiralNode.addAttribute(CurveSpiralNode.paramStepAttribute)

    # add length step attribute
    CurveSpiralNode.lengthStepAttribute = numericAttributeFn.create('lengthStep', 'lens', om.MFnNumericData.kDouble, 1.0)
    numericAttributeFn.setMin(0.01)
    numericAttributeFn.setSoftMax(5.0)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(True)
    CurveSpiralNode.addAttribute(CurveSpiralNode.lengthStepAttribute)

    # add drawing range attribute
    CurveSpiralNode.drawingRangeAttribute = numericAttributeFn.create('range', 'range', om.MFnNumericData.k2Float)
    numericAttributeFn.setDefault(0.0, 1.0)
    numericAttributeFn.setMin(0.0, 0.0)
    numericAttributeFn.setMax(1.0, 1.0)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(True)
    CurveSpiralNode.addAttribute(CurveSpiralNode.drawingRangeAttribute)

    # add base rotation attribute
    CurveSpiralNode.rotationAttribute = numericAttributeFn.create('rotation', 'rot', om.MFnNumericData.kDouble, 0.0)
    numericAttributeFn.setSoftMin(-180.0)
    numericAttributeFn.setSoftMax(180.0)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(True)
    CurveSpiralNode.addAttribute(CurveSpiralNode.rotationAttribute)

    # output curve attribute
    CurveSpiralNode.outputCurveAttribute = typedAttributeFn.create('outputCurve', 'oc', om.MFnData.kNurbsCurve)
    typedAttributeFn.setStorable(False)
    typedAttributeFn.setWritable(False)
    typedAttributeFn.setReadable(True)
    typedAttributeFn.setHidden(False)
    CurveSpiralNode.addAttribute(CurveSpiralNode.outputCurveAttribute)

    # add use world space attribute
    CurveSpiralNode.useWorldSpaceAttribute = numericAttributeFn.create('useWorldSpace', 'uws', om.MFnNumericData.kBoolean, False)
    numericAttributeFn.setStorable(True)
    numericAttributeFn.setWritable(True)
    numericAttributeFn.setReadable(False)
    numericAttributeFn.setKeyable(False)
    CurveSpiralNode.addAttribute(CurveSpiralNode.useWorldSpaceAttribute)

    # define affecting matrix
    CurveSpiralNode.attributeAffects(CurveSpiralNode.inputCurveAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.spiralRadiusAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.useRadiusMapAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.radiusRampAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.sweepAmountAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.usePtCountAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.ptCountAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.sampleByLengthAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.paramStepAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.lengthStepAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.drawingRangeAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.rotationAttribute, CurveSpiralNode.outputCurveAttribute)
    CurveSpiralNode.attributeAffects(CurveSpiralNode.useWorldSpaceAttribute, CurveSpiralNode.outputCurveAttribute)


# plugin initialization
def initializePlugin(mObject):
    mplugin = OpenMayaMPx.MFnPlugin(mObject, "James.N")
    try:
        mplugin.registerNode(kPluginNodename, kPluginNodeId, nodeCreator, nodeInitializer)
        mplugin.setVersion("1.4.2")
    except:
        sys.stderr.write("Failed to register node: %s" %kPluginNodename)
        raise

def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write("Failed to deregister node: %s" %kPluginNodename)
        raise