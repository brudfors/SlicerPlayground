/*==============================================================================

  Program: 3D Slicer

  Portions (c) Copyright Brigham and Women's Hospital (BWH) All Rights Reserved.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

==============================================================================*/

// .NAME vtkSlicerPlaygroundCppLogic - slicer logic class for volumes manipulation
// .SECTION Description
// This class manages the logic associated with reading, saving,
// and changing propertied of the volumes


#ifndef __vtkSlicerPlaygroundCppLogic_h
#define __vtkSlicerPlaygroundCppLogic_h

// Slicer includes
#include "vtkSlicerModuleLogic.h"

// MRML includes

// STD includes
#include <cstdlib>

#include "vtkSlicerPlaygroundCppModuleLogicExport.h"

class vtkMRMLScalarVolumeNode;
class vtkDoubleArray;

/// \ingroup Slicer_QtModules_ExtensionTemplate
class VTK_SLICER_PLAYGROUNDCPP_MODULE_LOGIC_EXPORT vtkSlicerPlaygroundCppLogic :
  public vtkSlicerModuleLogic
{
public:

  static vtkSlicerPlaygroundCppLogic *New();
  vtkTypeMacro(vtkSlicerPlaygroundCppLogic, vtkSlicerModuleLogic);
  void PrintSelf(ostream& os, vtkIndent indent);

  /*! Image processing connector method. */
	float ImageProcessingConnector(vtkMRMLScalarVolumeNode* inputVolumeNode, vtkMRMLScalarVolumeNode* outputVolumeNode, 
																 vtkDoubleArray* params, std::string algorithmName);
                                 
protected:
  vtkSlicerPlaygroundCppLogic();
  virtual ~vtkSlicerPlaygroundCppLogic();

  virtual void SetMRMLSceneInternal(vtkMRMLScene* newScene);
  /// Register MRML Node classes to Scene. Gets called automatically when the MRMLScene is attached to this logic class.
  virtual void RegisterNodes();
  virtual void UpdateFromMRMLScene();
  virtual void OnMRMLSceneNodeAdded(vtkMRMLNode* node);
  virtual void OnMRMLSceneNodeRemoved(vtkMRMLNode* node);
private:

  vtkSlicerPlaygroundCppLogic(const vtkSlicerPlaygroundCppLogic&); // Not implemented
  void operator=(const vtkSlicerPlaygroundCppLogic&); // Not implemented
};

#endif
