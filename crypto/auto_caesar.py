"""
Cracking automatique du chiffrement de César
"""

from .caesar import decrypt
from .scoring import score_text


def crack_caesar(ciphertext, top_n=5, data_dir='data'):
    """
    Casse automatiquement un chiffrement de César
    
    Stratégie:
    1. Générer les 25 candidats possibles
    2. Scorer chaque candidat
    3. Trier par score décroissant
    4. Retourner le top N
    
    Args:
        ciphertext (str): Texte chiffré
        top_n (int): Nombre de meilleurs candidats à retourner
        data_dir (str): Répertoire des données linguistiques
    
    Returns:
        list: Liste de dictionnaires avec {key, score, plaintext}
    
    Exemple:
        >>> cipher = "Khoor Zruog"
        >>> results = crack_caesar(cipher, top_n=3)
        >>> results[0]['key']
        3
        >>> results[0]['plaintext']
        'Hello World'
    """
    candidates = []
    
    print(f"[*] Analyse de César : génération de 25 candidats...")
    
    # Bruteforce sur les 25 clés possibles
    for key in range(1, 26):
        plaintext = decrypt(ciphertext, key)
        score = score_text(plaintext, data_dir)
        
        candidates.append({
            'key': key,
            'score': score,
            'plaintext': plaintext,
            'excerpt': plaintext[:150]  # Extrait pour affichage
        })
    
    # Trier par score décroissant
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"[✓] Meilleur candidat : clé={candidates[0]['key']}, "
          f"score={candidates[0]['score']:.2f}")
    
    return candidates[:top_n]


def crack_caesar_fast(ciphertext):
    """
    Version rapide : retourne uniquement le meilleur candidat
    
    Args:
        ciphertext (str): Texte chiffré
    
    Returns:
        dict: Meilleur candidat
    """
    results = crack_caesar(ciphertext, top_n=1)
    return results[0]