%module CArray

%{
#define SWIG_FILE_WITH_INIT
#include "CallArray.h"
%}

%include "numpy.i"
%include "carrays.i"
%array_class(int, intArray);

%init %{
import_array();
%}

%include "CallArray.h"
