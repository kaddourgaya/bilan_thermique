#include "chaleur_latente.hpp"
#include <cmath>
#include <stdexcept>
#include <cstring>

double es_eau_goff_gratch_murray(double Tc) {
    double Tk = Tc + 273.16;

    return 7.95357242e10 *
        std::exp(
            -18.1972839 * (373.16 / Tk)
            + 5.02808 * std::log(373.16 / Tk)
            - 20242.1852 * std::exp(-26.1205253 * Tk / 373.16)
            + 58.0691913 * std::exp(-8.039282 * (373.16 / Tk))
        );
}

double es_glace_goff_gratch_murray(double Tc) {
    double Tk = Tc + 273.16;

    return 5.75185606e10 *
        (
            -20.947013 * (373.16 / Tk)
            - 3.56654   * std::log(373.16 / Tk)
            - 2.01889049 * (273.16 / Tk)
        );
}

double chaleur_latente(double Ts, double Ta,
                       double va, double HR,
                       const char* surface) {
    double Kn = 8.0 + 0.35 * (Ts - Ta);

    double es   = 0.0;
    double ea_sat = 0.0;

    if (std::strcmp(surface, "eau") == 0) {
        es      = es_eau_goff_gratch_murray(Ts);
        ea_sat  = es_eau_goff_gratch_murray(Ta);
    } else if (std::strcmp(surface, "glace") == 0) {
        es      = es_glace_goff_gratch_murray(Ts);
        ea_sat  = es_glace_goff_gratch_murray(Ta);
    } else {
        throw std::runtime_error("surface doit être 'eau' ou 'glace'");
    }

    double ea = ea_sat * HR / 100.0;

    double phi_l =
        (4.1855 / 8.64) *
        (1.56 * Kn + 6.08 * va) *
        (es - ea);

    return phi_l;
}
