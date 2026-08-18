# Bilan Thermique – Sainte-Marguerite River (à completer)

Ce dépôt contient deux implémentations (Python et C++) du modèle de bilan thermique
utilisé pour analyser les échanges de chaleur entre la rivière Sainte-Marguerite et l’atmosphère,
selon la méthodologie de Ding et al. (2026).

## Structure du dépôt

- `python/` : version complète du modèle en Python
- `cpp/` : version C++ (en développement)
- `data/` : fichiers d’entrée (exemple.csv)
- `src/` : modules du modèle (chaleur sensible, latente, glace, interfaces, etc.)

## Méthodologie

Le modèle calcule :
- Rayonnement net (ondes courtes + ondes longues)
- Chaleur sensible (Rimsha-Donchenko, 1957)
- Chaleur latente (Rimsha-Donchenko, 1957)
- Température de surface de la glace (Lian & Zhao, 2011)
- Épaisseur de glace (Stefan+Michel, Bilello)
- Flux eau-air et glace-air
- Bilan thermique net selon Ding et al. (2026)

## Exécution

