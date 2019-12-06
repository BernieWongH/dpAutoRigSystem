# importing libraries:
import maya.cmds as cmds
import dpUtils as utils

dic_colors = {
    "yellow": 17,
    "red": 13,
    "blue": 6,
    "cyan": 18,
    "green": 7,
    "darkRed": 4,
    "darkBlue": 15,
    "white": 16,
    "black": 1,
    "gray": 3,
    "none": 0,
}

class ControlClass:

    def __init__(self, dpUIinst, presetDic, presetName, *args):
        """ Initialize the module class defining variables to use creating preset controls.
        """
        # defining variables:
        self.dpUIinst = dpUIinst
        self.presetDic = presetDic
        self.presetName = presetName


    # CONTROLS functions:
    def colorShape(self, objList, color, rgb=False, *args):
        """ Create a color override for all shapes from the objList.
        """
        if rgb:
            pass
        elif (dic_colors.has_key(color)):
            iColorIdx = dic_colors[color]
        else:
            iColorIdx = color

        # find shapes and apply the color override:
        shapeTypeList = ['nurbsCurve', 'nurbsSurface', 'mesh', 'subdiv']
        if objList:
            for objName in objList:
                objType = cmds.objectType(objName)
                # verify if the object is the shape type:
                if objType in shapeTypeList:
                    # set override as enable:
                    cmds.setAttr(objName+".overrideEnabled", 1)
                    # set color override:
                    if rgb:
                        cmds.setAttr(objName+".overrideRGBColors", 1)
                        cmds.setAttr(objName+".overrideColorR", color[0])
                        cmds.setAttr(objName+".overrideColorG", color[1])
                        cmds.setAttr(objName+".overrideColorB", color[2])
                    else:
                        cmds.setAttr(objName+".overrideRGBColors", 0)
                        cmds.setAttr(objName+".overrideColor", iColorIdx)
                # verify if the object is a transform type:
                elif objType == "transform":
                    # find all shapes children of the transform object:
                    shapeList = cmds.listRelatives(objName, shapes=True, children=True, fullPath=True)
                    if shapeList:
                        for shape in shapeList:
                            # set override as enable:
                            cmds.setAttr(shape+".overrideEnabled", 1)
                            # set color override:
                            if rgb:
                                cmds.setAttr(shape+".overrideRGBColors", 1)
                                cmds.setAttr(shape+".overrideColorR", color[0])
                                cmds.setAttr(shape+".overrideColorG", color[1])
                                cmds.setAttr(shape+".overrideColorB", color[2])
                            else:
                                cmds.setAttr(shape+".overrideRGBColors", 0)
                                cmds.setAttr(shape+".overrideColor", iColorIdx)


    def renameShape(self, transformList, *args):
        """Find shapes, rename them to Shapes and return the results.
        """
        resultList = []
        for transform in transformList:
            # list all children shapes:
            childShapeList = cmds.listRelatives(transform, shapes=True, children=True, fullPath=True)
            if childShapeList:
                # verify if there is only one shape and return it renamed:
                if len(childShapeList) == 1:
                    shape = cmds.rename(childShapeList[0], transform+"Shape")
                    cmds.select(clear=True)
                    resultList.append(shape)
                # else rename and return one list of renamed shapes:
                elif len(childShapeList) > 1:
                    for i, child in enumerate(childShapeList):
                        shape = cmds.rename(child, transform+str(i)+"Shape")
                        resultList.append(shape)
                    cmds.select(clear=True)
            else:
                print "There are not children shape to rename inside of:", transform
        return resultList


    def directConnect(self, fromObj, toObj, attrList=['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'], f=True, *args):
        """Connect attributes from list directely between two objects given.
        """
        if cmds.objExists(fromObj) and cmds.objExists(toObj):
            for attr in attrList:
                try:
                    # connect attributes:
                    cmds.connectAttr(fromObj+"."+attr, toObj+"."+attr, force=f)
                except:
                    print "Error: Cannot connect", toObj, ".", attr, "directely."
        
        
    def setLockHide(self, objList, attrList, l=True, k=False, *args):
        """Set lock or hide to attributes for object in lists.
        """
        if objList and attrList:
            for obj in objList:
                for attr in attrList:
                    try:
                        # set lock and hide of given attributes:
                        cmds.setAttr(obj+"."+attr, lock=l, keyable=k)
                    except:
                        print "Error: Cannot set", obj, ".", attr, "as lock=", l, "and keyable=", k
                        
                        
    def setNonKeyable(self, objList, attrList, *args):
        """Set nonKeyable to attributes for objects in lists.
        """
        if objList and attrList:
            for obj in objList:
                for attr in attrList:
                    if cmds.objExists(obj+"."+attr):
                        try:
                            # set lock and hide of given attributes:
                            cmds.setAttr(obj+"."+attr, keyable=False, channelBox=True)
                        except:
                            print "Error: Cannot set", obj, ".", attr, "as nonKeayble, sorry."


    def setNotRenderable(self, objList, *args):
        """Receive a list of objects, find its shapes if necessary and set all as not renderable.
        """
        # declare a list of attributes for render:
        renderAttrList = ["castsShadows", "receiveShadows", "motionBlur", "primaryVisibility", "smoothShading", "visibleInReflections", "visibleInRefractions", "doubleSided", "miTransparencyCast", "miTransparencyReceive", "miReflectionReceive", "miRefractionReceive", "miFinalGatherCast", "miFinalGatherReceive"]
        shapeTypeList = ['nurbsCurve', 'nurbsSurface', 'mesh', 'subdiv']
        # find all children shapes:
        if objList:
            for obj in objList:
                objType = cmds.objectType(obj)
                # verify if the object is the shape type:
                if objType in shapeTypeList:
                    # set attributes as not renderable:
                    for attr in renderAttrList:
                        try:
                            cmds.setAttr(obj+"."+attr, 0)
                        except:
                            #print "Error: Cannot set not renderable ", attr, "as zero for", obj
                            pass
                # verify if the object is a transform type:
                elif objType == "transform":
                    # find all shapes children of the transform object:
                    shapeList = cmds.listRelatives(obj, shapes=True, children=True)
                    if shapeList:
                        for shape in shapeList:
                            # set attributes as not renderable:
                            for attr in renderAttrList:
                                try:
                                    cmds.setAttr(shape+"."+attr, 0)
                                except:
                                    #print "Error: Cannot set not renderable ", attr, "as zero for", shape
                                    pass


    def distanceBet(self, a, b, name="temp_DistBet", keep=False, *args):
        """ Creates a distance between node for 2 objects a and b.
            Keeps them in the scene or delete.
            Returns the distance value only in case of not keeping distBet node or
            a list of distance value, distanceNode and two nulls used to calculate.
        """
        if cmds.objExists(a) and cmds.objExists(b):
            if keep:
                # create nulls:
                nullA = cmds.group(empty=True, name=a+"_DistBetNull")
                nullB = cmds.group(empty=True, name=b+"_DistBetNull")
                nullC = cmds.group(empty=True, name=b+"_DistBetNull_OrigRef")
                cmds.pointConstraint(a, nullA, maintainOffset=False, name=nullA+"_ParentConstraint")
                cmds.pointConstraint(b, nullB, maintainOffset=False, name=nullB+"_ParentConstraint")
                tempToDel = cmds.pointConstraint(b, nullC, maintainOffset=False)
                cmds.delete(tempToDel)
                pointConst = cmds.pointConstraint(b, nullC, nullB, maintainOffset=False, name=nullB+"_ParentConstraint")[0]
                # create distanceBetween node:
                distBet = cmds.shadingNode("distanceBetween", n=name, asUtility=True)
                # connect aPos to the distance between point1:
                cmds.connectAttr(nullA+".tx", distBet+".point1X")
                cmds.connectAttr(nullA+".ty", distBet+".point1Y")
                cmds.connectAttr(nullA+".tz", distBet+".point1Z")
                # connect bPos to the distance between point2:
                cmds.connectAttr(nullB+".tx", distBet+".point2X")
                cmds.connectAttr(nullB+".ty", distBet+".point2Y")
                cmds.connectAttr(nullB+".tz", distBet+".point2Z")
                dist = cmds.getAttr(distBet+".distance")
                return [dist, distBet, nullA, nullB, nullC, pointConst]
            else:
                # get xform datas:
                aPos = cmds.xform(a, query=True, worldSpace=True, translation=True)
                bPos = cmds.xform(b, query=True, worldSpace=True, translation=True)
                # create distanceBetween node:
                distBet = cmds.shadingNode("distanceBetween", n=name, asUtility=True)
                # set aPos to the distance between point1:
                cmds.setAttr(distBet+".point1X", aPos[0])
                cmds.setAttr(distBet+".point1Y", aPos[1])
                cmds.setAttr(distBet+".point1Z", aPos[2])
                # set bPos to the distance between point2:
                cmds.setAttr(distBet+".point2X", bPos[0])
                cmds.setAttr(distBet+".point2Y", bPos[1])
                cmds.setAttr(distBet+".point2Z", bPos[2])
                dist = cmds.getAttr(distBet+".distance")
                cmds.delete(distBet)
                return [dist, None, None, None, None, None]


    def middlePoint(self, a, b, createLocator=False, *args):
        """ Find the point location in the middle of two items.
            Return the middle point position as a vector and a locator in it if want.
        """
        if cmds.objExists(a) and cmds.objExists(b):
            # get xform datas:
            aPos = cmds.xform(a, query=True, worldSpace=True, rotatePivot=True)
            bPos = cmds.xform(b, query=True, worldSpace=True, rotatePivot=True)
            # calculating the result position:
            resultPosX = ( aPos[0] + bPos[0] )/2
            resultPosY = ( aPos[1] + bPos[1] )/2
            resultPosZ = ( aPos[2] + bPos[2] )/2
            resultPos = [resultPosX, resultPosY, resultPosZ]
            if createLocator:
                middleLoc = cmds.spaceLocator(name=a+"_"+b+"_Middle_Loc", position=resultPos)[0]
                cmds.xform(middleLoc, centerPivots=True)
                return [resultPos, middleLoc]
            return[resultPos]


    def createSimpleRibbon(self, name='ribbon', totalJoints=6, jointLabelNumber=0, jointLabelName="SimpleRibbon", *args):
        """ Creates a Ribbon system.
            Receives the total number of joints to create.
            Returns the ribbon nurbs plane, the joints groups and joints created.
        """
        # create a ribbonNurbsPlane:
        ribbonNurbsPlane = cmds.nurbsPlane(name=name+"RibbonNurbsPlane", constructionHistory=False, object=True, polygon=0, axis=(0, 1, 0), width=1, lengthRatio=8, patchesV=totalJoints)[0]
        # get the ribbonNurbsPlane shape:
        ribbonNurbsPlaneShape = cmds.listRelatives(ribbonNurbsPlane, shapes=True, children=True)[0]
        # make this ribbonNurbsPlane as template, invisible and not renderable:
        cmds.setAttr(ribbonNurbsPlane+".template", 1)
        cmds.setAttr(ribbonNurbsPlane+".visibility", 0)
        self.setNotRenderable([ribbonNurbsPlaneShape])
        # make this ribbonNurbsPlane as not skinable from dpAR_UI:
        cmds.addAttr(ribbonNurbsPlane, longName="doNotSkinIt", attributeType="bool", keyable=True)
        cmds.setAttr(ribbonNurbsPlane+".doNotSkinIt", 1)
        # create groups to be used as a root of the ribbon system:
        ribbonGrp = cmds.group(ribbonNurbsPlane, n=name+"_Rbn_RibbonJoint_Grp")
        # create joints:
        jointList, jointGrpList = [], []
        for j in range(totalJoints+1):
            # create pointOnSurfaceInfo:
            infoNode = cmds.createNode('pointOnSurfaceInfo', name=name+"_POSI"+str(j))
            # setting parameters worldSpace, U and V:
            cmds.connectAttr(ribbonNurbsPlaneShape + ".worldSpace[0]", infoNode + ".inputSurface")
            cmds.setAttr(infoNode + ".parameterV", ((1/float(totalJoints))*j) )
            cmds.setAttr(infoNode + ".parameterU", 0.5)
            # create and parent groups to calculate:
            posGrp = cmds.group(n=name+"Pos"+str(j)+"_Grp", empty=True)
            upGrp  = cmds.group(n=name+"Up"+str(j)+"_Grp", empty=True)
            aimGrp = cmds.group(n=name+"Aim"+str(j)+"_Grp", empty=True)
            cmds.parent(upGrp, aimGrp, posGrp, relative=True)
            # connect groups translations:
            cmds.connectAttr(infoNode + ".position", posGrp + ".translate", force=True)
            cmds.connectAttr(infoNode + ".tangentU", upGrp + ".translate", force=True)
            cmds.connectAttr(infoNode + ".tangentV", aimGrp + ".translate", force=True)
            # create joint:
            cmds.select(clear=True)
            joint = cmds.joint(name=name+"_%02d_Jnt"%j)
            jointList.append(joint)
            cmds.addAttr(joint, longName='dpAR_joint', attributeType='float', keyable=False)
            # parent the joint to the groups:
            cmds.parent(joint, posGrp, relative=True)
            jointGrp = cmds.group(joint, name=name+"Joint"+str(j)+"_Grp")
            jointGrpList.append(jointGrp)
            # create aimConstraint from aimGrp to jointGrp:
            cmds.aimConstraint(aimGrp, jointGrp, offset=(0, 0, 0), weight=1, aimVector=(0, 1, 0), upVector=(0, 0, 1), worldUpType="object", worldUpObject=upGrp, n=name+"Ribbon"+str(j)+"_AimConstraint" )
            # parent this ribbonPos to the ribbonGrp:
            cmds.parent(posGrp, ribbonGrp, absolute=True)
            # joint labelling:
            utils.setJointLabel(joint, jointLabelNumber, 18, jointLabelName+"_%02d"%j)
        return [ribbonNurbsPlane, ribbonNurbsPlaneShape, jointGrpList, jointList]


    def getControlModuleById(self, ctrlType, *args):
        """ Check the control type reading the loaded dictionary from preset json file.
            Return the respective control module name by id.
        """
        ctrlModule = self.presetDic[self.presetName][ctrlType]
        return ctrlModule


    def getControlInstance(self, instanceName, *args):
        """ Find the loaded control instance by name.
            Return the instance found.
        """
        if self.dpUIinst.controlInstanceList:
            for instance in self.dpUIinst.controlInstanceList:
                if instance.guideModuleName == instanceName:
                    return instance


    def cvControl(self, ctrlType, ctrlName, r=1, d=1, dir='+Y', rot=(0, 0, 0), *args):
        """ Create and return a curve to be used as a control.
            Check if the ctrlType starts with 'id_###_Abc' and get the control type from json file.
            Otherwise, check if ctrlType is a valid control curve object in order to create it.
        """
        # get control module:
        if ctrlType.startswith("id_"):
            ctrlModule = self.getControlModuleById(ctrlType)
        else:
            ctrlModule = ctrlType
        # get control instance:
        controlInstance = self.getControlInstance(ctrlModule)
        if controlInstance:
            # create curve
            curve = controlInstance.cvMain(False, ctrlType, ctrlName, r, d, dir, 1)
            # rotate and freezeTransformation
            cmds.rotate(rot[0], rot[1], rot[2], curve)
            cmds.makeIdentity(curve, rotate=True, apply=True)
            return curve


    def cvLocator(self, ctrlName, r=1, d=1, guide=False, *args):
        """Create and return a cvLocator curve to be usually used in the guideSystem and the clusterHandle to shapeSize.
        """
        curveInstance = self.getControlInstance("Locator")
        curve = curveInstance.cvMain(False, "Locator", ctrlName, r, d, '+Y', 1, guide)
        if guide:
            # create an attribute to be used as guide by module:
            cmds.addAttr(curve, longName="nJoint", attributeType='long')
            cmds.setAttr(curve+".nJoint", 1)
            # colorize curveShape:
            self.colorShape([curve], 'blue')
            # shapeSize setup:
            shapeSizeCluster = self.shapeSizeSetup(curve)
            return [curve, shapeSizeCluster]
        return curve


    #@utils.profiler
    def cvJointLoc(self, ctrlName, r=0.3, extraLocs=False, d=1, guide=True, *args):
        """Create and return a cvJointLocator curve to be usually used in the guideSystem and the clusterHandle to shapeSize.
        """
        # create locator curve:
        cvLoc = self.cvLocator(ctrlName+"_CvLoc", r, d)
        # create arrow curves:
        cvArrow1 = cmds.curve(n=ctrlName+"_CvArrow1", d=3, p=[(-0.1*r, 0.9*r, 0.2*r), (-0.1*r, 0.9*r, 0.23*r), (-0.1*r, 0.9*r, 0.27*r), (-0.1*r, 0.9*r, 0.29*r), (-0.1*r, 0.9*r, 0.3*r), (-0.372*r, 0.9*r, 0.24*r), (-0.45*r, 0.9*r, -0.13*r), (-0.18*r, 0.9*r, -0.345*r), (-0.17*r, 0.9*r, -0.31*r), (-0.26*r, 0.9*r, -0.41*r), (-0.21*r, 0.9*r, -0.41*r), (-0.05*r, 0.9*r, -0.4*r), (0, 0.9*r, -0.4*r), (-0.029*r, 0.9*r, -0.33*r), (-0.048*r, 0.9*r, -0.22*r), (-0.055*r, 0.9*r, -0.16*r), (-0.15*r, 0.9*r, -0.272*r), (-0.12*r, 0.9*r, -0.27*r), (-0.35*r, 0.9*r, -0.1*r), (-0.29*r, 0.9*r, 0.15*r), (-0.16*r, 0.9*r, 0.21*r), (-0.1*r, 0.9*r, 0.2*r)] )
        cvArrow2 = cmds.curve(n=ctrlName+"_CvArrow2", d=3, p=[(0.1*r, 0.9*r, -0.2*r), (0.1*r, 0.9*r, -0.23*r), (0.1*r, 0.9*r, -0.27*r), (0.1*r, 0.9*r, -0.29*r), (0.1*r, 0.9*r, -0.3*r), (0.372*r, 0.9*r, -0.24*r), (0.45*r, 0.9*r, 0.13*r), (0.18*r, 0.9*r, 0.345*r), (0.17*r, 0.9*r, 0.31*r), (0.26*r, 0.9*r, 0.41*r), (0.21*r, 0.9*r, 0.41*r), (0.05*r, 0.9*r, 0.4*r), (0, 0.9*r, 0.4*r), (0.029*r, 0.9*r, 0.33*r), (0.048*r, 0.9*r, 0.22*r), (0.055*r, 0.9*r, 0.16*r), (0.15*r, 0.9*r, 0.272*r), (0.12*r, 0.9*r, 0.27*r), (0.35*r, 0.9*r, 0.1*r), (0.29*r, 0.9*r, -0.15*r), (0.16*r, 0.9*r, -0.21*r), (0.1*r, 0.9*r, -0.2*r)] )
        cvArrow3 = cmds.curve(n=ctrlName+"_CvArrow3", d=3, p=[(-0.1*r, -0.9*r, 0.2*r), (-0.1*r, -0.9*r, 0.23*r), (-0.1*r, -0.9*r, 0.27*r), (-0.1*r, -0.9*r, 0.29*r), (-0.1*r, -0.9*r, 0.3*r), (-0.372*r, -0.9*r, 0.24*r), (-0.45*r, -0.9*r, -0.13*r), (-0.18*r, -0.9*r, -0.345*r), (-0.17*r, -0.9*r, -0.31*r), (-0.26*r, -0.9*r, -0.41*r), (-0.21*r, -0.9*r, -0.41*r), (-0.05*r, -0.9*r, -0.4*r), (0, -0.9*r, -0.4*r), (-0.029*r, -0.9*r, -0.33*r), (-0.048*r, -0.9*r, -0.22*r), (-0.055*r, -0.9*r, -0.16*r), (-0.15*r, -0.9*r, -0.272*r), (-0.12*r, -0.9*r, -0.27*r), (-0.35*r, -0.9*r, -0.1*r), (-0.29*r, -0.9*r, 0.15*r), (-0.16*r, -0.9*r, 0.21*r), (-0.1*r, -0.9*r, 0.2*r)] )
        cvArrow4 = cmds.curve(n=ctrlName+"_CvArrow4", d=3, p=[(0.1*r, -0.9*r, -0.2*r), (0.1*r, -0.9*r, -0.23*r), (0.1*r, -0.9*r, -0.27*r), (0.1*r, -0.9*r, -0.29*r), (0.1*r, -0.9*r, -0.3*r), (0.372*r, -0.9*r, -0.24*r), (0.45*r, -0.9*r, 0.13*r), (0.18*r, -0.9*r, 0.345*r), (0.17*r, -0.9*r, 0.31*r), (0.26*r, -0.9*r, 0.41*r), (0.21*r, -0.9*r, 0.41*r), (0.05*r, -0.9*r, 0.4*r), (0, -0.9*r, 0.4*r), (0.029*r, -0.9*r, 0.33*r), (0.048*r, -0.9*r, 0.22*r), (0.055*r, -0.9*r, 0.16*r), (0.15*r, -0.9*r, 0.272*r), (0.12*r, -0.9*r, 0.27*r), (0.35*r, -0.9*r, 0.1*r), (0.29*r, -0.9*r, -0.15*r), (0.16*r, -0.9*r, -0.21*r), (0.1*r, -0.9*r, -0.2*r)] )
        cvArrow5 = cmds.curve(n=ctrlName+"_CvArrow5", d=1, p=[(0, 0, 1.2*r), (0.09*r, 0, 1*r), (-0.09*r, 0, 1*r), (0, 0, 1.2*r)] )
        cvArrow6 = cmds.curve(n=ctrlName+"_CvArrow6", d=1, p=[(0, 0, 1.2*r), (0, 0.09*r, 1*r), (0, -0.09*r, 1*r), (0, 0, 1.2*r)] )
        # rename curveShape:
        locArrowList = [cvLoc, cvArrow1, cvArrow2, cvArrow3, cvArrow4, cvArrow5, cvArrow6]
        self.renameShape(locArrowList)
        # create ball curve:
        cvTemplateBall = self.cvControl("Ball", ctrlName+"_CvBall", r=0.7*r, d=3)
        # parent shapes to transform:
        locCtrl = cmds.group(name=ctrlName, empty=True)
        ballChildrenList = cmds.listRelatives(cvTemplateBall, shapes=True, children=True)
        for ballChildren in ballChildrenList:
            cmds.setAttr(ballChildren+".template", 1)
        self.transferShape(True, False, cvTemplateBall, [locCtrl])
        for transform in locArrowList:
            self.transferShape(True, False, transform, [locCtrl])
        if extraLocs: # does not used yet.
            # create hided locators in order to use them as upAimOrient and fromAimOrient to further joint:
            cvUpAim = self.cvLocator(ctrlName+"_CvUpAim", (0.25*r), d)
            cmds.xform(cvUpAim, ws=True, a=True, t=(r, 0, 0))
            cmds.setAttr(cvUpAim+".visibility", 0)
            cvFrontAim = self.cvLocator(ctrlName+"_CvFrontAim", (0.25*r), d)
            cmds.xform(cvFrontAim, ws=True, a=True, t=(0, 0, r))
            cmds.setAttr(cvFrontAim+".visibility", 0)
            cmds.parent(cvUpAim, cvFrontAim, locCtrl, relative=True)
        # create an attribute to be used as guide by module:
        cmds.addAttr(locCtrl, longName="nJoint", attributeType='long')
        cmds.setAttr(locCtrl+".nJoint", 1)
        # colorize curveShapes:
        self.colorShape([locCtrl], 'blue')
        # shapeSize setup:
        shapeSizeCluster = self.shapeSizeSetup(locCtrl)
        cmds.select(clear=True)
        return [locCtrl, shapeSizeCluster]
    
    
    def cvCharacter(self, ctrlType, ctrlName, r=1, d=1, dir="+Y", *args):
        """ Create and return a curve to be used as a control.
        """
        # get radius by checking linear unit
        r = self.dpCheckLinearUnit(r)
        curve = self.cvControl(ctrlType, ctrlName, r, d, dir)
        # edit a minime curve:
        cmds.addAttr(curve, longName="rigScale", attributeType='float', defaultValue=1, keyable=True)
        cmds.addAttr(curve, longName="rigScaleMultiplier", attributeType='float', defaultValue=1, keyable=False)
        
        # create Option_Ctrl Text:
        try:
            optCtrlTxt = cmds.group(name="Option_Ctrl_Txt", empty=True)
            try:
                cvText = cmds.textCurves(name="Option_Ctrl_Txt_TEMP_Grp", font="Source Sans Pro", text="Option Ctrl", constructionHistory=False)[0]
            except:
                cvText = cmds.textCurves(name="Option_Ctrl_Txt_TEMP_Grp", font="Arial", text="Option Ctrl", constructionHistory=False)[0]
            txtShapeList = cmds.listRelatives(cvText, allDescendents=True, type='nurbsCurve')
            if txtShapeList:
                for s, shape in enumerate(txtShapeList):
                    # store CV world position
                    curveCVList = cmds.getAttr(shape+'.cp', multiIndices=True)
                    vtxWorldPosition = []
                    for i in curveCVList :
                        cvPointPosition = cmds.xform(shape+'.cp['+str(i)+']', query=True, translation=True, worldSpace=True) 
                        vtxWorldPosition.append(cvPointPosition)
                    # parent the shapeNode :
                    cmds.parent(shape, optCtrlTxt, r=True, s=True)
                    # restore the shape world position
                    for i in curveCVList:
                        cmds.xform(shape+'.cp['+str(i)+']', a=True, worldSpace=True, t=vtxWorldPosition[i])
                    cmds.rename(shape, optCtrlTxt+"Shape"+str(s))
            cmds.delete(cvText)
            cmds.parent(optCtrlTxt, curve)
            cmds.setAttr(optCtrlTxt+".template", 1)
            cmds.setAttr(optCtrlTxt+".tx", -0.72*r)
            cmds.setAttr(optCtrlTxt+".ty", 1.1*r)
        except:
            # it will pass if we don't able to find the font to create the text
            pass
        return curve


    def findHistory(self, objList, historyName, *args):
        """Search and return the especific history of the listed objects.
        """
        if objList:
            foundHistoryList = []
            for objName in objList:
                # find historyName in the object's history:
                histList = cmds.listHistory(objName)
                for hist in histList:
                    histType = cmds.objectType(hist)
                    if histType == historyName:
                        foundHistoryList.append(hist)
            return foundHistoryList
    
    
    def cvBaseGuide(self, ctrlName, r=1, *args):
        """Create a control to be used as a Base Guide control.
            Returns the main control (circle) and the radius control in a list.
        """
        # get radius by checking linear unit
        r = self.dpCheckLinearUnit(r)
        # create a simple circle curve:
        circle = cmds.circle(n=ctrlName, ch=True, o=True, nr=(0, 0, 1), d=3, s=8, radius=r)[0]
        radiusCtrl = cmds.circle(n=ctrlName+"_RadiusCtrl", ch=True, o=True, nr=(0, 1, 0), d=3, s=8, radius=(r/4.0))[0]
        # rename curveShape:
        self.renameShape([circle, radiusCtrl])
        # configure system of limits and radius:
        cmds.setAttr(radiusCtrl+".translateX", r)
        cmds.parent(radiusCtrl, circle, relative=True)
        cmds.transformLimits(radiusCtrl, tx=(0.01, 1), etx=(True, False))
        self.setLockHide([radiusCtrl], ['ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'])
        # find makeNurbCircle history of the circles:
        historyList = self.findHistory([circle, radiusCtrl], 'makeNurbCircle')
        circleHistory     = historyList[0]
        radiusCtrlHistory = historyList[1]
        # rename and make a connection for circle:
        circleHistory = cmds.rename(circleHistory, circle+"_makeNurbCircle")
        cmds.connectAttr(radiusCtrl+".tx", circleHistory+".radius", force=True)
        radiusCtrlHistory = cmds.rename(radiusCtrlHistory, radiusCtrl+"_makeNurbCircle")
        # create a mutiplyDivide in order to automatisation the radius of the radiusCtrl:
        radiusCtrlMD = cmds.createNode('multiplyDivide', name=radiusCtrl+'_MD')
        cmds.connectAttr(radiusCtrl+'.translateX', radiusCtrlMD+'.input1X', force=True)
        cmds.setAttr(radiusCtrlMD+'.input2X', 0.15)
        cmds.connectAttr(radiusCtrlMD+".outputX", radiusCtrlHistory+".radius", force=True)
        # colorize curveShapes:
        self.colorShape([circle], 'yellow')
        self.colorShape([radiusCtrl], 'cyan')
        cmds.setAttr(circle+"Shape.lineWidth", 2)
        cmds.select(clear=True)
        return [circle, radiusCtrl]
    
    
    def setAndFreeze(nodeName="", tx=None, ty=None, tz=None, rx=None, ry=None, rz=None, sx=None, sy=None, sz=None, freeze=True):
        """This function set attribute values and do a freezeTransfomation.
        """
        if nodeName != "":
            attrNameList  = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
            attrValueList = [tx, ty, tz, rx, ry, rz, sx, sy, sz]
            # setting attribute values:
            for v, attrValue in enumerate(attrValueList):
                if attrValue:
                    try:
                        cmds.setAttr(nodeName+'.'+attrNameList[v], attrValue)
                    except:
                        pass
            # looking the need of freeze:
            if freeze:
                freezeT = False
                freezeR = False
                freezeS = False
                if tx != None or ty != None or tz != None:
                    freezeT = True
                if rx != None or ry != None or rz != None:
                    freezeR = True
                if sx != None or sy != None or sz != None:
                    freezeS = True
                try:
                    cmds.makeIdentity(nodeName, apply=freeze, translate=freezeT, rotate=freezeR, scale=freezeS)
                except:
                    pass
    
    
    def transferShape(self, deleteSource=False, clearDestinationShapes=True, sourceItem=None, destinationList=None, applyColor=True, *args):
        """ Transfer control shape from sourceItem to destination list
        """
        if not sourceItem:
            selList = cmds.ls(selection=True, type="transform")
            if selList and len(selList) > 1:
                # get first selected item
                sourceItem = selList[0]
                # get other selected items
                destinationList = selList[1:]
        if sourceItem:
            sourceShapeList = cmds.listRelatives(sourceItem, shapes=True, type="nurbsCurve", fullPath=True)
            if sourceShapeList:
                if destinationList:
                    for destTransform in destinationList:
                        destShapeList = cmds.listRelatives(destTransform, shapes=True, type="nurbsCurve", fullPath=True)
                        if destShapeList:
                            if clearDestinationShapes:
                                cmds.delete(destShapeList)
                        dupSourceItem = cmds.duplicate(sourceItem)[0]
                        if applyColor:
                            self.setSourceColorOverride(dupSourceItem, [destTransform])
                        dupSourceShapeList = cmds.listRelatives(dupSourceItem, shapes=True, type="nurbsCurve", fullPath=True)
                        for dupSourceShape in dupSourceShapeList:
                            cmds.parent(dupSourceShape, destTransform, relative=True, shape=True)
                        cmds.delete(dupSourceItem)
                        self.renameShape([destTransform])
                    if deleteSource:
                        # update cvClassName:
                        if cmds.objExists(sourceItem+".className"):
                            if cmds.objExists(destTransform+".className"):
                                cmds.setAttr(destTransform+".className", cmds.getAttr(sourceItem+".className"), type="string")
                        cmds.delete(sourceItem)
    
    
    def setSourceColorOverride(self, sourceItem, destinationList, *args):
        """ Check if there's a colorOverride for destination shapes
            and try to set it to source shapes.
        """
        colorList = []
        for item in destinationList:
            childShapeList = cmds.listRelatives(item, children=True, shapes=True, noIntermediate=True, type="nurbsCurve")
            if childShapeList:
                for childShape in childShapeList:
                    if cmds.getAttr(childShape+".overrideEnabled") == 1:
                        if cmds.getAttr(childShape+".overrideRGBColors") == 1:
                            colorList.append(cmds.getAttr(childShape+".overrideColorR"))
                            colorList.append(cmds.getAttr(childShape+".overrideColorG"))
                            colorList.append(cmds.getAttr(childShape+".overrideColorB"))
                            self.colorShape([sourceItem], colorList, True)
                        else:
                            colorList.append(cmds.getAttr(childShape+".overrideColor"))
                            self.colorShape([sourceItem], colorList[0])
                        break
    
    
    def dpCheckLinearUnit(self, origRadius, defaultUnit="centimeter", *args):
        """ Verify if the Maya linear unit is in Centimeter.
            Return the radius to the new unit size.

            WIP!
            Changing to shapeSize cluster setup
        """
        newRadius = origRadius
    #    newRadius = 1
    #    linearUnit = cmds.currentUnit(query=True, linear=True, fullName=True)
    #    # centimeter
    #    if linearUnit == defaultUnit:
    #        newRadius = origRadius
    #    elif linearUnit == "meter":
    #        newRadius = origRadius*0.01
    #    elif linearUnit == "millimeter":
    #        newRadius = origRadius*10
    #    elif linearUnit == "inch":
    #        newRadius = origRadius*0.393701
    #    elif linearUnit == "foot":
    #        newRadius = origRadius*0.032808
    #    elif linearUnit == "yard":
    #        newRadius = origRadius*0.010936
        return newRadius
    
    
    #@utils.profiler
    def shapeSizeSetup(self, transformNode, *args):
        """ Find shapes, create a cluster deformer to all and set the pivot to transform pivot.
            Returns the created cluster.
        """
        clusterHandle = None
        childShapeList = cmds.listRelatives(transformNode, shapes=True, children=True)
    #    print "Child length {0}".format(len(childShapeList))
        if childShapeList:
            thisNamespace = childShapeList[0].split(":")[0]
            cmds.namespace(set=thisNamespace, force=True)
            clusterName = transformNode.split(":")[1]+"_ShapeSizeCH"
            clusterHandle = cmds.cluster(childShapeList, name=clusterName)[1]
            cmds.setAttr(clusterHandle+".visibility", 0)
            cmds.xform(clusterHandle, scalePivot=(0, 0, 0), worldSpace=True)
            cmds.namespace(set=":")
        else:
            print "There are not children shape to create shapeSize setup of:", transformNode
        return clusterHandle