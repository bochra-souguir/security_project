### **8. bin/crack_auto.py**
 
#!/usr/bin/env python3
"""
CLI Principal - Cryptanalyse Automatique
Projet P1-C1 - ESSTHS 2025/2026

Usage:
    python bin/crack_auto.py --input data/test.txt --top 5
    python bin/crack_auto.py --input data/test.txt --json > results.json
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto.detector import detect_cipher_type, analyze_text_properties
from crypto.auto_caesar import crack_caesar
from crypto.auto_vigenere import crack_vigenere


def print_banner():
    """Affiche la bannière du programme"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     CRYPTANALYSE AUTOMATIQUE - Projet P1-C1              ║
║     César & Vigenère - Auto Cracking Tool                ║
║                                                           ║
║                                    
║                                    
║                                      
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def load_ciphertext(filepath):
    """
    Charge le texte chiffré depuis un fichier
    
    Args:
        filepath (str): Chemin du fichier
    
    Returns:
        str: Contenu du fichier
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erreur : fichier '{filepath}' introuvable")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
        sys.exit(1)


def save_results(results, output_file):
    """
    Sauvegarde les résultats en JSON
    
    Args:
        results (dict): Résultats de l'analyse
        output_file (str): Fichier de sortie
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Résultats sauvegardés : {output_file}")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")


def print_results_human(results, cipher_type):
    """
    Affiche les résultats en format lisible
    
    Args:
        results (dict): Résultats de l'analyse
        cipher_type (str): Type de chiffrement détecté
    """
    print("\n" + "="*70)
    print("📊 RÉSULTATS DE L'ANALYSE")
    print("="*70)
    
    print(f"\n🔍 Type de chiffrement détecté : {cipher_type.upper()}")
    
    props = results['text_properties']
    print(f"\n📈 Propriétés du texte chiffré :")
    print(f"   - Longueur : {props['length']} caractères")
    print(f"   - Indice de coïncidence : {props['ic']:.4f}")
    print(f"   - Entropie : {props['entropy']:.4f} bits/caractère")
    
    print(f"\n🏆 Top {len(results['candidates'])} candidats :\n")
    
    for i, candidate in enumerate(results['candidates'], 1):
        print(f"┌─ Candidat #{i} " + "─"*55)
        print(f"│  🔑 Clé : {candidate['key']}")
        print(f"│  ⭐ Score : {candidate['score']:.2f}/25")
        
        if cipher_type == 'vigenere':
            print(f"│  📏 Longueur clé : {candidate.get('key_length', 'N/A')}")
        
        print(f"│")
        print(f"│  📝 Extrait du texte déchiffré :")
        
        # Afficher l'extrait avec retour à la ligne propre
        excerpt = candidate['excerpt']
        words = excerpt.split()
        line = "│     "
        for word in words:
            if len(line) + len(word) + 1 > 70:
                print(line)
                line = "│     " + word + " "
            else:
                line += word + " "
        if line.strip() != "│":
            print(line)
        
        print(f"└" + "─"*67 + "\n")
    
    print("="*70)
    print(f"\n✅ Analyse terminée !")
    
    # Recommandation
    best = results['candidates'][0]
    print(f"\n💡 Recommandation : La clé la plus probable est '{best['key']}'")
    print(f"   avec un score de {best['score']:.2f}/25")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description='Outil de cryptanalyse automatique pour César et Vigenère',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python bin/crack_auto.py --input data/test_caesar.txt
  python bin/crack_auto.py --input data/test_vigenere.txt --top 3
  python bin/crack_auto.py --input data/challenge.txt --json --output results.json
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Fichier contenant le texte chiffré'
    )
    
    parser.add_argument(
        '--top', '-t',
        type=int,
        default=5,
        help='Nombre de meilleurs candidats à afficher (défaut: 5)'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Sortie en format JSON'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Fichier de sortie pour sauvegarder les résultats'
    )
    
    parser.add_argument(
        '--data-dir', '-d',
        default='data',
        help='Répertoire contenant les fichiers linguistiques (défaut: data)'
    )
    
    parser.add_argument(
        '--force-type',
        choices=['caesar', 'vigenere'],
        help='Forcer le type de chiffrement (sans auto-détection)'
    )
    
    args = parser.parse_args()
    
    # Afficher la bannière (sauf en mode JSON)
    if not args.json:
        print_banner()
        print(f"📂 Chargement du fichier : {args.input}\n")
    
    # Charger le texte chiffré
    ciphertext = load_ciphertext(args.input)
    
    if not args.json:
        print(f"✅ Fichier chargé : {len(ciphertext)} caractères\n")
        print("🔄 Analyse en cours...\n")
    
    # Détecter le type de chiffrement
    if args.force_type:
        cipher_type = args.force_type
        if not args.json:
            print(f"⚠️  Type forcé : {cipher_type.upper()}\n")
    else:
        cipher_type = detect_cipher_type(ciphertext)
        if not args.json:
            print(f"🔍 Détection automatique : {cipher_type.upper()}\n")
    
    # Analyser les propriétés du texte
    text_props = analyze_text_properties(ciphertext)
    
    # Cracker selon le type
    if cipher_type == 'caesar':
        candidates = crack_caesar(ciphertext, top_n=args.top, data_dir=args.data_dir)
    else:
        candidates = crack_vigenere(ciphertext, top_n=args.top, data_dir=args.data_dir)
    
    # Préparer les résultats
    results = {
        'input_file': args.input,
        'cipher_type': cipher_type,
        'text_properties': text_props,
        'candidates': candidates
    }
    
    # Affichage
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_results_human(results, cipher_type)
    
    # Sauvegarde optionnelle
    if args.output:
        save_results(results, args.output)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption utilisateur (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n[X] Erreur fatale : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
