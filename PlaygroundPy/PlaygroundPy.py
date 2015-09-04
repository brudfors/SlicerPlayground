import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import math
import time

#
# PlaygroundPy
#

class PlaygroundPy(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Playground" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Brudfors"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mikael Brudfors (UC3M)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# PlaygroundPyWidget
#

class PlaygroundPyWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    ############################################################ Playground
    playgroundCollapsibleButton = ctk.ctkCollapsibleButton()
    playgroundCollapsibleButton.text = "Playground"
    playgroundCollapsibleButton.collapsed = False
    self.layout.addWidget(playgroundCollapsibleButton)
    playgroundFormLayout = qt.QFormLayout(playgroundCollapsibleButton)

    # Load for testing
    self.loadTestModelButton = qt.QPushButton("Load Test Model")
    playgroundFormLayout.addRow(self.loadTestModelButton)    
    
    # ModelTipToToolCreator
    self.modelTipToToolCreatorGroupBox = ctk.ctkCollapsibleGroupBox()
    self.modelTipToToolCreatorGroupBox.setTitle("ModelTipToToolCreator")
    self.modelTipToToolCreatorGroupBox.collapsed = True
    modelTipToToolCreatorFormLayout = qt.QFormLayout(self.modelTipToToolCreatorGroupBox)
    playgroundFormLayout.addRow(self.modelTipToToolCreatorGroupBox)
    
    self.modeldistanceToModelToolTipToToolSelector = slicer.qMRMLNodeComboBox()
    self.modeldistanceToModelToolTipToToolSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.modeldistanceToModelToolTipToToolSelector.selectNodeUponCreation = True
    self.modeldistanceToModelToolTipToToolSelector.addEnabled = True
    self.modeldistanceToModelToolTipToToolSelector.editEnabled = False
    self.modeldistanceToModelToolTipToToolSelector.removeEnabled = True
    self.modeldistanceToModelToolTipToToolSelector.renameEnabled = True
    self.modeldistanceToModelToolTipToToolSelector.noneEnabled = False
    self.modeldistanceToModelToolTipToToolSelector.showHidden = False
    self.modeldistanceToModelToolTipToToolSelector.showChildNodeTypes = False
    self.modeldistanceToModelToolTipToToolSelector.setMRMLScene( slicer.mrmlScene )
    modelTipToToolCreatorFormLayout.addRow("ModelTipToTool: ", self.modeldistanceToModelToolTipToToolSelector)
    
    self.modelTipToToolCreatorByTransformsGroupBox = ctk.ctkCollapsibleGroupBox()
    self.modelTipToToolCreatorByTransformsGroupBox.setTitle("By Transforms")
    self.modelTipToToolCreatorByTransformsGroupBox.collapsed = False
    modelTipToToolCreatorByTransformsFormLayout = qt.QFormLayout(self.modelTipToToolCreatorByTransformsGroupBox)
    modelTipToToolCreatorFormLayout.addRow(self.modelTipToToolCreatorByTransformsGroupBox)
    
    self.tooldistanceToModelToolTipToToolSelector = slicer.qMRMLNodeComboBox()
    self.tooldistanceToModelToolTipToToolSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.tooldistanceToModelToolTipToToolSelector.selectNodeUponCreation = False
    self.tooldistanceToModelToolTipToToolSelector.addEnabled = False
    self.tooldistanceToModelToolTipToToolSelector.removeEnabled = False
    self.tooldistanceToModelToolTipToToolSelector.noneEnabled = False
    self.tooldistanceToModelToolTipToToolSelector.showHidden = False
    self.tooldistanceToModelToolTipToToolSelector.showChildNodeTypes = False
    self.tooldistanceToModelToolTipToToolSelector.setMRMLScene( slicer.mrmlScene )
    modelTipToToolCreatorByTransformsFormLayout.addRow("ToolTipToTool: ", self.tooldistanceToModelToolTipToToolSelector)
 
    self.modelTipToToolTipSelector = slicer.qMRMLNodeComboBox()
    self.modelTipToToolTipSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.modelTipToToolTipSelector.selectNodeUponCreation = False
    self.modelTipToToolTipSelector.addEnabled = False
    self.modelTipToToolTipSelector.removeEnabled = False
    self.modelTipToToolTipSelector.noneEnabled = False
    self.modelTipToToolTipSelector.showHidden = False
    self.modelTipToToolTipSelector.showChildNodeTypes = False
    self.modelTipToToolTipSelector.setMRMLScene( slicer.mrmlScene )
    modelTipToToolCreatorByTransformsFormLayout.addRow("ModelTipToToolTip: ", self.modelTipToToolTipSelector)
    
    self.toolToReferenceSelector = slicer.qMRMLNodeComboBox()
    self.toolToReferenceSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.toolToReferenceSelector.selectNodeUponCreation = False
    self.toolToReferenceSelector.addEnabled = False
    self.toolToReferenceSelector.removeEnabled = False
    self.toolToReferenceSelector.noneEnabled = False
    self.toolToReferenceSelector.showHidden = False
    self.toolToReferenceSelector.showChildNodeTypes = False
    self.toolToReferenceSelector.setMRMLScene( slicer.mrmlScene )
    modelTipToToolCreatorByTransformsFormLayout.addRow("ToolToReference: ", self.toolToReferenceSelector)
    
    self.applyModelTipToReferenceCreatorByTransformsButton = qt.QPushButton("Apply")
    self.applyModelTipToReferenceCreatorByTransformsButton.enabled = False
    modelTipToToolCreatorByTransformsFormLayout.addRow(self.applyModelTipToReferenceCreatorByTransformsButton)

    self.modelTipToToolCreatorByFiducialsGroupBox = ctk.ctkCollapsibleGroupBox()
    self.modelTipToToolCreatorByFiducialsGroupBox.setTitle("By Fiducials")
    self.modelTipToToolCreatorByFiducialsGroupBox.collapsed = False
    modelTipToToolCreatorByFiducialsFormLayout = qt.QFormLayout(self.modelTipToToolCreatorByFiducialsGroupBox)
    modelTipToToolCreatorFormLayout.addRow(self.modelTipToToolCreatorByFiducialsGroupBox)
    
    self.originFiducialSelector = slicer.qMRMLNodeComboBox()
    self.originFiducialSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.originFiducialSelector.selectNodeUponCreation = False
    self.originFiducialSelector.addEnabled = False
    self.originFiducialSelector.removeEnabled = False
    self.originFiducialSelector.noneEnabled = False
    self.originFiducialSelector.showHidden = False
    self.originFiducialSelector.showChildNodeTypes = False
    self.originFiducialSelector.setMRMLScene( slicer.mrmlScene )
    modelTipToToolCreatorByFiducialsFormLayout.addRow("Origin Fiducial: ", self.originFiducialSelector)
    
    self.fromFiducialSelector = slicer.qMRMLNodeComboBox()
    self.fromFiducialSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.fromFiducialSelector.selectNodeUponCreation = False
    self.fromFiducialSelector.addEnabled = False
    self.fromFiducialSelector.removeEnabled = False
    self.fromFiducialSelector.noneEnabled = False
    self.fromFiducialSelector.showHidden = False
    self.fromFiducialSelector.showChildNodeTypes = False
    self.fromFiducialSelector.setMRMLScene( slicer.mrmlScene )
    modelTipToToolCreatorByFiducialsFormLayout.addRow("From Fiducial: ", self.fromFiducialSelector)
    
    self.toFiducialSelector = slicer.qMRMLNodeComboBox()
    self.toFiducialSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.toFiducialSelector.selectNodeUponCreation = False
    self.toFiducialSelector.addEnabled = False
    self.toFiducialSelector.removeEnabled = False
    self.toFiducialSelector.noneEnabled = False
    self.toFiducialSelector.showHidden = False
    self.toFiducialSelector.showChildNodeTypes = False
    self.toFiducialSelector.setMRMLScene( slicer.mrmlScene )
    modelTipToToolCreatorByFiducialsFormLayout.addRow("To Fiducial: ", self.toFiducialSelector)

    self.applyModelTipToToolCreatorByFiducialsButton = qt.QPushButton("Apply")
    self.applyModelTipToToolCreatorByFiducialsButton.enabled = False
    modelTipToToolCreatorByFiducialsFormLayout.addRow(self.applyModelTipToToolCreatorByFiducialsButton)
    
    # FirstPersonView
    self.firstPersonViewGroupBox = ctk.ctkCollapsibleGroupBox()
    self.firstPersonViewGroupBox.setTitle("FirstPersonView")
    self.firstPersonViewGroupBox.collapsed = True
    firstPersonViewFormLayout = qt.QFormLayout(self.firstPersonViewGroupBox)
    playgroundFormLayout.addRow(self.firstPersonViewGroupBox)
    
    self.stylusTipSelector = slicer.qMRMLNodeComboBox()
    self.stylusTipSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.stylusTipSelector.selectNodeUponCreation = False
    self.stylusTipSelector.addEnabled = False
    self.stylusTipSelector.removeEnabled = False
    self.stylusTipSelector.noneEnabled = False
    self.stylusTipSelector.showHidden = False
    self.stylusTipSelector.showChildNodeTypes = False
    self.stylusTipSelector.setMRMLScene( slicer.mrmlScene )
    firstPersonViewFormLayout.addRow("StylusTip: ", self.stylusTipSelector)
        
    self.movingLRS_FiducialSelector = slicer.qMRMLNodeComboBox()
    self.movingLRS_FiducialSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.movingLRS_FiducialSelector.selectNodeUponCreation = True
    self.movingLRS_FiducialSelector.addEnabled = True
    self.movingLRS_FiducialSelector.editEnabled = False
    self.movingLRS_FiducialSelector.removeEnabled = True
    self.movingLRS_FiducialSelector.renameEnabled = True
    self.movingLRS_FiducialSelector.noneEnabled = False
    self.movingLRS_FiducialSelector.showHidden = False
    self.movingLRS_FiducialSelector.showChildNodeTypes = False
    self.movingLRS_FiducialSelector.setMRMLScene( slicer.mrmlScene )
    firstPersonViewFormLayout.addRow("Moving LRS Fiducials List: ", self.movingLRS_FiducialSelector)
    
    self.recordFirstPersonViewPointButton = qt.QPushButton(" Record Point")
    self.recordFirstPersonViewPointButton.enabled = False
    firstPersonViewFormLayout.addRow(self.recordFirstPersonViewPointButton)

    self.createFirstPersonViewButton = qt.QPushButton("Create First Person View")
    self.createFirstPersonViewButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.createFirstPersonViewButton.enabled = False
    firstPersonViewFormLayout.addRow(self.createFirstPersonViewButton)
    
    # Record points
    self.pointRecorderGroupBox = ctk.ctkCollapsibleGroupBox()
    self.pointRecorderGroupBox.setTitle("PointRecorder")
    self.pointRecorderGroupBox.collapsed = True
    pointRecorderFormLayout = qt.QFormLayout(self.pointRecorderGroupBox)
    playgroundFormLayout.addRow(self.pointRecorderGroupBox)

    self.pointerTransformSelector = slicer.qMRMLNodeComboBox()
    self.pointerTransformSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.pointerTransformSelector.selectNodeUponCreation = True
    self.pointerTransformSelector.addEnabled = True
    self.pointerTransformSelector.editEnabled = False
    self.pointerTransformSelector.removeEnabled = True
    self.pointerTransformSelector.renameEnabled = True
    self.pointerTransformSelector.noneEnabled = False
    self.pointerTransformSelector.showHidden = False
    self.pointerTransformSelector.showChildNodeTypes = False
    self.pointerTransformSelector.setMRMLScene( slicer.mrmlScene )
    pointRecorderFormLayout.addRow("Pointer Transform: ", self.pointerTransformSelector)
        
    self.pointerFiducialsSelector = slicer.qMRMLNodeComboBox()
    self.pointerFiducialsSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.pointerFiducialsSelector.selectNodeUponCreation = True
    self.pointerFiducialsSelector.addEnabled = True
    self.pointerFiducialsSelector.editEnabled = False
    self.pointerFiducialsSelector.removeEnabled = True
    self.pointerFiducialsSelector.renameEnabled = True
    self.pointerFiducialsSelector.noneEnabled = False
    self.pointerFiducialsSelector.showHidden = False
    self.pointerFiducialsSelector.showChildNodeTypes = False
    self.pointerFiducialsSelector.setMRMLScene( slicer.mrmlScene )
    pointRecorderFormLayout.addRow("Pointer Fiducials: ", self.pointerFiducialsSelector)  

    self.pointRecorderApplyButton = qt.QPushButton("Record Point")
    self.pointRecorderApplyButton.enabled = False
    pointRecorderFormLayout.addRow(self.pointRecorderApplyButton)
    
    # Texture Mapping
    self.textureMappingGroupBox = ctk.ctkCollapsibleGroupBox()
    self.textureMappingGroupBox.setTitle("TextureMapping")
    self.textureMappingGroupBox.collapsed = True
    textureMappingFormLayout = qt.QFormLayout(self.textureMappingGroupBox)
    playgroundFormLayout.addRow(self.textureMappingGroupBox)

    self.inputTextureSelector = slicer.qMRMLNodeComboBox()
    self.inputTextureSelector.nodeTypes = ["vtkMRMLVectorVolumeNode"]
    self.inputTextureSelector.selectNodeUponCreation = True
    self.inputTextureSelector.addEnabled = False
    self.inputTextureSelector.removeEnabled = False
    self.inputTextureSelector.noneEnabled = False
    self.inputTextureSelector.showHidden = False
    self.inputTextureSelector.showChildNodeTypes = False
    self.inputTextureSelector.setMRMLScene( slicer.mrmlScene )
    textureMappingFormLayout.addRow("Input Texture: ", self.inputTextureSelector)
    
    self.inputModelSelector = slicer.qMRMLNodeComboBox()
    self.inputModelSelector.nodeTypes = ["vtkMRMLModelNode"]
    self.inputModelSelector.selectNodeUponCreation = True
    self.inputModelSelector.addEnabled = False
    self.inputModelSelector.removeEnabled = False
    self.inputModelSelector.noneEnabled = False
    self.inputModelSelector.showHidden = False
    self.inputModelSelector.showChildNodeTypes = False
    self.inputModelSelector.setMRMLScene( slicer.mrmlScene )
    textureMappingFormLayout.addRow("Input Model: ", self.inputModelSelector)

    self.textureMappingApplyButton = qt.QPushButton("Apply")
    self.textureMappingApplyButton.enabled = False
    textureMappingFormLayout.addRow(self.textureMappingApplyButton)
    
    # Fiducial registration
    self.registrationGroupBox = ctk.ctkCollapsibleGroupBox()
    self.registrationGroupBox.setTitle("Fiducial Registration")
    self.registrationGroupBox.collapsed = True
    registrationFormLayout = qt.QFormLayout(self.registrationGroupBox)
    playgroundFormLayout.addRow(self.registrationGroupBox)
    
    self.registrationOutputSelector = slicer.qMRMLNodeComboBox()
    self.registrationOutputSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.registrationOutputSelector.selectNodeUponCreation = True
    self.registrationOutputSelector.addEnabled = True
    self.registrationOutputSelector.editEnabled = False
    self.registrationOutputSelector.removeEnabled = True
    self.registrationOutputSelector.renameEnabled = True
    self.registrationOutputSelector.noneEnabled = False
    self.registrationOutputSelector.showHidden = False
    self.registrationOutputSelector.showChildNodeTypes = False
    self.registrationOutputSelector.setMRMLScene( slicer.mrmlScene )
    registrationFormLayout.addRow("Output Transform: ", self.registrationOutputSelector)
        
    self.movingFiducialsSelector = slicer.qMRMLNodeComboBox()
    self.movingFiducialsSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.movingFiducialsSelector.selectNodeUponCreation = True
    self.movingFiducialsSelector.addEnabled = True
    self.movingFiducialsSelector.editEnabled = False
    self.movingFiducialsSelector.removeEnabled = True
    self.movingFiducialsSelector.renameEnabled = True
    self.movingFiducialsSelector.noneEnabled = False
    self.movingFiducialsSelector.showHidden = False
    self.movingFiducialsSelector.showChildNodeTypes = False
    self.movingFiducialsSelector.setMRMLScene( slicer.mrmlScene )
    registrationFormLayout.addRow("Moving Fiducials: ", self.movingFiducialsSelector)
    
    self.fixedFiducialsSelector = slicer.qMRMLNodeComboBox()
    self.fixedFiducialsSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.fixedFiducialsSelector.selectNodeUponCreation = True
    self.fixedFiducialsSelector.addEnabled = True
    self.fixedFiducialsSelector.editEnabled = False
    self.fixedFiducialsSelector.removeEnabled = True
    self.fixedFiducialsSelector.renameEnabled = True
    self.fixedFiducialsSelector.noneEnabled = False
    self.fixedFiducialsSelector.showHidden = False
    self.fixedFiducialsSelector.showChildNodeTypes = False
    self.fixedFiducialsSelector.setMRMLScene( slicer.mrmlScene )
    registrationFormLayout.addRow("Fixed Fiducials: ", self.fixedFiducialsSelector)
    
    self.errorLabel = qt.QLabel('0.0')
    registrationFormLayout.addRow("RMS Error: ", self.errorLabel)
    
    self.registrationApplyButton = qt.QPushButton("Apply")
    self.registrationApplyButton.enabled = False
    registrationFormLayout.addRow(self.registrationApplyButton)
    
    # PreviousToNextCalculator
    self.previousToNextCalculatorGroupBox = ctk.ctkCollapsibleGroupBox()
    self.previousToNextCalculatorGroupBox.setTitle("PreviousToNextCalculator")
    self.previousToNextCalculatorGroupBox.collapsed = True
    previousToNextCalculatorFormLayout = qt.QFormLayout(self.previousToNextCalculatorGroupBox)
    playgroundFormLayout.addRow(self.previousToNextCalculatorGroupBox)
    
    self.previousTransformSelector = slicer.qMRMLNodeComboBox()
    self.previousTransformSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.previousTransformSelector.selectNodeUponCreation = False
    self.previousTransformSelector.addEnabled = False
    self.previousTransformSelector.removeEnabled = False
    self.previousTransformSelector.noneEnabled = False
    self.previousTransformSelector.showHidden = False
    self.previousTransformSelector.showChildNodeTypes = False
    self.previousTransformSelector.setMRMLScene( slicer.mrmlScene )
    previousToNextCalculatorFormLayout.addRow("Select Previous: ", self.previousTransformSelector)
    
    self.nextTransformSelector = slicer.qMRMLNodeComboBox()
    self.nextTransformSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.nextTransformSelector.selectNodeUponCreation = False
    self.nextTransformSelector.addEnabled = False
    self.nextTransformSelector.removeEnabled = False
    self.nextTransformSelector.noneEnabled = False
    self.nextTransformSelector.showHidden = False
    self.nextTransformSelector.showChildNodeTypes = False
    self.nextTransformSelector.setMRMLScene( slicer.mrmlScene )
    previousToNextCalculatorFormLayout.addRow("Select Next: ", self.nextTransformSelector)
    
    self.previousToNextTransformSelector = slicer.qMRMLNodeComboBox()
    self.previousToNextTransformSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.previousToNextTransformSelector.selectNodeUponCreation = True
    self.previousToNextTransformSelector.addEnabled = True
    self.previousToNextTransformSelector.editEnabled = False
    self.previousToNextTransformSelector.removeEnabled = True
    self.previousToNextTransformSelector.renameEnabled = True
    self.previousToNextTransformSelector.noneEnabled = False
    self.previousToNextTransformSelector.showHidden = False
    self.previousToNextTransformSelector.showChildNodeTypes = False
    self.previousToNextTransformSelector.setMRMLScene( slicer.mrmlScene )
    previousToNextCalculatorFormLayout.addRow("Select PreviousToNext: ", self.previousToNextTransformSelector)
    
    self.calculatePreviousToNextButton = qt.QPushButton("Calculate")
    self.calculatePreviousToNextButton.enabled = False
    previousToNextCalculatorFormLayout.addRow(self.calculatePreviousToNextButton)  
    
    # TransformPolyData
    self.transformPolyDataGroupBox = ctk.ctkCollapsibleGroupBox()
    self.transformPolyDataGroupBox.setTitle("TransformPolyData")
    self.transformPolyDataGroupBox.collapsed = True
    transformPolyDataFormLayout = qt.QFormLayout(self.transformPolyDataGroupBox)
    playgroundFormLayout.addRow(self.transformPolyDataGroupBox)
    
    self.transformPolyDataModelSelector = slicer.qMRMLNodeComboBox()
    self.transformPolyDataModelSelector.nodeTypes = ["vtkMRMLModelNode"]
    self.transformPolyDataModelSelector.selectNodeUponCreation = False
    self.transformPolyDataModelSelector.addEnabled = False
    self.transformPolyDataModelSelector.removeEnabled = False
    self.transformPolyDataModelSelector.noneEnabled = False
    self.transformPolyDataModelSelector.showHidden = False
    self.transformPolyDataModelSelector.showChildNodeTypes = False
    self.transformPolyDataModelSelector.setMRMLScene( slicer.mrmlScene )
    transformPolyDataFormLayout.addRow("Select Model: ", self.transformPolyDataModelSelector)
    
    self.transformPolyDataSelector = slicer.qMRMLNodeComboBox()
    self.transformPolyDataSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.transformPolyDataSelector.selectNodeUponCreation = True
    self.transformPolyDataSelector.addEnabled = True
    self.transformPolyDataSelector.editEnabled = False
    self.transformPolyDataSelector.removeEnabled = True
    self.transformPolyDataSelector.renameEnabled = True
    self.transformPolyDataSelector.noneEnabled = False
    self.transformPolyDataSelector.showHidden = False
    self.transformPolyDataSelector.showChildNodeTypes = False
    self.transformPolyDataSelector.setMRMLScene( slicer.mrmlScene )
    transformPolyDataFormLayout.addRow("Select Transform: ", self.transformPolyDataSelector)
    
    self.applyTransformPolyDataButton = qt.QPushButton("Apply")
    self.applyTransformPolyDataButton.enabled = False
    transformPolyDataFormLayout.addRow(self.applyTransformPolyDataButton)
    
    # FiducialToModelDistance
    self.fiducialTestingGroupBox = ctk.ctkCollapsibleGroupBox()
    self.fiducialTestingGroupBox.setTitle("FiducialToModelDistance")
    self.fiducialTestingGroupBox.collapsed = True
    fiducialTestingFormLayout = qt.QFormLayout(self.fiducialTestingGroupBox)
    playgroundFormLayout.addRow(self.fiducialTestingGroupBox)
    
    self.fiducialTestingModelSelector = slicer.qMRMLNodeComboBox()
    self.fiducialTestingModelSelector.nodeTypes = ["vtkMRMLModelNode"]
    self.fiducialTestingModelSelector.selectNodeUponCreation = False
    self.fiducialTestingModelSelector.addEnabled = False
    self.fiducialTestingModelSelector.removeEnabled = False
    self.fiducialTestingModelSelector.noneEnabled = False
    self.fiducialTestingModelSelector.showHidden = False
    self.fiducialTestingModelSelector.showChildNodeTypes = False
    self.fiducialTestingModelSelector.setMRMLScene( slicer.mrmlScene )
    fiducialTestingFormLayout.addRow("Select Model: ", self.fiducialTestingModelSelector)
    
    self.outerPointSelector = slicer.qMRMLNodeComboBox()
    self.outerPointSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.outerPointSelector.selectNodeUponCreation = True
    self.outerPointSelector.addEnabled = True
    self.outerPointSelector.editEnabled = False
    self.outerPointSelector.removeEnabled = True
    self.outerPointSelector.renameEnabled = True
    self.outerPointSelector.noneEnabled = False
    self.outerPointSelector.showHidden = False
    self.outerPointSelector.showChildNodeTypes = False
    self.outerPointSelector.setMRMLScene( slicer.mrmlScene )
    fiducialTestingFormLayout.addRow("Select Point: ", self.outerPointSelector)
    
    self.calculateFiducialDistanceButton = qt.QPushButton("Calculate Distance")
    self.calculateFiducialDistanceButton.enabled = False
    fiducialTestingFormLayout.addRow(self.calculateFiducialDistanceButton)  

    # CastToDouble
    self.castToDoubleGroupBox = ctk.ctkCollapsibleGroupBox()
    self.castToDoubleGroupBox.setTitle("CastToDouble")
    self.castToDoubleGroupBox.collapsed = True
    castToDoubleFormLayout = qt.QFormLayout(self.castToDoubleGroupBox)
    playgroundFormLayout.addRow(self.castToDoubleGroupBox)
    
    self.castToDoubleSelector = slicer.qMRMLNodeComboBox()
    self.castToDoubleSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.castToDoubleSelector.selectNodeUponCreation = False
    self.castToDoubleSelector.addEnabled = False
    self.castToDoubleSelector.removeEnabled = False
    self.castToDoubleSelector.noneEnabled = False
    self.castToDoubleSelector.showHidden = False
    self.castToDoubleSelector.showChildNodeTypes = False
    self.castToDoubleSelector.setMRMLScene( slicer.mrmlScene )
    castToDoubleFormLayout.addRow("Select Volume: ", self.castToDoubleSelector)
    
    self.castToDoubleButton = qt.QPushButton("Apply")
    self.castToDoubleButton.enabled = False
    castToDoubleFormLayout.addRow(self.castToDoubleButton)  
    
    ############################################### Connnections
    # Load for testing
    self.loadTestModelButton.connect('clicked(bool)', self.onLoadTestModelButton)
    # FirstPersonView
    self.stylusTipSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.recordFirstPersonViewPointButton.connect('clicked(bool)', self.onRecordFirstPersonViewPointButton)
    self.createFirstPersonViewButton.connect('clicked(bool)', self.onCreateFirstPersonViewButton)
    self.movingLRS_FiducialSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # ModelTipToReferenceCreator
    self.modeldistanceToModelToolTipToToolSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.applyModelTipToReferenceCreatorByTransformsButton.connect('clicked(bool)', self.onApplyModelTipToReferenceCreatorByTransformsButton)
    self.applyModelTipToToolCreatorByFiducialsButton.connect('clicked(bool)', self.onApplymodelTipToToolCreatorByFiducialsButton)
    self.tooldistanceToModelToolTipToToolSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.toolToReferenceSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.modelTipToToolTipSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)    
    self.originFiducialSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.fromFiducialSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.toFiducialSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # Record points
    self.pointerTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.pointerFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.pointRecorderApplyButton.connect('clicked(bool)', self.onPointRecorderApplyButton)
    # Texture Mapping
    self.textureMappingApplyButton.connect('clicked(bool)', self.onTextureMappingApplyButton)
    self.inputModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputTextureSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # Fiducial registration
    self.registrationApplyButton.connect('clicked(bool)', self.onRegistrationApplyButton)
    self.registrationOutputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.movingFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.fixedFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # PreviousToNextCalculator
    self.calculatePreviousToNextButton.connect('clicked(bool)', self.onCalculatePreviousToNextClicked)
    self.previousTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.nextTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.previousToNextTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # TransformPolyData
    self.applyTransformPolyDataButton.connect('clicked(bool)', self.onApplyTransformPolyDataClicked)
    self.transformPolyDataSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)   
    self.transformPolyDataModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)   
    # FiducialToModelDistance
    self.outerPointSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.fiducialTestingModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.calculateFiducialDistanceButton.connect('clicked(bool)', self.onCalculateFiducialDistanceClicked)
    # CastToDouble
    self.castToDoubleSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.castToDoubleButton.connect('clicked(bool)', self.onCastToDoubleClicked)
    
    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()
    
  def onSelect(self):
    # ModelTipToReferenceCreator
    self.applyModelTipToReferenceCreatorByTransformsButton.enabled = self.tooldistanceToModelToolTipToToolSelector.currentNode() and self.toolToReferenceSelector.currentNode() and self.modeldistanceToModelToolTipToToolSelector.currentNode() and self.modelTipToToolTipSelector.currentNode()
    self.applyModelTipToToolCreatorByFiducialsButton.enabled = self.originFiducialSelector.currentNode() and self.fromFiducialSelector.currentNode() and self.toFiducialSelector.currentNode() and self.modeldistanceToModelToolTipToToolSelector.currentNode()
    # FirstPersonView
    self.recordFirstPersonViewPointButton.enabled = self.movingLRS_FiducialSelector.currentNode() and self.stylusTipSelector.currentNode()
    self.createFirstPersonViewButton.enabled = self.movingLRS_FiducialSelector.currentNode()
    # Record points
    self.pointRecorderApplyButton.enabled = self.pointerTransformSelector.currentNode() and self.pointerFiducialsSelector.currentNode()
    # Texture Mapping 
    self.textureMappingApplyButton.enabled = self.inputModelSelector.currentNode() and self.inputTextureSelector.currentNode()     
    # Fiducial registration
    self.registrationApplyButton.enabled = self.registrationOutputSelector.currentNode() and self.movingFiducialsSelector.currentNode() and self.fixedFiducialsSelector.currentNode()
    # PreviousToNextCalculator
    self.calculatePreviousToNextButton.enabled = self.previousTransformSelector.currentNode() and self.nextTransformSelector.currentNode() and self.previousToNextTransformSelector.currentNode()
    # TransformPolyData
    self.applyTransformPolyDataButton.enabled = self.transformPolyDataSelector.currentNode() and self.transformPolyDataModelSelector.currentNode()
    # FiducialToModelDistance
    self.calculateFiducialDistanceButton.enabled = self.outerPointSelector.currentNode() and self.fiducialTestingModelSelector.currentNode()
    # CastToDouble
    self.castToDoubleButton.enabled = self.castToDoubleSelector.currentNode()
  
  # Load for testing
  def onLoadTestModelButton(self):
    testModel = slicer.util.getNode('TumorModel')
    if not testModel:
      slicer.util.loadModel('C:/Mikael/src/playground/Data/TumorModel.vtk')
      testModel = slicer.util.getNode(pattern="TumorModel")      
      modelDisplayNode = testModel.GetModelDisplayNode()
      modelDisplayNode.SliceIntersectionVisibilityOn()
      modelDisplayNode.SetColor(1,0,0)   
      
  # FirstPersonView
  def onRecordFirstPersonViewPointButton(self):
    logic = PlaygroundPyLogic()
    logic.recordPoint(self.movingLRS_FiducialSelector.currentNode(), self.stylusTipSelector.currentNode())
  
  def onCreateFirstPersonViewButton(self):
    logic = PlaygroundPyLogic()
    logic.createMovingLRSToFixedLRS(self.movingLRS_FiducialSelector.currentNode())
    logic.setFirstPersonView()
    
  # ModelTipToReferenceCreator
  def onApplyModelTipToReferenceCreatorByTransformsButton(self):
    logic = PlaygroundPyLogic()
    logic.modelTipToToolCreatorByTransforms(self.tooldistanceToModelToolTipToToolSelector.currentNode(), self.modelTipToToolTipSelector.currentNode(), self.toolToReferenceSelector.currentNode(), self.modeldistanceToModelToolTipToToolSelector.currentNode())
    
  def onApplymodelTipToToolCreatorByFiducialsButton(self):
    logic = PlaygroundPyLogic()
    logic.modelTipToToolCreatorByFiducials(self.originFiducialSelector.currentNode(), self.fromFiducialSelector.currentNode(), self.toFiducialSelector.currentNode(), self.modeldistanceToModelToolTipToToolSelector.currentNode())
  
  # TransformPolyData
  def onApplyTransformPolyDataClicked(self):
    logic = PlaygroundPyLogic()
    logic.transformPolyData(self.transformPolyDataModelSelector.currentNode(), self.transformPolyDataSelector.currentNode())
  
  # FiducialToModelDistance
  def onCalculateFiducialDistanceClicked(self):
    logic = PlaygroundPyLogic() 
    logic.calculateFiducialDistance(self.fiducialTestingModelSelector.currentNode(), self.outerPointSelector.currentNode())
  
  # Record points
  def onPointRecorderApplyButton(self):
    logic = PlaygroundPyLogic()
    logic.recordPoint(self.pointerFiducialsSelector.currentNode(), self.pointerTransformSelector.currentNode())
  
  # Texture Mapping  
  def onTextureMappingApplyButton(self):
    logic = PlaygroundPyLogic()
    logic.showTextureOnModel(self.inputModelSelector.currentNode(), self.inputTextureSelector.currentNode())
  
  # Fiducial registration
  def onRegistrationApplyButton(self):
    logic = PlaygroundPyLogic()
    logic.fiducialRegistration(self.registrationOutputSelector.currentNode(), self.fixedFiducialsSelector.currentNode(), self.movingFiducialsSelector.currentNode(), "Rigid", self.errorLabel)
    
  # PreviousToNextCalculator
  def onCalculatePreviousToNextClicked(self):
    logic = PlaygroundPyLogic()
    logic.calculatePreviousToNext(self.previousTransformSelector.currentNode(), self.nextTransformSelector.currentNode(), self.previousToNextTransformSelector.currentNode())

  # CastToDouble
  def onCastToDoubleClicked(self):
    logic = PlaygroundPyLogic()
    logic.castVolumeNodeToDouble(self.castToDoubleSelector.currentNode())
    
############################################################ PlaygroundPyLogic
class PlaygroundPyLogic(ScriptedLoadableModuleLogic):

  # CastToDouble
  def castVolumeNodeToDouble(self, volumeNode):    
    castFilter = vtk.vtkImageCast()
    castFilter.SetInputData(volumeNode.GetImageData())
    castFilter.SetOutputScalarTypeToDouble()
    castFilter.Update()
    volumeNode.SetAndObserveImageData(castFilter.GetOutput())
    logging.info(volumeNode.GetName() + ' was casted to double.')
    
  def calculateFiducialDistance(self, modelNode, fiducial):
    closestFiducial = slicer.util.getNode('CP')
    if not closestFiducial:
      closestFiducial = slicer.vtkMRMLMarkupsFiducialNode()  
      closestFiducial.SetName('CP')
      closestFiducial.AddFiducial(0, 0, 0)
      closestFiducial.SetNthFiducialLabel(0, 'CP')
      slicer.mrmlScene.AddNode(closestFiducial)
      closestFiducial.SetDisplayVisibility(False)
        
    line = slicer.util.getNode('Line')
    if not line:
      line = slicer.vtkMRMLModelNode()
      line.SetName('Line')
      linePolyData = vtk.vtkPolyData()
      line.SetAndObservePolyData(linePolyData)      
      modelDisplay = slicer.vtkMRMLModelDisplayNode()
      modelDisplay.SetSliceIntersectionVisibility(True)
      modelDisplay.SetColor(0,1,0)
      slicer.mrmlScene.AddNode(modelDisplay)      
      line.SetAndObserveDisplayNodeID(modelDisplay.GetID())      
      slicer.mrmlScene.AddNode(line)
      
    cellLocator = vtk.vtkCellLocator()
    cellLocator.SetDataSet(modelNode.GetPolyData())
    cellLocator.BuildLocator()
    
    if fiducial.GetNumberOfFiducials() > 0:          
      ras = [0.0, 0.0, 0.0]
      closestPoint = [0.0, 0.0, 0.0]
      
      fiducial.GetNthFiducialPosition(0, ras)
      distanceSquared = vtk.mutable(0.0) 
      subId = vtk.mutable(0) 
      cellId = vtk.mutable(0) 
      cell = vtk.vtkGenericCell()
      
      cellLocator.FindClosestPoint(ras, closestPoint, cell, cellId, subId, distanceSquared);
      distance = math.sqrt(distanceSquared)
            
      closestFiducial.SetNthFiducialPosition(0,  closestPoint[0], closestPoint[1], closestPoint[2])
      closestFiducial.SetDisplayVisibility(True)
      
      self.drawLineBetweenPoints(line, ras, closestPoint)
      
      self.set3dViewConernerAnnotation('Distance = ' + "%.2f" % distance + 'mm')
    else:
      logging.warning('No fiducials in list!')     
  
  def set3dViewConernerAnnotation(self, text):
    threeDWidget = slicer.app.layoutManager().threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.setCornerAnnotationText(text)    
  
  def drawLineBetweenPoints(self, lineModel, point1, point2):        
    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    points.InsertNextPoint(point1)
    points.InsertNextPoint(point2)

    # Create line
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0,0) 
    line.GetPointIds().SetId(1,1)
    lineCellArray = vtk.vtkCellArray()
    lineCellArray.InsertNextCell(line)
    
    # Update model data
    lineModel.GetPolyData().SetPoints(points)
    lineModel.GetPolyData().SetLines(lineCellArray)
    
  def transformPolyData(self, modelNode, transformNode):
    transformedModel = slicer.util.getNode('Transformed Model')
    if not transformedModel:
      transformedModel = slicer.vtkMRMLModelNode()
      transformedModel.SetName('Transformed Model')
      transformedModel.SetAndObservePolyData(modelNode.GetPolyData())     
      modelDisplay = slicer.vtkMRMLModelDisplayNode()
      modelDisplay.SetSliceIntersectionVisibility(True)
      modelDisplay.SetColor(0,1,0)
      slicer.mrmlScene.AddNode(modelDisplay)      
      transformedModel.SetAndObserveDisplayNodeID(modelDisplay.GetID())      
      slicer.mrmlScene.AddNode(transformedModel)
      transformedModel.SetDisplayVisibility(False)  
      
    t = vtk.vtkGeneralTransform()

    transformNode.GetTransformToWorld(t)
    
    transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()
    transformPolyDataFilter.SetTransform(t)
    transformPolyDataFilter.SetInputData(modelNode.GetPolyData())
    transformPolyDataFilter.Update()

    transformedModel.SetAndObservePolyData(transformPolyDataFilter.GetOutput()) 
      
  # Calculates the transform from previous to next (PreviousToNext).
  def calculatePreviousToNext(self, previousTransformNode, nextTransformNode, previousToNextTransformNode):
      start = time.time()
      
      previousMatrix = vtk.vtkMatrix4x4()
      nextMatrix = vtk.vtkMatrix4x4()
      previousToNextMatrix = vtk.vtkMatrix4x4()
      
      previousTransformNode.GetMatrixTransformToWorld(previousMatrix)
      nextTransformNode.GetMatrixTransformToWorld(nextMatrix)
      
      previousMatrix.Invert()
      
      vtk.vtkMatrix4x4().Multiply4x4(nextMatrix, previousMatrix, previousToNextMatrix)
      previousToNextTransformNode.SetMatrixTransformToParent(previousToNextMatrix)
      
      end = time.time()
      logging.info('Calculated PreviousToNext in ' + "%.4f" % (end - start) + 's.')
      
  # Show a texture on a model
  def showTextureOnModel(self, modelNode, textureImageNode): 
    modelDisplayNode=modelNode.GetDisplayNode() # Get model display node
    
    modelDisplayNode.SetBackfaceCulling(0) # In computer graphics, back-face culling determines whether a polygon of a graphical object is visible. 
    textureImageFlipVert=vtk.vtkImageFlip() # vtkImageFlip will reflect the data along the filtered axis. 
    textureImageFlipVert.SetFilteredAxis(1) # Specify which axis will be flipped. This must be an integer between 0 (for x) and 2 (for z). Initial value is 0.
    textureImageFlipVert.SetInputConnection(textureImageNode.GetImageDataConnection()) # Set the connection for the given input port index. Each input port of a filter has a specific purpose. A port may have zero or more connections and the required number is specified by each filter. Setting the connection with this method removes all other connections from the port. 
    
    modelDisplayNode.SetTextureImageDataConnection(textureImageFlipVert.GetOutputPort()) # Set and observe the texture image data port.
    
  def recordPoint(self, fiducialList, stylysTipTransform):    
    point = [0.0,0.0,0.0]
    
    m = vtk.vtkMatrix4x4()
    stylysTipTransform.GetMatrixTransformToWorld(m)
    point[0] = m.GetElement(0, 3)
    point[1] = m.GetElement(1, 3)
    point[2] = m.GetElement(2, 3)
    
    fiducialList.AddFiducial(point[0], point[1], point[2])
  
  def createMovingLRSToFixedLRS(self, movingLRS = None):
    if movingLRS.GetNumberOfFiducials() < 3:
      logging.warning('Moving LRS fiducials list needs to contain at least three fiducials!')
      return False
      
    fixedLRS = slicer.util.getNode('FixedLRS')    
    if not fixedLRS:
      # Create FixedLRS markups node
      fixedLRS = slicer.vtkMRMLMarkupsFiducialNode()
      fixedLRS.SetName('FixedLRS')
      fixedLRS.AddFiducial(-100.0, 0.0, 0.0)
      fixedLRS.SetNthFiducialLabel(0, 'FixedL')
      fixedLRS.AddFiducial(100.0, 0.0, 0.0)
      fixedLRS.SetNthFiducialLabel(1, 'FixedR')
      fixedLRS.AddFiducial(0.0, 0.0, 100.0)
      fixedLRS.SetNthFiducialLabel(2, 'FixedS')
      slicer.mrmlScene.AddNode(fixedLRS)
      fixedLRS.SetDisplayVisibility(False)
   
    movingLRSToFixedLRS = slicer.util.getNode('MovingLRSToFixedLRS')    
    if not movingLRSToFixedLRS:
      # Create MovingLRSToFixedLRS transform node
      movingLRSToFixedLRS = slicer.vtkMRMLLinearTransformNode()
      movingLRSToFixedLRS.SetName('MovingLRSToFixedLRS')
      slicer.mrmlScene.AddNode(movingLRSToFixedLRS)
    
    self.fiducialRegistration(movingLRSToFixedLRS, fixedLRS, movingLRS, "Rigid")
    
    return True
  
  def setFirstPersonView(self):
    lm=slicer.app.layoutManager() 
    view=lm.threeDWidget(0).threeDView() 
    view.resetFocalPoint()
    view.lookFromViewAxis(ctk.ctkAxesWidget.Posterior) 
  
  # Performs a fiducial registration using the Slicer module Fiducial Registration.
  def fiducialRegistration(self, saveTransform, fixedLandmarks, movingLandmarks, transformType, errorLabel = None):
    logging.info("Fiducial registration starts")
    parameters = {}
    rms = 0
    parameters["fixedLandmarks"] = fixedLandmarks.GetID()
    parameters["movingLandmarks"] = movingLandmarks.GetID()
    parameters["saveTransform"] = saveTransform.GetID()
    parameters["rms"] = rms 
    parameters["transformType"] = transformType
    fidReg = slicer.modules.fiducialregistration
    slicer.cli.run(fidReg, None, parameters)
    logging.info("Fiducial registration finished")
    
    if errorLabel:
      errorLabel.setText(str(rms))
    
    return True
  
  def imageProcessingConnector(self, inputVolumeNode, paramsVTK, runtimeLabel=None):     
    logging.info('imageProcessingConnector started')
    runtime = slicer.modules.playgroundcpp.logic().ImageProcessingConnector(inputVolumeNode, self.BSPVolumeNode, paramsVTK, 'Foroughi2007')
    runtime = str(round(runtime, 3)) 
    message = runtime + ' s.'
    if runtimeLabel:
      runtimeLabel.setText(message)
    logging.info('imageProcessingConnector completed (' + message + ')') 
    return True
    
  def modelTipToToolCreatorByTransforms(self, originTransformNode, fromTransformNode, toTransformNode, outputTransformNode):
    logging.info('INFO | modelTipToToolCreatorByTransforms')
    originPoint = [0.0,0.0,0.0]
    fromPoint = [0.0,0.0,0.0]
    toPoint = [0.0,0.0,0.0]
    
    m = vtk.vtkMatrix4x4()
    originTransformNode.GetMatrixTransformToWorld(m)
    originPoint[0] = m.GetElement(0, 3)
    originPoint[1] = m.GetElement(1, 3)
    originPoint[2] = m.GetElement(2, 3)
    m.Identity()
    fromTransformNode.GetMatrixTransformToWorld(m)
    fromPoint[0] = m.GetElement(0, 3)
    fromPoint[1] = m.GetElement(1, 3)
    fromPoint[2] = m.GetElement(2, 3)
    m.Identity()
    toTransformNode.GetMatrixTransformToWorld(m)
    toPoint[0] = m.GetElement(0, 3)
    toPoint[1] = m.GetElement(1, 3)
    toPoint[2] = m.GetElement(2, 3)    
    
    m = vtk.vtkMatrix4x4()
    m = self.getRotMatAligningVecAtoVecB(originPoint, fromPoint, toPoint)
    outputTransformNode.SetMatrixTransformToParent(m)
 
    return True

  def modelTipToToolCreatorByFiducials(self, originFiducial, fromFiducial, toFiducial, outputTransformNode):
    logging.info('INFO | modelTipToToolCreatorByFiducials')
    originPoint = [0.0,0.0,0.0]
    fromPoint = [0.0,0.0,0.0]
    toPoint = [0.0,0.0,0.0]
    
    originFiducial.GetNthFiducialWorldCoordinates(0, originPoint)        
    fromFiducial.GetNthFiducialWorldCoordinates(0, fromPoint)        
    toFiducial.GetNthFiducialWorldCoordinates(0, toPoint)
    
    m = vtk.vtkMatrix4x4()
    m = self.getRotMatAligningVecAtoVecB(originPoint, fromPoint, toPoint)
    outputTransformNode.SetMatrixTransformToParent(m)
    
    return True
    
  # See: http://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
  def getRotMatAligningVecAtoVecB(self, originPoint, fromPoint, toPoint):
    logging.info('INFO | originPoint = '  + str(originPoint) +  '\nfromPoint = ' + str(fromPoint) + '\ntoPoint = ' + str(toPoint))
    import numpy as np       
    
    # Calculate unit vector a and unit vector b
    a = np.subtract(fromPoint[0:3], originPoint[0:3])
    aMagnitude = np.linalg.norm(a)
    a[0] = a[0] / aMagnitude
    a[1] = a[1] / aMagnitude
    a[2] = a[2] / aMagnitude
    b = np.subtract(toPoint[0:3], originPoint[0:3])
    bMagnitude = np.linalg.norm(b)
    b[0] = b[0] / bMagnitude 
    b[1] = b[1] / bMagnitude
    b[2] = b[2] / bMagnitude
    logging.info('INFO | a ='  + str(a) + '\nb =' + str(b))
 
    if a is not b:    
      # Cross a and b
      v = np.cross(a, b)
      logging.info('INFO | v = '  + str(v))
      
      # Define the skew-symmetric cross-product matrix of v
      v_1 = v[0]
      v_2 = v[1]
      v_3 = v[2]
      V_x = np.matrix([[0, -v_3, v_2], 
                       [v_3, 0, -v_1], 
                       [-v_2, v_1, 0]])
      logging.info('INFO | V_x =\n'  + str(V_x))
    
      # Calculate R
      I = np.identity(3)
      R = I + V_x + V_x**2 * (1 - np.dot(a, b)) / (np.linalg.norm(np.cross(a, b))**2)
    else:
      R = np.identity(3)
      
    logging.info('INFO | R =\n'  + str(R))
    
    # Create VTK matrix
    m = vtk.vtkMatrix4x4()
    self.numpy3x3MatrixToVTK4x4Matrix(R, m)
    
    return m
    
  def numpy3x3MatrixToVTK4x4Matrix(self, inNumpyMatrix, outVTKMatrix):
    outVTKMatrix.SetElement(0, 0, inNumpyMatrix[0, 0])
    outVTKMatrix.SetElement(0, 1, inNumpyMatrix[0, 1])
    outVTKMatrix.SetElement(0, 2, inNumpyMatrix[0, 2])
    
    outVTKMatrix.SetElement(1, 0, inNumpyMatrix[1, 0])
    outVTKMatrix.SetElement(1, 1, inNumpyMatrix[1, 1])
    outVTKMatrix.SetElement(1, 2, inNumpyMatrix[1, 2])
    
    outVTKMatrix.SetElement(2, 0, inNumpyMatrix[2, 0])
    outVTKMatrix.SetElement(2, 1, inNumpyMatrix[2, 1])
    outVTKMatrix.SetElement(2, 2, inNumpyMatrix[2, 2])
    
    return True
