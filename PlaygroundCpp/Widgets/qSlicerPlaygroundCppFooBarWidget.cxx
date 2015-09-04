/*==============================================================================

  Program: 3D Slicer

  Copyright (c) Kitware Inc.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

// FooBar Widgets includes
#include "qSlicerPlaygroundCppFooBarWidget.h"
#include "ui_qSlicerPlaygroundCppFooBarWidget.h"

//-----------------------------------------------------------------------------
/// \ingroup Slicer_QtModules_PlaygroundCpp
class qSlicerPlaygroundCppFooBarWidgetPrivate
  : public Ui_qSlicerPlaygroundCppFooBarWidget
{
  Q_DECLARE_PUBLIC(qSlicerPlaygroundCppFooBarWidget);
protected:
  qSlicerPlaygroundCppFooBarWidget* const q_ptr;

public:
  qSlicerPlaygroundCppFooBarWidgetPrivate(
    qSlicerPlaygroundCppFooBarWidget& object);
  virtual void setupUi(qSlicerPlaygroundCppFooBarWidget*);
};

// --------------------------------------------------------------------------
qSlicerPlaygroundCppFooBarWidgetPrivate
::qSlicerPlaygroundCppFooBarWidgetPrivate(
  qSlicerPlaygroundCppFooBarWidget& object)
  : q_ptr(&object)
{
}

// --------------------------------------------------------------------------
void qSlicerPlaygroundCppFooBarWidgetPrivate
::setupUi(qSlicerPlaygroundCppFooBarWidget* widget)
{
  this->Ui_qSlicerPlaygroundCppFooBarWidget::setupUi(widget);
}

//-----------------------------------------------------------------------------
// qSlicerPlaygroundCppFooBarWidget methods

//-----------------------------------------------------------------------------
qSlicerPlaygroundCppFooBarWidget
::qSlicerPlaygroundCppFooBarWidget(QWidget* parentWidget)
  : Superclass( parentWidget )
  , d_ptr( new qSlicerPlaygroundCppFooBarWidgetPrivate(*this) )
{
  Q_D(qSlicerPlaygroundCppFooBarWidget);
  d->setupUi(this);
}

//-----------------------------------------------------------------------------
qSlicerPlaygroundCppFooBarWidget
::~qSlicerPlaygroundCppFooBarWidget()
{
}
