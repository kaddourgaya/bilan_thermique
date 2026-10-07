#include "glace.hpp"
#include <algorithm>
#include <cmath>

double epaisseur_glace_croissance(double alpha_h, double AFDD) {
    return alpha_h * std::sqrt(AFDD);
}

double epaisseur_glace_fonte(double eta_max, double A, double ATDD) {
    return std::max(0.0, eta_max - A * ATDD);
}

double choisir_hi(double Fi, double Ta,
                  double hi_mesure,
                  double hi_croissance,
                  double hi_fonte) {
    if (Fi <= 0.0) return 0.0;
    if (Ta < 0.0)  return hi_croissance;
    return hi_fonte;
}

double temperature_surface_glace(double ka, double ki,
                                 double hi, double ha,
                                 double Ta) {
    return (ka * hi) / (ka * hi + ki * ha) * Ta;
}
