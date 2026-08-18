# main.py

import csv
import numpy as np

from src.chaleur_sensible import chaleur_sensible
from src.chaleur_latente import chaleur_latente
from src.glace import (
    epaisseur_glace_croissance,
    epaisseur_glace_fonte,
    choisir_hi,
    temperature_surface_glace
)
from src.interfaces import flux_eau_air, flux_glace_air
from src.bilan import flux_net

def main():
    print("Lecture du fichier exemple.csv...")

    with open("data/exemple.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:

            # ============================
            # 1. INPUTS
            # ============================
            Ta = float(row["Ta"])
            va = float(row["va"])
            HR = float(row["HR"])
            Fi = float(row["Fi"])
            Tw = float(row["Tw"])
            ha = float(row["ha"])
            hi_mesure = float(row["hi"])
            AFDD = float(row["AFDD"])
            ATDD = float(row["ATDD"])
            NetRad = float(row["NetRad"])
            use_hi_mesure = int(row["use_hi_mesure"])  # <-- NOUVEAU

            # ============================
            # 2. ÉPAISSEUR GLACE THÉORIQUE
            # ============================
            alpha_h = 0.6
            A = 0.5

            hi_croissance = epaisseur_glace_croissance(alpha_h, AFDD)
            hi_fonte = epaisseur_glace_fonte(hi_croissance, A, ATDD)

            # ============================
            # 3. CHOIX DU hi FINAL
            # ============================
            # MODE 1 : hi calculé (par défaut)
            hi_calcule = choisir_hi(Fi, Ta, hi_mesure, hi_croissance, hi_fonte)

            # MODE 2 : hi mesuré (si use_hi_mesure = 1)
            if use_hi_mesure == 1:
                hi = hi_mesure
            else:
                hi = hi_calcule

            # ============================
            # 4. TEMPÉRATURE SURFACE GLACE
            # ============================
            ka = 0.024
            ki = 2.1
            Tis = temperature_surface_glace(ka, ki, hi, ha, Ta)

            # ============================
            # 5. TEMPÉRATURES DE SURFACE Ts
            # ============================
            if Fi <= 0:
                Ts_aw = Tw
                Ts_ai = Tis
            elif Fi >= 1:
                Ts_aw = Tw
                Ts_ai = Tis
            else:
                Ts_aw = Tw
                Ts_ai = Tis

            # ============================
            # 6. CHALEUR SENSIBLE φs
            # ============================
            phi_s_aw = chaleur_sensible(Ts_aw, Ta, va)
            phi_s_ai = chaleur_sensible(Ts_ai, Ta, va)

            # ============================
            # 7. CHALEUR LATENTE φl
            # ============================
            phi_l_aw = chaleur_latente(Ts_aw, Ta, va, HR, surface="eau")
            phi_l_ai = chaleur_latente(Ts_ai, Ta, va, HR, surface="glace")

            # ============================
            # 8. FLUX INTERFACES φaw / φai
            # ============================
            phi_aw = flux_eau_air(NetRad, phi_s_aw, phi_l_aw)
            phi_ai = flux_glace_air(NetRad, phi_s_ai, phi_l_ai)

            # ============================
            # 9. BILAN THERMIQUE NET φn
            # ============================
            phi_n = flux_net(phi_aw, phi_ai, Fi)

            # ============================
            # 10. AFFICHAGE
            # ============================
            print("---- Nouvelle ligne ----")
            print("hi utilisé :", hi)
            print("Flux interface eau-air (φaw) :", phi_aw)
            print("Flux interface glace-air (φai) :", phi_ai)
            print("Bilan thermique net (φn) :", phi_n)

if __name__ == "__main__":
    main()
