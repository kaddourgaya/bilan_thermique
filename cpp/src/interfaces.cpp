#include "interfaces.hpp"

double flux_eau_air(double NetRad,
                    double phi_s_aw,
                    double phi_l_aw) {
    return NetRad - phi_s_aw - phi_l_aw;
}

double flux_glace_air(double NetRad,
                      double phi_s_ai,
                      double phi_l_ai) {
    return NetRad - phi_s_ai - phi_l_ai;
}
