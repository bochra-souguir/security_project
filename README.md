# 🔐 Projet P1-C1 : Cryptanalyse Intelligente Automatique

**Étudiant** : Bochra Souguir  
**Classe** : 3LI - ESSTHS  
**Date de rendu** : 03/01/2026  
**Enseignant** : Ala Eddine KHARRAT

## 📋 Description
Outil de cryptanalyse automatique capable de détecter et casser les chiffrements de César et Vigenère sans connaître la clé à l'avance.

### Fonctionnalités implémentées :
- ✅ **Détection automatique** : César vs Vigenère via indice de coïncidence
- ✅ **César** : Brute-force complet avec scoring linguistique
- ✅ **Vigenère** : Méthode Kasiski + analyse fréquentielle
- ✅ **Système de scoring** : 4 métriques combinées (mots valides, stopwords, entropie, bigrams)
- ✅ **Interface CLI** : Arguments avancés, sortie JSON, logs détaillés
- ✅ **Tests unitaires** : 32/37 tests passants (86% de succès)

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets)

### Installation
```bash
# Cloner le projet
git clone https://github.com/bochra-souguir/security_project.git
cd security_project

# Créer environnement virtuel
python -m venv venv

# Activer
# Windows :
venv\Scripts\activate
# Linux/Mac :
source venv/bin/activate

# Installer dépendances
pip install pytest pytest-cov nltk
