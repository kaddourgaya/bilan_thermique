#include <iostream>
#include <fstream>
#include <string>

#include "csv_row.hpp"
#include "glace.hpp"
#include "chaleur_sensible.hpp"
#include "chaleur_latente.hpp"
#include "interfaces.hpp"
#include "bilan.hpp"

int main() {
    std::cout << "Lecture du fichier data/exemple.csv...\n";

    std::ifstream file("data/exemple.csv");
    if (!file.is_open()) {
        std::cerr << "Impossible d'ouvrir data/exemple.csv\n";
        return 1;
    }

    std::string line;
    // sauter l'en-tête
    std::getline(file, line);
    if (!line.empty() && line.back() == '\r')
        line.pop_back();

    while (std::getline(file, line)) {
        if (!line.empty() && line.back() == '\r')
            line.pop_back();
        CsvRow row = parse_csv_line(line);

        double Ta   = row.Ta;
        double va   = row.va;
        double HR   = row.HR;
        double Fi   = row.Fi;
        double Tw   = row.Tw;
        double ha   = row.ha;
        double hi_mesure = row.hi;
        double AFDD = row.AFDD;
        double ATDD = row.ATDD;
        double NetRad = row.NetRad;
        int    use_hi_mesure = row.use_hi_mesure;

        double alpha_h = 0.6;
        double A       = 0.5;

        double hi_croissance = epaisseur_glace_croissance(alpha_h, AFDD);
        double hi_fonte      = epaisseur_glace_fonte(hi_croissance, A, ATDD);

        double hi_calcule = choisir_hi(Fi, Ta, hi_mesure, hi_croissance, hi_fonte);
        double hi = (use_hi_mesure == 1) ? hi_mesure : hi_calcule;

        double ka = 0.024;
        double ki = 2.1;
        double Tis = temperature_surface_glace(ka, ki, hi, ha, Ta);

        double Ts_aw = Tw;
        double Ts_ai = Tis;

        double phi_s_aw = chaleur_sensible(Ts_aw, Ta, va);
        double phi_s_ai = chaleur_sensible(Ts_ai, Ta, va);

        double phi_l_aw = chaleur_latente(Ts_aw, Ta, va, HR, "eau");
        double phi_l_ai = chaleur_latente(Ts_ai, Ta, va, HR, "glace");

        double phi_aw = flux_eau_air(NetRad, phi_s_aw, phi_l_aw);
        double phi_ai = flux_glace_air(NetRad, phi_s_ai, phi_l_ai);

        double phi_n  = flux_net(phi_aw, phi_ai, Fi);

        std::cout << "---- Nouvelle ligne ----\n";
        std::cout << "hi utilisé : " << hi << "\n";
        std::cout << "Flux interface eau-air (φaw) : " << phi_aw << "\n";
        std::cout << "Flux interface glace-air (φai) : " << phi_ai << "\n";
        std::cout << "Bilan thermique net (φn) : " << phi_n << "\n";
    }

    return 0;
}
