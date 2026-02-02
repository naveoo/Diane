# Documentation - Configuration de Simulation de Factions Politiques

**Version:** 1.0  
**Date:** 30 janvier 2026

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Vue d'ensemble des systèmes](#2-vue-densemble-des-systèmes)
3. [Système de Puissance](#3-système-de-puissance-powerconfig)
4. [Système de Légitimité](#4-système-de-légitimité-legitimacyconfig)
5. [Système Économique](#5-système-économique-economyconfig)
6. [Analyse et Calibration Globale](#6-analyse-et-calibration-globale)
7. [Configurations des autres systèmes](#7-configurations-des-autres-systèmes)
8. [Conclusion et Recommandations](#8-conclusion-et-recommandations)

---

## 1. Introduction

Ce document présente la documentation complète du fichier de configuration `defaults.py` de la simulation de factions politiques. Il détaille chaque paramètre, les formules mathématiques appliquées et propose des conseils pour l'analyse et le calibrage des valeurs.

### 1.1 Structure du fichier

Le fichier est organisé en **neuf sections principales**, chacune regroupant les paramètres d'un système spécifique :

- `SimulationConfig` : Paramètres généraux de la simulation
- `FactionConfig` : Limites et valeurs par défaut des factions
- `RegionConfig` : Configuration des régions
- `PowerConfig` : Système de puissance
- `LegitimacyConfig` : Système de légitimité
- `EconomyConfig` : Système économique
- `ConflictConfig` : Gestion des conflits
- `AllianceConfig` : Gestion des alliances
- `CollapseConfig` : Effondrement des factions

Cette organisation modulaire permet une maintenance aisée et une compréhension claire des interdépendances.

### 1.2 Conventions de nommage

| Préfixe/Suffixe | Signification | Exemple |
|-----------------|---------------|---------|
| `default_*` | Valeurs initiales assignées aux nouvelles entités | `default_power = 50.0` |
| `min_* / max_*` | Limites strictes (bornes) pour les valeurs | `min_power = 0.0` |
| `*_threshold` | Seuils déclenchant des événements | `revolution_threshold = 25.0` |
| `*_chance` | Probabilités d'occurrence (0.0 à 1.0) | `revolution_chance = 0.15` |
| `*_factor / *_weight` | Coefficients multiplicateurs dans les formules | `stability_legitimacy_factor = 0.3` |
| `*_bonus / *_penalty` | Modificateurs additifs | `alliance_power_bonus = 0.1` |

---

## 2. Vue d'ensemble des systèmes

La simulation repose sur **trois piliers interdépendants** qui évoluent à chaque tick :

### 2.1 Les trois systèmes principaux

| Système | Description | Impact principal |
|---------|-------------|------------------|
| **Puissance** | Force militaire et politique d'une faction | Augmente avec les régions et alliances, décline naturellement |
| **Légitimité** | Acceptation populaire et soutien | Influencée par la stabilité, l'égalité économique et les ressources |
| **Économie** | Ressources disponibles pour maintenir l'ordre | Croît avec les revenus, diminue par corruption |

### 2.2 Cycle de mise à jour

À chaque tick, la méthode `Clock.update()` exécute **dans l'ordre** :

1. **Mise à jour de la puissance** (`_update_power`)
2. **Mise à jour de la légitimité** (`_update_legitimacy`)
3. **Mise à jour de l'économie** (`_update_economy`)

### 2.3 Interdépendances clés

```
Régions ──┬──> Puissance (+0.2/région)
          ├──> Ressources (+0.5/région)
          └──> Légitimité (via stabilité moyenne)

Ressources ──> Légitimité (pénalité si < 5.0)

Puissance (toutes factions) ──> Légitimité (via coefficient de Gini)
```

---

## 3. Système de Puissance (PowerConfig)

### 3.1 Paramètres

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `base_power_growth` | `0.01` | Croissance naturelle (+1% par tick) |
| `power_decay` | `0.005` | Déclin naturel (-0.5% par tick) |
| `region_power_weight` | `0.2` | Bonus par région contrôlée |
| `alliance_power_bonus` | `0.1` | Bonus par alliance active |
| `max_power` | `100.0` | Plafond maximal de puissance |

### 3.2 Formule mathématique

La puissance d'une faction est mise à jour selon la séquence suivante :

#### Étape 1 : Croissance de base
```
power_new = power × (1 + base_power_growth)
```

#### Étape 2 : Déclin naturel
```
power_new = power_new × (1 - power_decay)
```

#### Étape 3 : Bonus régional (si régions contrôlées)
```
power_new = power_new + (nb_regions × region_power_weight)
```

#### Étape 4 : Bonus alliances (si alliances actives)
```
power_new = power_new + (nb_alliances × alliance_power_bonus)
```

#### Étape 5 : Application du plafond
```
power_final = min(power_new, max_power)
```

### 3.3 Formule consolidée

```
power(t+1) = min(
    power(t) × (1 + base_power_growth) × (1 - power_decay)
    + (nb_regions × region_power_weight)
    + (nb_alliances × alliance_power_bonus),
    max_power
)
```

### 3.4 Analyse et calibration

#### Croissance nette sans territoires

Avec les valeurs par défaut :
```
Taux net = (1 + 0.01) × (1 - 0.005) = 1.01 × 0.995 ≈ 1.00495
```
Soit environ **+0.5% par tick**. Une faction sans territoire gagne donc très lentement en puissance.

#### Impact territorial

Chaque région ajoute **+0.2** de puissance brute par tick (avant application des multiplicateurs).

**Exemple :**
- Faction avec 5 régions : +1.0 de puissance brute/tick
- Après multiplicateurs : ~+1.005 supplémentaires

#### Scénarios de croissance

| Situation | Puissance initiale | Après 100 ticks | Après 1000 ticks |
|-----------|-------------------|-----------------|------------------|
| Sans territoire | 50.0 | ~52.5 | ~82.4 |
| 3 régions | 50.0 | ~70.3 | 100.0 (plafond) |
| 5 régions | 50.0 | ~80.5 | 100.0 (plafond) |

#### Recommandations de calibrage

**Pour une croissance plus rapide :**
- Augmenter `base_power_growth` (ex : `0.02` = +2%/tick)
- Résultat : factions atteignent le plafond plus vite

**Pour privilégier l'expansion territoriale :**
- Augmenter `region_power_weight` (ex : `0.5`)
- Résultat : contrôle territorial devient déterminant

**Pour stabiliser les grandes puissances :**
- Réduire `max_power` (ex : `80.0`)
- Résultat : plafond atteint plus tôt, force l'équilibre

**Pour un déclin plus marqué :**
- Augmenter `power_decay` (ex : `0.01` = -1%/tick)
- Résultat : factions doivent constamment conquérir pour compenser

---

## 4. Système de Légitimité (LegitimacyConfig)

### 4.1 Paramètres

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `base_legitimacy_decay` | `0.01` | Érosion naturelle (-1%/tick) |
| `stability_legitimacy_factor` | `0.3` | Coefficient de conversion stabilité→légitimité |
| `inequality_penalty` | `0.4` | Pénalité d'inégalité (coefficient de Gini) |
| `starvation_legitimacy_loss` | `0.5` | Perte absolue si famine |
| `revolution_threshold` | `25.0` | Seuil déclenchant les révolutions |
| `revolution_chance` | `0.15` | 15% de probabilité si sous le seuil |
| `legitimacy_floor` | `0.0` | Minimum absolu |
| `legitimacy_ceiling` | `100.0` | Maximum absolu |

### 4.2 Formule mathématique

#### Étape 1 : Déclin de base
```
legitimacy = legitimacy × (1 - base_legitimacy_decay)
```

#### Étape 2 : Bonus de stabilité régionale
```
avg_stability = Σ(region.stability) / nb_regions

legitimacy = legitimacy + (avg_stability × stability_legitimacy_factor)
```

**Note :** Ce bonus n'est appliqué que si la faction contrôle au moins une région.

#### Étape 3 : Pénalité d'inégalité (coefficient de Gini)

Le coefficient de Gini mesure l'inégalité de distribution de la puissance entre **toutes les factions actives** (power ≠ 0).

```
gini_coefficient = gini([f.power pour f in factions_actives])  // ∈ [0, 1]

legitimacy = legitimacy - (gini_coefficient × inequality_penalty × 100)
```

**Interprétation du Gini :**
- `0.0` : égalité parfaite (toutes les factions ont la même puissance)
- `0.5` : inégalité modérée
- `1.0` : monopole total (une faction détient toute la puissance)

#### Étape 4 : Pénalité de famine
```
Si resources < resource_starvation_threshold (5.0) :
    legitimacy = legitimacy - starvation_legitimacy_loss
```

#### Étape 5 : Application des limites
```
legitimacy = clamp(legitimacy, legitimacy_floor, legitimacy_ceiling)
```

### 4.3 Formule consolidée

```
legitimacy(t+1) = clamp(
    legitimacy(t) × (1 - base_legitimacy_decay)
    + (avg_stability × stability_legitimacy_factor)
    - (gini × inequality_penalty × 100)
    - (starvation_penalty si resources < 5.0),
    0.0,
    100.0
)
```

### 4.4 Analyse et calibration

#### ⚠️ **BUG CRITIQUE DÉTECTÉ** dans le code

**Ligne incorrecte :**
```python
if f.legitimacy < Defaults.legitimacy.legitimacy_ceiling:
    f.set_legitimacy(Defaults.legitimacy.legitimacy_ceiling)
```

**Problème :** Utilise `<` au lieu de `>`. Actuellement, **toute faction avec légitimité inférieure à 100 se voit attribuer 100**, ce qui annule complètement le système de légitimité.

**Correction nécessaire :**
```python
if f.legitimacy > Defaults.legitimacy.legitimacy_ceiling:
    f.set_legitimacy(Defaults.legitimacy.legitimacy_ceiling)
```

#### Impact du coefficient de Gini

| Gini | Signification | Pénalité (inequality_penalty=0.4) |
|------|---------------|-----------------------------------|
| 0.0 | Égalité parfaite | 0 points |
| 0.3 | Faible inégalité | -12 points |
| 0.5 | Inégalité moyenne | -20 points |
| 0.7 | Forte inégalité | -28 points |
| 1.0 | Monopole total | -40 points |

**Implications :**
- Une faction dominante (Gini élevé) réduit la légitimité de **toutes** les factions
- Encourage un équilibre des puissances
- Peut déclencher des révolutions même pour des factions stables si l'inégalité globale est forte

#### Scénarios typiques

**Scénario 1 : Faction stable avec territoires**
- Stabilité moyenne des régions : 80.0
- Gini global : 0.3 (faible inégalité)
- Ressources : 30.0 (pas de famine)

```
legitimacy(t+1) = legitimacy(t) × 0.99
                  + (80.0 × 0.3)
                  - (0.3 × 0.4 × 100)
                = legitimacy(t) × 0.99 + 24.0 - 12.0
                = legitimacy(t) × 0.99 + 12.0
```
**Résultat :** Légitimité augmente progressivement.

**Scénario 2 : Faction en famine dans un monde inégal**
- Stabilité moyenne : 60.0
- Gini global : 0.8 (forte inégalité)
- Ressources : 3.0 (famine)

```
legitimacy(t+1) = legitimacy(t) × 0.99
                  + (60.0 × 0.3)
                  - (0.8 × 0.4 × 100)
                  - 0.5
                = legitimacy(t) × 0.99 + 18.0 - 32.0 - 0.5
                = legitimacy(t) × 0.99 - 14.5
```
**Résultat :** Chute rapide de la légitimité (environ -15 points/tick).

#### Recommandations de calibrage

**Pour ralentir la chute de légitimité :**
- Réduire `base_legitimacy_decay` à `0.005` (-0.5%/tick)
- Augmenter `stability_legitimacy_factor` à `0.5` pour valoriser la stabilité

**Pour tolérer plus d'inégalité :**
- Réduire `inequality_penalty` à `0.2`
- Résultat : Gini de 1.0 inflige -20 au lieu de -40

**Pour des révolutions plus fréquentes :**
- Augmenter `revolution_chance` à `0.30` (30%)
- Ou augmenter `revolution_threshold` à `35.0`

**Pour des situations de famine plus tolérables :**
- Réduire `starvation_legitimacy_loss` à `0.2`
- Ou réduire `resource_starvation_threshold` à `3.0`

---

## 5. Système Économique (EconomyConfig)

### 5.1 Paramètres

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `base_resource_income` | `1.0` | Revenu de base par tick |
| `region_resource_bonus` | `0.5` | Bonus par région contrôlée |
| `corruption_factor` | `0.02` | Facteur de corruption appliqué |
| `resource_starvation_threshold` | `5.0` | Seuil de famine (impact sur légitimité) |

### 5.2 Formule mathématique

#### Étape 1 : Revenu de base
```
resources = resources + base_resource_income
```

#### Étape 2 : Bonus régional
```
resources = resources + (nb_regions × region_resource_bonus)
```

#### Étape 3 : Application de la corruption
```
resources = resources × corruption_factor
```

### 5.3 Formule consolidée (implémentation actuelle)

```
resources(t+1) = (resources(t) + base_resource_income + nb_regions × region_resource_bonus) × corruption_factor
```

### 5.4 Analyse et calibration

```
resources(t+1) = (resources(t) + base_resource_income + nb_regions × region_resource_bonus) × (1 - corruption_factor)
```

#### Équilibre économique

À l'équilibre (ressources stables), les revenus compensent la corruption :

```
revenus = corruption × resources_equilibre

resources_equilibre = (base_income + nb_regions × bonus) / corruption_factor

Avec les valeurs par défaut (corrigées) :
- Sans région : 1.0 / 0.02 = 50.0
- Avec 3 régions : (1.0 + 1.5) / 0.02 = 125.0
```

#### Recommandations de calibrage

**Après correction du bug :**

1. **Ajuster le taux de corruption :**
   - `corruption_factor = 0.01` : 1% de perte (économie stable)
   - `corruption_factor = 0.05` : 5% de perte (économie difficile)

2. **Augmenter les revenus si accumulation trop lente :**
   - `base_resource_income = 2.0`
   - `region_resource_bonus = 1.0`

3. **Ajuster le seuil de famine :**
   - `resource_starvation_threshold = 10.0` pour un système plus exigeant
   - `resource_starvation_threshold = 2.0` pour plus de tolérance

**Exemple de configuration équilibrée :**
```python
base_resource_income: float = 2.0
region_resource_bonus: float = 1.0
corruption_factor: float = 0.03  # 3% de perte
resource_starvation_threshold: float = 10.0
```

---

## 6. Analyse et Calibration Globale

### 6.1 Interdépendances entre systèmes

#### Économie → Légitimité

```
resources < 5.0  ──>  legitimacy -= 0.5/tick
```

**Impact :** Une faction en famine perd rapidement sa légitimité, risquant une révolution.

#### Puissance → Légitimité (via Gini)

```
Distribution de puissance inégale  ──>  Gini élevé  ──>  Pénalité pour toutes les factions
```

**Impact :** Une faction dominante déstabilise l'ensemble du système politique.

#### Régions → Tous les systèmes

```
Régions ──┬──> Puissance (+0.2/région)
          ├──> Ressources (+0.5/région)
          └──> Légitimité (via stabilité moyenne)
```

**Impact :** Le contrôle territorial est crucial, mais des régions instables peuvent être contre-productives.

### 6.2 Scénarios de test recommandés

#### Scénario 1 : Faction isolée sans territoire

**Configuration :**
- Puissance initiale : 50.0
- Légitimité initiale : 50.0
- Ressources initiales : 50.0
- Régions : 0
- Alliances : 0

**Objectifs :**
- Vérifier les taux de croissance/déclin de base
- Observer l'effet du bug économique

**Résultats attendus (après correction des bugs) :**
- Puissance : croissance très lente (~0.5%/tick)
- Légitimité : déclin lent (-1%/tick) puis stabilisation
- Ressources : croissance linéaire (+1.0/tick avant corruption)

#### Scénario 2 : Deux factions équilibrées

**Configuration :**
- 2 factions avec puissance = 50.0 chacune
- Chaque faction contrôle 3 régions (stabilité = 100.0)

**Objectifs :**
- Observer l'impact du coefficient de Gini (proche de 0)
- Vérifier le bonus de stabilité

**Résultats attendus :**
- Gini ≈ 0.0 → faible pénalité de légitimité
- Légitimité augmente grâce à la stabilité régionale
- Situation stable et durable

#### Scénario 3 : Faction dominante (monopole)

**Configuration :**
- Faction A : puissance = 90.0, 8 régions
- Faction B : puissance = 10.0, 1 région

**Objectifs :**
- Vérifier l'effondrement par inégalité
- Tester le déclenchement des révolutions

**Résultats attendus :**
- Gini ≈ 0.8-0.9 → pénalité de -32 à -36 points
- Légitimité de toutes les factions chute
- Révolution probable si légitimité < 25.0

#### Scénario 4 : Famine

**Configuration :**
- Faction avec ressources initiales = 3.0 (< 5.0)
- 0 région (pas de bonus économique)

**Objectifs :**
- Tester le seuil de famine
- Observer la spirale descendante

**Résultats attendus :**
- Perte de -0.5 légitimité/tick (pénalité famine)
- Avec le bug actuel : effondrement économique immédiat
- Après correction : possibilité de récupération lente

### 6.3 Métriques à surveiller

Pour un suivi efficace de la simulation, enregistrez ces métriques à chaque `snapshot_interval` :

#### Métriques globales

- **Coefficient de Gini** : mesure l'inégalité de puissance
- **Nombre de factions actives** : factions avec power > 0
- **Puissance totale** : somme de toutes les puissances

#### Métriques par faction

- **Puissance** : valeur et tendance (croissance/déclin)
- **Légitimité** : valeur et nombre sous seuil de révolution
- **Ressources** : valeur et nombre en famine
- **Nombre de régions contrôlées**
- **Stabilité moyenne** : des régions contrôlées
- **Nombre d'alliances**

#### Métriques d'événements

- **Nombre de révolutions déclenchées**
- **Nombre de factions effondrées**
- **Nombre de révoltes**
- **Formations/ruptures d'alliances**

### 6.4 Graphiques recommandés

1. **Évolution temporelle de la puissance** (toutes factions)
2. **Évolution du coefficient de Gini**
3. **Évolution de la légitimité moyenne**
4. **Distribution des ressources** (histogramme)
5. **Carte de contrôle territorial** (par faction)

---

## 7. Configurations des autres systèmes

### 7.1 Configuration Simulation (SimulationConfig)

```python
@dataclass(frozen=True)
class SimulationConfig:
    max_ticks: int = 1_000_000          # Durée maximale de la simulation
    snapshot_interval: int = 100        # Fréquence de sauvegarde des métriques
    base_tick_duration: float = 1.0     # Durée d'un tick (en secondes simulées)
```

**Usage :**
- `max_ticks` : Arrête la simulation après ce nombre d'itérations
- `snapshot_interval` : Détermine quand sauvegarder les données (tous les N ticks)
- `base_tick_duration` : Permet de convertir les ticks en temps simulé

### 7.2 Configuration Factions (FactionConfig)

```python
@dataclass(frozen=True)
class FactionConfig:
    default_name: str = "FactionX"
    max_name_size: int = 99
    
    # Puissance
    default_power: float = 50.0
    min_power: float = 0.0
    max_power: float = 100.0
    
    # Légitimité
    default_legitimacy: float = 50.0
    min_legitimacy: float = 0.0
    max_legitimacy: float = 100.0
    
    # Ressources
    default_resources: float = 50.0
    min_resources: float = 0.0
    max_resources: float = 100.0
    
    # Alliances
    max_alliances: int = 3
```

**Usage :**
- Définit les valeurs initiales pour les nouvelles factions
- Établit les limites min/max pour validation
- `max_alliances` : Limite le nombre d'alliances simultanées par faction

### 7.3 Configuration Régions (RegionConfig)

```python
@dataclass(frozen=True)
class RegionConfig:
    default_name: str = "RegionX"
    max_name_size: int = 99
    
    # Population
    default_population: int = 1000
    min_population: int = 10
    max_population: int = 10_000
    
    # Stabilité
    default_stability: float = 100.0
    default_stability_insurrection: float = 50.0  # Après une insurrection
    min_stability: float = 0.0
    max_stability: float = 100.0
```

**Usage :**
- `default_stability` : Stabilité initiale d'une région en temps de paix
- `default_stability_insurrection` : Stabilité après un événement de révolte
- La population peut influencer d'autres mécaniques (non implémentées actuellement)

### 7.4 Configuration Conflits (ConflictConfig)

```python
@dataclass(frozen=True)
class ConflictConfig:
    revolt_stability_threshold: float = 30.0     # Seuil de déclenchement
    revolution_legitimacy_threshold: float = 20.0
    revolt_power_loss: float = 10.0              # Perte en cas de révolte
    revolt_stability_loss: float = 20.0
    revolt_chance: float = 30.0                  # Probabilité (%)
    civil_war_chance: float = 0.05               # 5% de chance
    coup_d_etat_chance: float = 0.03             # 3% de chance
```

**Usage (non implémenté dans le code fourni) :**
- Détermine quand et comment les conflits se déclenchent
- `revolt_chance` : Si stabilité < seuil, jet de dé pour déclencher une révolte
- Impact sur la puissance et la stabilité de la faction

### 7.5 Configuration Alliances (AllianceConfig)

```python
@dataclass(frozen=True)
class AllianceConfig:
    alliance_power_ratio_limit: float = 1.5      # Différence max de puissance
    betrayal_cost: float = 15.0                  # Coût de légitimité d'une trahison
    alliance_formation_chance: float = 0.05      # 5% de chance par tick
    alliance_break_chance: float = 0.02          # 2% de chance par tick
```

**Usage (non implémenté dans le code fourni) :**
- `alliance_power_ratio_limit` : Deux factions ne peuvent s'allier que si leur ratio de puissance < 1.5
- `betrayal_cost` : Pénalité de légitimité pour rompre une alliance
- Probabilités pour la formation/rupture automatique d'alliances

### 7.6 Configuration Effondrement (CollapseConfig)

```python
@dataclass(frozen=True)
class CollapseConfig:
    faction_power_floor: float = 5.0             # Seuil d'effondrement
    faction_legitimacy_floor: float = 10.0
    collapse_power_transfer_ratio: float = 0.3   # 30% transféré aux voisins
```

**Usage (non implémenté dans le code fourni) :**
- Une faction s'effondre si puissance < 5.0 OU légitimité < 10.0
- Lors de l'effondrement, 30% de sa puissance est redistribuée aux factions voisines
- Les régions contrôlées deviennent libres ou sont conquises

---

## 8. Conclusion et Recommandations

### 8.1 Bugs critiques à corriger

### 8.2 Améliorations proposées

#### Ajout de paramètres manquants

**Dans PowerConfig :**
```python
power_from_resources_factor: float = 0.01  # Conversion ressources → puissance
```

**Dans LegitimacyConfig :**
```python
alliance_legitimacy_bonus: float = 2.0  # Bonus par alliance
military_victory_bonus: float = 5.0     # Bonus après victoire militaire
```

**Dans EconomyConfig :**
```python
trade_income_multiplier: float = 0.1    # Bonus par alliance commerciale
war_economy_cost: float = 2.0           # Coût supplémentaire en guerre
```

#### Réorganisation suggérée

Créer une classe `EventConfig` pour centraliser tous les seuils d'événements :

```python
@dataclass(frozen=True)
class EventConfig:
    # Révolution
    revolution_legitimacy_threshold: float = 25.0
    revolution_chance: float = 0.15
    
    # Révolte
    revolt_stability_threshold: float = 30.0
    revolt_chance: float = 0.30
    
    # Famine
    starvation_threshold: float = 5.0
    starvation_legitimacy_loss: float = 0.5
    
    # Effondrement
    collapse_power_threshold: float = 5.0
    collapse_legitimacy_threshold: float = 10.0
```

### 8.3 Configurations recommandées par style de jeu

#### Style "Équilibré" (par défaut)

Configuration actuelle après correction des bugs.

#### Style "Expansion rapide"

```python
PowerConfig:
    base_power_growth = 0.02
    region_power_weight = 0.5
    alliance_power_bonus = 0.2

EconomyConfig:
    base_resource_income = 2.0
    region_resource_bonus = 1.0
    corruption_factor = 0.01
```

#### Style "Survie difficile"

```python
LegitimacyConfig:
    base_legitimacy_decay = 0.02
    inequality_penalty = 0.6
    revolution_threshold = 30.0
    revolution_chance = 0.25

EconomyConfig:
    corruption_factor = 0.05
    resource_starvation_threshold = 10.0
```

#### Style "Empire dominant"

```python
PowerConfig:
    max_power = 200.0
    region_power_weight = 1.0

LegitimacyConfig:
    inequality_penalty = 0.2  # Tolérance accrue aux inégalités

CollapseConfig:
    faction_power_floor = 1.0  # Élimine rapidement les faibles
```

### 8.4 Tests unitaires recommandés

#### Test 1 : Croissance sans territoire

```python
def test_power_growth_no_territory():
    faction = Faction(power=50.0, regions=[], alliances=[])
    for _ in range(100):
        update_power(faction)
    assert 52.0 < faction.power < 53.0
```

#### Test 2 : Impact du Gini

```python
def test_gini_penalty():
    faction1 = Faction(power=90.0, legitimacy=50.0)
    faction2 = Faction(power=10.0, legitimacy=50.0)
    
    update_legitimacy([faction1, faction2])
    
    # Gini élevé devrait réduire la légitimité de toutes les factions
    assert faction1.legitimacy < 50.0
    assert faction2.legitimacy < 50.0
```

#### Test 3 : Famine

```python
def test_starvation_penalty():
    faction = Faction(resources=3.0, legitimacy=50.0)
    
    update_legitimacy(faction)
    
    assert faction.legitimacy == 50.0 - 0.5  # Pénalité appliquée
```

### 8.5 Fichier de configuration réorganisé et corrigé

Voir le fichier `defaults_fixed.py` ci-joint pour une version corrigée et enrichie avec :
- Corrections des bugs identifiés
- Commentaires détaillés
- Formules mathématiques en documentation
- Suggestions de valeurs alternatives
- Validation des paramètres

---

## Annexe A : Formules mathématiques complètes

### Formule complète du système (un tick)

```
Pour chaque faction f :

1. Mise à jour puissance :
   power(t+1) = min(
       power(t) × (1.01) × (0.995)
       + nb_regions × 0.2
       + nb_alliances × 0.1,
       100.0
   )

2. Calcul Gini global :
   gini = gini_coefficient([f.power pour f si f.power > 0])

3. Mise à jour légitimité :
   avg_stab = Σ(r.stability) / nb_regions si nb_regions > 0 sinon 0
   
   legitimacy(t+1) = clamp(
       legitimacy(t) × 0.99
       + avg_stab × 0.3
       - gini × 40
       - (0.5 si resources < 5.0 sinon 0),
       0.0,
       100.0
   )

4. Mise à jour économie (APRÈS CORRECTION) :
   resources(t+1) = (
       resources(t)
       + 1.0
       + nb_regions × 0.5
   ) × (1 - 0.02)
```

### Matrice des influences

|   | Puissance | Légitimité | Ressources | Régions | Alliances |
|---|-----------|------------|------------|---------|-----------|
| **Puissance** | ↗ +1% / ↘ -0.5% | via Gini (↘) | - | ↗ +0.2/région | ↗ +0.1/alliance |
| **Légitimité** | - | ↘ -1% | ↘ si < 5.0 | ↗ via stabilité | - |
| **Ressources** | - | - | ↘ -2% | ↗ +0.5/région | - |
| **Régions** | ↗ | ↗ | ↗ | - | - |
| **Alliances** | ↗ | - | - | - | - |

Légende :
- ↗ : influence positive
- ↘ : influence négative
- `-` : pas d'influence directe

---

## Annexe B : Glossaire

| Terme | Définition |
|-------|------------|
| **Tick** | Unité de temps de base de la simulation (1 itération) |
| **Faction** | Entité politique dans la simulation |
| **Puissance** | Force militaire et politique d'une faction (0-100) |
| **Légitimité** | Acceptation populaire et soutien d'une faction (0-100) |
| **Ressources** | Capital économique abstrait d'une faction |
| **Région** | Territoire pouvant être contrôlé par une faction |
| **Stabilité** | Niveau d'ordre et de paix dans une région (0-100) |
| **Gini** | Coefficient mesurant l'inégalité de distribution (0-1) |
| **Famine** | État où les ressources < seuil (5.0) |
| **Révolution** | Événement déclenchable si légitimité < seuil (25.0) |
| **Effondrement** | Disparition d'une faction (puissance ou légitimité trop faible) |

---

## Annexe C : Références et lectures complémentaires

### Coefficient de Gini
- Mesure statistique d'inégalité développée par Corrado Gini (1912)
- Formule : `G = (Σ|xi - xj|) / (2n²μ)` où μ est la moyenne
- Valeur 0 = égalité parfaite, 1 = inégalité maximale

### Modèles politiques similaires
- Modèles de dynamique des conflits (Richardson, 1960)
- Théorie de la stabilité hégémonique (Gilpin, 1981)
- Modèles agent-based de formation d'alliances (Axelrod, 1997)

### Implémentation technique
- `dataclass(frozen=True)` : crée des classes immuables en Python
- Pattern "Strategy" pour les différentes configurations
- Tests basés sur la simulation Monte Carlo recommandés

---