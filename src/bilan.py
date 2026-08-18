def flux_net(phi_aw: float, phi_ai: float, Fi: float) -> float:
    """
    Bilan thermique net φn (W/m²)
    Trois conditions :
    - Fi = 0   → chenal ouvert       → φn = φaw
    - 0 < Fi < 1 → partiellement glacé → φn = φaw(1-Fi) + φai*Fi
    - Fi = 1   → entièrement glacé   → φn = φai
    """
    if Fi <= 0:
        return phi_aw
    elif Fi >= 1:
        return phi_ai
    else:
        return phi_aw * (1 - Fi) + phi_ai * Fi
