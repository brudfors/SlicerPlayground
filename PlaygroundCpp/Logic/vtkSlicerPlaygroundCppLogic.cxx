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

// PlaygroundCpp Logic includes
#include "vtkSlicerPlaygroundCppLogic.h"

// MRML includes
#include <vtkMRMLScene.h>
#include <vtkMRMLScalarVolumeNode.h>
#include <vtkMRMLSelectionNode.h>

// VTK includes
#include <vtkIntArray.h>
#include <vtkNew.h>
#include <vtkObjectFactory.h>
#include <vtkImageData.h>
#include <vtkDoubleArray.h>
#include <vtkTimerLog.h>

// STD includes
#include <cassert>

// Slicer includes
#include <vtkSlicerVolumesLogic.h>

// Other includes
#include "mkl.h"
#ifdef NDEBUG
#include <omp.h>
#endif

//----------------------------------------------------------------------------
vtkStandardNewMacro(vtkSlicerPlaygroundCppLogic);

//----------------------------------------------------------------------------
vtkSlicerPlaygroundCppLogic::vtkSlicerPlaygroundCppLogic()
{
}

//----------------------------------------------------------------------------
vtkSlicerPlaygroundCppLogic::~vtkSlicerPlaygroundCppLogic()
{
}

//----------------------------------------------------------------------------
void vtkSlicerPlaygroundCppLogic::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
}

//---------------------------------------------------------------------------
void vtkSlicerPlaygroundCppLogic::SetMRMLSceneInternal(vtkMRMLScene * newScene)
{
  vtkNew<vtkIntArray> events;
  events->InsertNextValue(vtkMRMLScene::NodeAddedEvent);
  events->InsertNextValue(vtkMRMLScene::NodeRemovedEvent);
  events->InsertNextValue(vtkMRMLScene::EndBatchProcessEvent);
  this->SetAndObserveMRMLSceneEventsInternal(newScene, events.GetPointer());
}

//-----------------------------------------------------------------------------
void vtkSlicerPlaygroundCppLogic::RegisterNodes()
{
  assert(this->GetMRMLScene() != 0);
}

//---------------------------------------------------------------------------
void vtkSlicerPlaygroundCppLogic::UpdateFromMRMLScene()
{
  assert(this->GetMRMLScene() != 0);
}

//---------------------------------------------------------------------------
void vtkSlicerPlaygroundCppLogic
::OnMRMLSceneNodeAdded(vtkMRMLNode* vtkNotUsed(node))
{
}

//---------------------------------------------------------------------------
void vtkSlicerPlaygroundCppLogic
::OnMRMLSceneNodeRemoved(vtkMRMLNode* vtkNotUsed(node))
{
}

//---------------------------------------------------------------------------
// An image processing connector method, which takes both an input, and a output volume node from 3D Slicer,
// an array of parameters, and the name of the algorithm to execute.
float vtkSlicerPlaygroundCppLogic
::ImageProcessingConnector(vtkMRMLScalarVolumeNode* inputVolumeNode, vtkMRMLScalarVolumeNode* outputVolumeNode, 
													 vtkDoubleArray* params, std::string algorithmName)
{
	int* dims = inputVolumeNode->GetImageData()->GetDimensions();
	int nx = dims[0];
	int ny = dims[1];
	int nz = dims[2];

	float runtime = 0.0;
	if (algorithmName == "Foroughi2007")
	{
		// Define necessary parameters
		int blurredVSBLoG = params->GetValue(0);
		double boneThreshold = params->GetValue(1);
		double shadowSigma = params->GetValue(2);
		int shadowVSIntensity = params->GetValue(3);
		double smoothingSigma = params->GetValue(4);
		int transducerMargin = params->GetValue(5);		
	
		vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
		timer->StartTimer();

		// Extract BSP from input volume (through pointer) and put result into the output volume's buffer
		//this->Foroughi2007(static_cast<double*>(inputVolumeNode->GetImageData()->GetScalarPointer(0,0,0)), 
		//									 static_cast<double*>(outputVolumeNode->GetImageData()->GetScalarPointer(0,0,0)), 
		//									 smoothingSigma, transducerMargin, shadowSigma, 
		// 								   boneThreshold, blurredVSBLoG, shadowVSIntensity,
		//									 nx, ny, nz);
    
		timer->StopTimer();
		runtime = timer->GetElapsedTime();
	}
	else
	{
		std::cout << "No algorithm defined!" << std::endl;
	}

	return runtime;
}