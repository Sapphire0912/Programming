%module Cconvolution

%{
#define SWIG_FILE_WITH_INIT
#include "convolutionH.h"
%}

%include "numpy.i"
%init %{
import_array();
%}

%apply (int INPLACE_ARRAY2[ANY][ANY]) {(int src[600][800])};
void CMultiThreshold(int src[600][800]);

%include "convolutionH.h"

