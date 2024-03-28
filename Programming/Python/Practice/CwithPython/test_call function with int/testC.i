%module testC

%{
#define SWIG_FILE_WITH_INIT
#include "testH.h"
%}

%include "testH.h"

