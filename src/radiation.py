# src/radiation.py

def rayonnement_ondes_courtes(sr_in: float, sr_out: float) -> float:
    """
    Rayonnement net à ondes courtes φsr (W/m²)
    φsr = SW_In − SW_Out
    Mesure Apogee SN500SS
    """
    return sr_in - sr_out


def rayonnement_ondes_longues(lr_in: float, lr_out: float) -> float:
    """
    Rayonnement net à ondes longues φlr (W/m²)
    φlr = LW_In − LW_Out
    Mesure Apogee SN500SS
    """
    return lr_in - lr_out
