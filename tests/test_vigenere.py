"""
Tests unitaires pour le chiffrement de Vigenère
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from crypto.vigenere import encrypt, decrypt


class TestVigenereBasic:
    """Tests de base pour Vigenère"""
    
    def test_encrypt_simple(self):
        """Test de chiffrement simple"""
        plaintext = "HELLO"
        key = "KEY"
        expected = "RIJVS"
        
        result = encrypt(plaintext, key)
        assert result == expected
    
    def test_decrypt_simple(self):
        """Test de déchiffrement simple"""
        ciphertext = "RIJVS"
        key = "KEY"
        expected = "HELLO"
        
        result = decrypt(ciphertext, key)
        assert result == expected
    
    def test_encrypt_decrypt_inverse(self):
        """Test d'inversibilité"""
        plaintext = "The quick brown fox"
        key = "ESSTHS"
        
        ciphertext = encrypt(plaintext, key)
        recovered = decrypt(ciphertext, key)
        
        assert recovered == plaintext
    
    def test_key_repetition(self):
        """Test de la répétition de la clé"""
        plaintext = "AAAAAAAA"
        key = "AB"
        
        # A avec A → A (décalage 0)
        # A avec B → B (décalage 1)
        expected = "ABABABAB"
        
        result = encrypt(plaintext, key)
        assert result == expected
    
    def test_preserve_case(self):
        """Test de préservation de la casse"""
        plaintext = "HeLLo"
        key = "KEY"
        
        result = encrypt(plaintext, key)
        
        # Vérifier le pattern de casse
        assert result[0].isupper()
        assert result[1].islower()
        assert result[2].isupper()
        assert result[3].isupper()
        assert result[4].islower()
    
    def test_preserve_spaces(self):
        """Test de préservation des espaces"""
        plaintext = "HELLO WORLD"
        key = "KEY"
        
        ciphertext = encrypt(plaintext, key)
        
        # L'espace doit être préservé
        assert ' ' in ciphertext
        assert ciphertext.index(' ') == plaintext.index(' ')


class TestVigenereEdgeCases:
    """Tests de cas limites"""
    
    def test_empty_string(self):
        """Test avec chaîne vide"""
        result = encrypt("", "KEY")
        assert result == ""
    
    def test_single_char_key(self):
        """Test avec clé d'un seul caractère (équivalent César)"""
        plaintext = "HELLO"
        key = "D"  # Décalage de 3
        
        result = encrypt(plaintext, key)
        
        # Devrait être équivalent à César avec clé 3
        from crypto.caesar import encrypt as caesar_encrypt
        expected = caesar_encrypt(plaintext, 3)
        
        assert result == expected
    
    def test_invalid_key_empty(self):
        """Test avec clé vide"""
        with pytest.raises(ValueError):
            encrypt("HELLO", "")
    
    def test_invalid_key_numeric(self):
        """Test avec clé contenant des chiffres"""
        with pytest.raises(ValueError):
            encrypt("HELLO", "KEY123")
    
    def test_long_key(self):
        """Test avec clé longue"""
        plaintext = "HELLO"
        key = "VERYLONGKEY"
        
        # Ne devrait pas lever d'erreur
        result = encrypt(plaintext, key)
        assert len(result) == len(plaintext)
    
    def test_key_case_insensitive(self):
        """Test que la casse de la clé n'affecte pas le résultat"""
        plaintext = "HELLO"
        
        result1 = encrypt(plaintext, "key")
        result2 = encrypt(plaintext, "KEY")
        result3 = encrypt(plaintext, "Key")
        
        assert result1 == result2 == result3


class TestVigenereExamples:
    """Tests avec des exemples réels"""
    
    def test_wikipedia_example(self):
        """Test avec l'exemple de Wikipedia"""
        plaintext = "ATTACKATDAWN"
        key = "LEMON"
        expected = "LXFOPVEFRNHR"
        
        result = encrypt(plaintext, key)
        assert result == expected
    
    def test_course_example(self):
        """Test avec l'exemple du cours (TP2)"""
        plaintext = "iamathirdyearstudent"
        key = "ESSTHS"
        
        ciphertext = encrypt(plaintext, key)
        recovered = decrypt(ciphertext, key)
        
        assert recovered == plaintext


if __name__ == '__main__':
    pytest.main([__file__, '-v'])