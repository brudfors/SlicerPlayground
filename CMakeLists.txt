cmake_minimum_required(VERSION 2.8.9)

project(Playground)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://www.example.com/Slicer/Extensions/Playground")
set(EXTENSION_CATEGORY "Brudfors")
set(EXTENSION_CONTRIBUTORS "Mikael Brudfors (UC3M)")
set(EXTENSION_DESCRIPTION "This is an example of a simple extension")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/Playground.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/Playground/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(PlaygroundPy)
add_subdirectory(PlaygroundCpp)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
