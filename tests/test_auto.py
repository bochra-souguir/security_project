"""
Tests d'intégration pour la cryptanalyse automatique
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from crypto.detector import detect_cipher_type, calculate_ic
from crypto.auto_caesar import crack_caesar
from crypto.auto_vigenere import crack_vigenere
from crypto.caesar import encrypt as caesar_encrypt
from crypto.vigenere import encrypt as vigenere_encrypt


class TestDetector:
    """Tests pour la détection automatique"""
    
    def test_detect_caesar(self):
        """Test de détection de César"""
        plaintext = "this is a long text in english with many words"
        ciphertext = caesar_encrypt(plaintext, 7)
        
        detected = detect_cipher_type(ciphertext)
        assert detected == 'caesar'
    
    def test_detect_vigenere(self):
        """Test de détection de Vigenère"""
        plaintext = "this is a long text in english with many words"
        ciphertext = vigenere_encrypt(plaintext, "ESSTHS")
        
        detected = detect_cipher_type(ciphertext)
        assert detected == 'vigenere'
    
    def test_ic_calculation(self):
        """Test du calcul de l'IC"""
        # Texte aléatoire → IC bas
        random_text = "XYZABCQWERTY"
        ic_random = calculate_ic(random_text)
        assert ic_random < 0.05
        
        # Texte en anglais → IC plus élevé
        english_text = "the quick brown fox jumps over the lazy dog"
        ic_english = calculate_ic(english_text)
        assert ic_english > 0.055


class TestAutoCrackingCaesar:
    """Tests pour le cracking automatique de César"""
    
    def test_crack_simple(self):
        """Test de cracking simple"""
        plaintext = "this is a secret message that should be cracked easily"
        key = 13
        ciphertext = caesar_encrypt(plaintext, key)
        
        results = crack_caesar(ciphertext, top_n=5)
        
        # Le meilleur résultat doit être la bonne clé
        assert results[0]['key'] == key
    
    def test_crack_top_n(self):
        """Test que le nombre de résultats est correct"""
        ciphertext = caesar_encrypt("test message", 5)
        
        results = crack_caesar(ciphertext, top_n=3)
        assert len(results) == 3
    
    def test_crack_scores_decreasing(self):
        """Test que les scores sont décroissants"""
        plaintext = "the quick brown fox jumps over the lazy dog"
        ciphertext = caesar_encrypt(plaintext, 7)
        
        results = crack_caesar(ciphertext, top_n=5)
        
        scores = [r['score'] for r in results]
        assert scores == sorted(scores, reverse=True)


class TestAutoCrackingVigenere:
    """Tests pour le cracking automatique de Vigenère"""
    
    def test_crack_short_key(self):
        """Test de cracking avec clé courte"""
        plaintext = "this is a secret message that should be cracked by analyzing the frequency of letters in the ciphertext"
        key = "KEY"
        ciphertext = vigenere_encrypt(plaintext, key)
        
        results = crack_vigenere(ciphertext, top_n=3)
        
        # La bonne clé devrait être dans les résultats
        found_keys = [r['key'] for r in results]
        assert key in found_keys
    
    def test_crack_medium_key(self):
        """Test avec clé de longueur moyenne"""
        plaintext = "in cryptography a caesar cipher also known as caesar shift cipher shift or simply caesar is one of the simplest and most widely known encryption techniques it is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet"
        key = "ESSTHS"
        ciphertext = vigenere_encrypt(plaintext, key)
        
        results = crack_vigenere(ciphertext, top_n=5)
        
        # Le meilleur résultat devrait avoir la bonne longueur de clé
        assert results[0]['key_length'] == len(key)


class TestIntegration:
    """Tests d'intégration complets"""
    
    def test_full_pipeline_caesar(self):
        """Test du pipeline complet pour César"""
        plaintext = "the art of war is of vital importance to the state"
        key = 17
        ciphertext = caesar_encrypt(plaintext, key)
        
        # Détection
        detected = detect_cipher_type(ciphertext)
        assert detected == 'caesar'
        
        # Cracking
        results = crack_caesar(ciphertext, top_n=1)
        
        # Vérification
        assert results[0]['key'] == key
        assert results[0]['plaintext'] == plaintext
    
    def test_full_pipeline_vigenere(self):
        """Test du pipeline complet pour Vigenère"""
        plaintext = "cryptography is the practice and study of techniques for secure communication in the presence of third parties called adversaries"
        key = "SECURE"
        ciphertext = vigenere_encrypt(plaintext, key)
        
        # Détection
        detected = detect_cipher_type(ciphertext)
        assert detected == 'vigenere'
        
        # Cracking
        results = crack_vigenere(ciphertext, top_n=3)
        
        # Vérification
        found_keys = [r['key'] for r in results]
        assert key in found_keys


if __name__ == '__main__':
    pytest.main([__file__, '-v'])