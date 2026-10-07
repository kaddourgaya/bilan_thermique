#pragma once

double es_eau_goff_gratch_murray(double Tc);
double es_glace_goff_gratch_murray(double Tc);

double chaleur_latente(double Ts, double Ta,
                       double va, double HR,
                       const char* surface);
