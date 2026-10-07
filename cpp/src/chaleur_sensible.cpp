#include "chaleur_sensible.hpp"

double chaleur_sensible(double Ts, double Ta, double va) {
    double kn = 8.0 + 0.35 * (Ts - Ta);
    return 0.4844 * (kn + 3.9 * va) * (Ts - Ta);
}
