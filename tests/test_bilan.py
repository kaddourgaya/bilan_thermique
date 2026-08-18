# tests/test_bilan.py

from src.bilan import flux_net

def test_flux_net():
    assert flux_net(100, -50, 0.5) == 25
