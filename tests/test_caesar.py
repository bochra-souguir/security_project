"""
Tests unitaires pour le chiffrement de César
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from crypto.caesar import encrypt, decrypt, bruteforce


class TestCaesarBasic:
    """Tests de base pour César"""
    
    def test_encrypt_simple(self):
        """Test de chiffrement simple"""
        plaintext = "HELLO"
        key = 3
        expected = "KHOOR"
        
        result = encrypt(plaintext, key)
        assert result == expected
    
    def test_decrypt_simple(self):
        """Test de déchiffrement simple"""
        ciphertext = "KHOOR"
        key = 3
        expected = "HELLO"
        
        result = decrypt(ciphertext, key)
        assert result == expected
    
    def test_encrypt_decrypt_inverse(self):
        """Test d'inversibilité"""
        plaintext = "The quick brown fox jumps over the lazy dog"
        key = 13
        
        ciphertext = encrypt(plaintext, key)
        recovered = decrypt(ciphertext, key)
        
        assert recovered == plaintext
    
    def test_preserve_case(self):
        """Test de préservation de la casse"""
        plaintext = "HeLLo WoRLd"
        key = 5
        
        result = encrypt(plaintext, key)
        
        # Vérifier que les majuscules restent majuscules
        assert result[0].isupper()
        assert result[2].isupper()
        assert result[3].isupper()
        
        # Vérifier que les minuscules restent minuscules
        assert result[1].islower()
        assert result[4].islower()
    
    def test_preserve_punctuation(self):
        """Test de préservation de la ponctuation"""
        plaintext = "Hello, World! How are you?"
        key = 7
        
        ciphertext = encrypt(plaintext, key)
        
        # La ponctuation doit être inchangée
        assert ',' in ciphertext
        assert '!' in ciphertext
        assert '?' in ciphertext
        assert ' ' in ciphertext
    
    def test_empty_string(self):
        """Test avec chaîne vide"""
        result = encrypt("", 5)
        assert result == ""
    
    def test_key_wraparound(self):
        """Test du bouclage de l'alphabet"""
        # Z avec clé 1 devrait donner A
        assert encrypt("Z", 1) == "A"
        assert encrypt("z", 1) == "a"
        
        # A avec clé -1 devrait donner Z
        assert encrypt("A", -1) == "Z"
        assert encrypt("a", -1) == "z"


class TestCaesarBruteforce:
    """Tests pour le bruteforce"""
    
    def test_bruteforce_count(self):
        """Test du nombre de candidats générés"""
        ciphertext = "KHOOR"
        candidates = bruteforce(ciphertext)
        
        assert len(candidates) == 25
    
    def test_bruteforce_contains_solution(self):
        """Test que le bruteforce contient la bonne solution"""
        plaintext = "SECRET MESSAGE"
        key = 17
        ciphertext = encrypt(plaintext, key)
        
        candidates = bruteforce(ciphertext)
        plaintexts = [pt for k, pt in candidates]
        
        assert plaintext in plaintexts


class TestCaesarEdgeCases:
    """Tests de cas limites"""
    
    def test_key_boundaries(self):
        """Test des clés aux limites"""
        plaintext = "ABC"
        
        # Clé 1
        assert encrypt(plaintext, 1) == "BCD"
        
        # Clé 25 (équivalent à -1)
        assert encrypt(plaintext, 25) == "ZAB"
    
    def test_invalid_key_type(self):
        """Test avec type de clé invalide"""
        with pytest.raises(ValueError):
            encrypt("HELLO", "not_a_number")
    
    def test_invalid_key_range(self):
        """Test avec clé hors limites"""
        with pytest.raises(ValueError):
            encrypt("HELLO", 0)
        
        with pytest.raises(ValueError):
            encrypt("HELLO", 26)
    
    def test_numbers_preserved(self):
        """Test que les chiffres sont préservés"""
        plaintext = "Test123"
        ciphertext = encrypt(plaintext, 5)
        
        assert "123" in ciphertext


if __name__ == '__main__':
    pytest.main([__file__, '-v'])