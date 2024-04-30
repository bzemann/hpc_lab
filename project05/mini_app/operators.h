//******************************************
// operators.h
// based on min-app code written by Oliver Fuhrer, MeteoSwiss
// modified by Ben Cumming, CSCS
// *****************************************

// Description: Contains simple operators which can be used on 2/3d-meshes

#ifndef OPERATORS_H
#define OPERATORS_H

#include "data.h"

namespace operators {

void diffusion(data::Field const& s_old, data::Field const& s_new,
               data::Field& f);

}

#endif /* OPERATORS_H */
