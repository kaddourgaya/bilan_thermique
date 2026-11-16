import csv
import numpy as np

from src.chaleur_sensible import chaleur_sensible
from src.chaleur_latente import (
    chaleur_latente_article,
    chaleur_latente_cequeau,
    es_magnus_tetens
)
from src.radiation import (
    rayonnement_ondes_courtes,
    rayonnement_ondes_longues,
    rayonnement_ondes_longues_ding
)
from src.glace import (
    epaisseur_glace_croissance,
    epaisseur_glace_fonte,
    choisir_hi,
    temperature_surface_glace
)
from src.interfaces import flux_eau_air, flux_glace_air
from src.bilan import flux_net

def main():
    print("======================================================================")
    print(" LECTURE DE EXEMPLE_TEST_CORRIGE.CSV ET BILAN THERMIQUE COMPARATIF")
    print("======================================================================")

    with open("data/exemple_test_corrige.csv", "r") as f:
        reader = csv.DictReader(f)
        ligne_id = 1
        for row in reader:

            # 1. Données d'entrée
            Ta = float(row["Ta"])
            va = float(row["va"])
            vs = float(row["vs"])
            HR = float(row["HR"])
            Fi = float(row["Fi"])
            Tw = float(row["Tw"])
            ha = float(row["ha"])
            hi_mesure = float(row["hi"])
            AFDD = float(row["AFDD"])
            ATDD = float(row["ATDD"])
            
            sr_in = float(row["sr_in"])
            sr_out = float(row["sr_out"])
            lr_in = float(row.get("lr_in", 0.0))
            lr_out = float(row.get("lr_out", 0.0))
            C = float(row["C"])
            ek = float(row.get("ek", 1.0))
            Le = float(row.get("Le", 0.0))
            A_surface = float(row["A"])
            A_fonte = float(row["A_fonte"])
            
            use_hi_mesure = int(row["use_hi_mesure"])
            use_lr_mesure = int(row.get("use_lr_mesure", 0))

            # 2. Épaisseur théorique de la glace
            alpha_h = 0.6
            hi_croissance = epaisseur_glace_croissance(alpha_h, AFDD)
            hi_fonte = epaisseur_glace_fonte(hi_croissance, A_fonte, ATDD)

            # 3. Choix du hi final
            if use_hi_mesure == 1:
                hi = hi_mesure
                source_hi = "Mesuré"
            else:
                hi = choisir_hi(Fi, Ta, hi_mesure, hi_croissance, hi_fonte)
                source_hi = "Calculé"

            # 4. Température de surface de la glace (Tis)
            ka = 0.024
            ki = 2.1
            Tis = temperature_surface_glace(ka, ki, hi, ha, Ta)

            # 5. Températures de surface selon l'interface
            Ts_aw = Tw
            Ts_ai = Tis

            # 6. Rayonnements (en W/m² puis convertis en MJ/m²/jour via 0.0864)
            phi_sr = rayonnement_ondes_courtes(sr_in, sr_out)
            
            # Calcul Longwave selon Ding et al. (2026) - Conditions Fi
            phi_lr_w_ding, phi_lr_i_ding = rayonnement_ondes_longues_ding(
                Tw=Ts_aw, Tis=Ts_ai, Ta=Ta, HR=HR, C=C, Fi=Fi, ek=ek
            )
            
            # Mesure Longwave (Apogee SN500SS)
            phi_lr_mesure = rayonnement_ondes_longues(lr_in, lr_out)

            #ajouter les données dans le csv pour comparer les 2 ensuite
            if use_lr_mesure == 1:
                phi_lr_aw = phi_lr_mesure
                phi_lr_ai = phi_lr_mesure
                source_lr = "Mesuré"
            else:
                phi_lr_aw = phi_lr_w_ding
                phi_lr_ai = phi_lr_i_ding
                source_lr = "Calculé (Ding)"

            NetRad_aw_W = phi_sr + phi_lr_aw
            NetRad_ai_W = phi_sr + phi_lr_ai
            NetRad_aw = NetRad_aw_W * 0.0864
            NetRad_ai = NetRad_ai_W * 0.0864

            # 7. Chaleur sensible φs (en MJ/m²/jour)
            phi_s_aw = chaleur_sensible(Ts_aw, Ta, va, vs, surface="eau")
            phi_s_ai = chaleur_sensible(Ts_ai, Ta, va, vs, surface="glace")

            # --- MÉTHODE 1 : ARTICLE / AÉRODYNAMIQUE ---
            phi_l_aw_art = chaleur_latente_article(Ts_aw, Ta, va, vs, HR, surface="eau")
            phi_l_ai_art = chaleur_latente_article(Ts_ai, Ta, va, vs, HR, surface="glace")
            phi_aw_art = flux_eau_air(NetRad_aw, phi_s_aw, phi_l_aw_art)
            phi_ai_art = flux_glace_air(NetRad_ai, phi_s_ai, phi_l_ai_art)
            phi_n_art = flux_net(phi_aw_art, phi_ai_art, Fi)

            # --- MÉTHODE 2 : CEQUEAU (basée sur Le, A, et conditions de Fi) ---
            phi_l_aw_ceq = chaleur_latente_cequeau(Ta, Le, Fi, A_surface, Ce=1.0)
            phi_l_ai_ceq = chaleur_latente_cequeau(Ta, Le, Fi, A_surface, Ce=1.0)
            phi_aw_ceq = flux_eau_air(NetRad_aw, phi_s_aw, phi_l_aw_ceq)
            phi_ai_ceq = flux_glace_air(NetRad_ai, phi_s_ai, phi_l_ai_ceq)
            phi_n_ceq = flux_net(phi_aw_ceq, phi_ai_ceq, Fi)

            # Affichage détaillé par simulation
            print(f"\n--- Simulation #{ligne_id} ---")
            print(f"  Météo & Paramètres : Ta={Ta}°C | Tw={Tw}°C | Tis={Tis:.2f}°C | HR={HR}% | va={va} m/s | C={C}")
            print(f"  Couverture Glace   : Fi={Fi} | hi={hi:.3f} m ({source_hi}) | Le={Le} m | A={A_surface} m²")
            print(f"  Longwave ({source_lr}) : φlr_w={phi_lr_w_ding:.2f} | φlr_i={phi_lr_i_ding:.2f} | φlr_mes={phi_lr_mesure:.2f} W/m²")
            print(f"  Rayonnements (Net) : NetRad_eau={NetRad_aw:.2f} | NetRad_glace={NetRad_ai:.2f} MJ/m²/j")
            print(f"  Chaleur Sensible   : φs_eau={phi_s_aw:.2f} | φs_glace={phi_s_ai:.2f} MJ/m²/j")
            
            # --- AFFICHAGE APART : COMPARAISON DE LA CHALEUR LATENTE ---
            if Fi == 0.0:
                print(f"  >>> [COMPARAISON CHALEUR LATENTE - EAU LIBRE (Fi = 0)]")
                print(f"      - Article (Aérodynamique) : φl_aw = {phi_l_aw_art:.2f} MJ/m²/j")
                print(f"      - CEQUEAU (Lame Le)       : φl_aw = {phi_l_aw_ceq:.2f} MJ/m²/j")
            elif Fi == 1.0:
                print(f"  >>> [COMPARAISON CHALEUR LATENTE - GLACE COMPLÈTE (Fi = 1)]")
                print(f"      - Article (Sublimation)   : φl_ai = {phi_l_ai_art:.2f} MJ/m²/j")
                print(f"      - CEQUEAU (Lame Le)       : φl_ai = {phi_l_ai_ceq:.2f} MJ/m²/j")
            else:
                print(f"  >>> [COMPARAISON CHALEUR LATENTE - ÉTAT MIXTE (Fi = {Fi})]")
                print(f"      - Article : φl_aw={phi_l_aw_art:.2f} | φl_ai={phi_l_ai_art:.2f} MJ/m²/j")
                print(f"      - CEQUEAU : φl_aw={phi_l_aw_ceq:.2f} | φl_ai={phi_l_ai_ceq:.2f} MJ/m²/j")

            print(f"  ------------------------------------------------------------------")
            print(f"  [1] Méthode ARTICLE :")
            print(f"      -> Flux Interfaces : φaw={phi_aw_art:.2f} | φai={phi_ai_art:.2f} MJ/m²/j")
            print(f"      -> Bilan Net (φn)  : {phi_n_art:.2f} MJ/m²/j")
            print(f"  [2] Méthode CEQUEAU :")
            print(f"      -> Flux Interfaces : φaw={phi_aw_ceq:.2f} | φai={phi_ai_ceq:.2f} MJ/m²/j")
            print(f"      -> Bilan Net (φn)  : {phi_n_ceq:.2f} MJ/m²/j")
            
            ligne_id += 1

    print("\n======================================================================")

if __name__ == "__main__":
    main()