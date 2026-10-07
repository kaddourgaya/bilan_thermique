#include "bilan.hpp"

double flux_net(double phi_aw, double phi_ai, double Fi) {
    if (Fi <= 0.0) return phi_aw;
    if (Fi >= 1.0) return phi_ai;
    return phi_aw * (1.0 - Fi) + phi_ai * Fi;
}
