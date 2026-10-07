#pragma once

double epaisseur_glace_croissance(double alpha_h, double AFDD);
double epaisseur_glace_fonte(double eta_max, double A, double ATDD);
double choisir_hi(double Fi, double Ta,
                  double hi_mesure,
                  double hi_croissance,
                  double hi_fonte);
double temperature_surface_glace(double ka, double ki,
                                 double hi, double ha,
                                 double Ta);
