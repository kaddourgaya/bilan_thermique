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
    print("Lecture du fichier exemple.csv et calcul des bilans thermiques...")

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

            # 6. Rayonnements en W/m²
            phi_sr = rayonnement_ondes_courtes(sr_in, sr_out)
            phi_lr_aw = rayonnement_ondes_longues_ding(Ts_aw, Ta, HR, C, es_eau_goff_gratch_murray, ek)
            phi_lr_ai = rayonnement_ondes_longues_ding(Ts_ai, Ta, HR, C, es_glace_goff_gratch_murray, ek)

            NetRad_aw_W = phi_sr + phi_lr_aw
            NetRad_ai_W = phi_sr + phi_lr_ai

            # Conversion de W/m² vers MJ/m²/jour (Facteur 0.0864) pour harmonisation CEQUEAU
            NetRad_aw = NetRad_aw_W * 0.0864
            NetRad_ai = NetRad_ai_W * 0.0864

            # 7. Chaleur sensible φs (déjà renvoyée en MJ/jour ou MJ/m²/jour par nos fonctions)
            phi_s_aw = chaleur_sensible(Ts_aw, Ta, va, surface="eau")
            phi_s_ai = chaleur_sensible(Ts_ai, Ta, va, surface="glace")

            # 8. Chaleur latente φl (déjà convertie en MJ/m²/jour dans chaleur_latente.py)
            phi_l_aw = chaleur_latente(Ts_aw, Ta, va, HR, surface="eau")
            phi_l_ai = chaleur_latente(Ts_ai, Ta, va, HR, surface="glace")

            # 9. Flux aux interfaces φaw / φai (en MJ/m²/jour)
            phi_aw = flux_eau_air(NetRad_aw, phi_s_aw, phi_l_aw)
            phi_ai = flux_glace_air(NetRad_ai, phi_s_ai, phi_l_ai)

            # 10. Bilan thermique net φn (en MJ/m²/jour)
            phi_n = flux_net(phi_aw, phi_ai, Fi)

            # 11. Affichage formaté
            print("--------------------------------------------------")
            print(f"Utiliser hi (mesuré : 1, calculé : 0) : {use_hi_mesure:.0f}")
            print(f"Fi : {Fi} | Ta : {Ta}°C | hi : {hi:.3f}m")
            print(f"Flux interface eau-air (φaw) : {phi_aw:.2f} MJ/m²/jour")
            print(f"Flux interface glace-air (φai) : {phi_ai:.2f} MJ/m²/jour")
            print(f"Bilan thermique net (φn)       : {phi_n:.2f} MJ/m²/jour")

if __name__ == "__main__":
    main()