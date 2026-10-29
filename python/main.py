import csv
import numpy as np

from src.chaleur_sensible import chaleur_sensible
from src.chaleur_latente import (
    chaleur_latente,
    es_eau_goff_gratch_murray,
    es_glace_goff_gratch_murray
)
from src.radiation import rayonnement_ondes_courtes, rayonnement_ondes_longues_ding
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

            # 1. Données d'entrée
            Ta = float(row["Ta"])
            va = float(row["va"])
            HR = float(row["HR"])
            Fi = float(row["Fi"])
            Tw = float(row["Tw"])
            ha = float(row["ha"])
            hi_mesure = float(row["hi"])
            AFDD = float(row["AFDD"])
            ATDD = float(row["ATDD"])
            
            sr_in = float(row["sr_in"])
            sr_out = float(row["sr_out"])
            C = float(row["C"])
            ek = float(row.get("ek", 1.0))
            
            use_hi_mesure = int(row["use_hi_mesure"])

            # 2. Épaisseur théorique de la glace
            alpha_h = 0.6
            A = 0.5

            hi_croissance = epaisseur_glace_croissance(alpha_h, AFDD)
            hi_fonte = epaisseur_glace_fonte(hi_croissance, A, ATDD)

            # 3. Choix du hi final
            if use_hi_mesure == 1:
                hi = hi_mesure
            else:
                hi = choisir_hi(Fi, Ta, hi_mesure, hi_croissance, hi_fonte)

            # 4. Température de surface de la glace
            ka = 0.024
            ki = 2.1
            Tis = temperature_surface_glace(ka, ki, hi, ha, Ta)

            # 5. Températures de surface
            Ts_aw = Tw
            Ts_ai = Tis

            # 6. Rayonnement net
            phi_sr = rayonnement_ondes_courtes(sr_in, sr_out)

            phi_lr_aw = rayonnement_ondes_longues_ding(Ts_aw, Ta, HR, C, es_eau_goff_gratch_murray, ek)
            phi_lr_ai = rayonnement_ondes_longues_ding(Ts_ai, Ta, HR, C, es_glace_goff_gratch_murray, ek)

            NetRad_aw = phi_sr + phi_lr_aw
            NetRad_ai = phi_sr + phi_lr_ai

            # 7. Chaleur sensible φs
            phi_s_aw = chaleur_sensible(Ts_aw, Ta, va, surface="eau")
            phi_s_ai = chaleur_sensible(Ts_ai, Ta, va, surface="glace")

            # 8. Chaleur latente φl
            phi_l_aw = chaleur_latente(Ts_aw, Ta, va, HR, surface="eau")
            phi_l_ai = chaleur_latente(Ts_ai, Ta, va, HR, surface="glace")

            # 9. Flux aux interfaces φaw / φai
            phi_aw = flux_eau_air(NetRad_aw, phi_s_aw, phi_l_aw)
            phi_ai = flux_glace_air(NetRad_ai, phi_s_ai, phi_l_ai)

            # 10. Bilan thermique net φn
            phi_n = flux_net(phi_aw, phi_ai, Fi)

            # 11. Affichage
            print("---- Nouvelle ligne ----")
            print("Le Fi est de : ", Fi)
            print("hi utilisé :", hi)
            print("Flux interface eau-air (φaw) :", phi_aw)
            print("Flux interface glace-air (φai) :", phi_ai)
            print("Bilan thermique net (φn) :", phi_n)

if __name__ == "__main__":
    main()