
import os
from collections import Counter
import math


class TextScorer:
    """
    Classe pour scorer la qualité d'un texte déchiffré
    """
    
    def __init__(self, data_dir='data'):
        """
        Initialise le scorer avec les ressources linguistiques
        
        Args:
            data_dir (str): Répertoire contenant stopwords_en.txt et words_en.txt
        """
        self.stopwords = self._load_stopwords(data_dir)
        self.vocab = self._load_vocabulary(data_dir)
    
    def _load_stopwords(self, data_dir):
        """Charge les stopwords anglais"""
        path = os.path.join(data_dir, 'stopwords_en.txt')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return set(word.strip().lower() for word in f)
        except FileNotFoundError:
            # Fallback : stopwords de base
            return {
                'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
                'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one',
                'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
                'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when'
            }
    
    def _load_vocabulary(self, data_dir):
        """Charge le dictionnaire anglais"""
        path = os.path.join(data_dir, 'words_en.txt')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return set(word.strip().lower() for word in f)
        except FileNotFoundError:
            # Fallback : vocabulaire minimal
            return set()
    
    def score(self, text):
        """
        Calcule un score global pour un texte
        
        Combine 4 métriques:
        1. Ratio de mots valides (0-10 points)
        2. Présence de stopwords (0-5 points)
        3. Entropie des caractères (0-5 points)
        4. Bigrams communs (0-5 points)
        
        Args:
            text (str): Texte à scorer
        
        Returns:
            float: Score total (0-25)
        """
        if not text or not text.strip():
            return 0.0
        
        # Extraire les mots
        words = [w.lower() for w in text.split() if w.isalpha()]
        
        if not words:
            return 0.0
        
        # 1. Ratio de mots valides
        valid_ratio = self._score_valid_words(words)
        
        # 2. Présence de stopwords
        stopwords_score = self._score_stopwords(words)
        
        # 3. Entropie des caractères
        entropy_score = self._score_entropy(text)
        
        # 4. Bigrams communs
        bigram_score = self._score_bigrams(text)
        
        total_score = (
            valid_ratio * 10 +
            stopwords_score * 5 +
            entropy_score * 5 +
            bigram_score * 5
        )
        
        return round(total_score, 2)
    
    def _score_valid_words(self, words):
        """
        Score basé sur le ratio de mots valides dans le dictionnaire
        
        Returns:
            float: 0-1
        """
        if not self.vocab:
            # Fallback : heuristique simple
            return sum(len(w) >= 3 for w in words) / len(words)
        
        valid_count = sum(1 for w in words if w in self.vocab)
        return valid_count / len(words)
    
    def _score_stopwords(self, words):
        """
        Score basé sur la présence de stopwords
        Les stopwords sont très fréquents dans un texte clair
        
        Returns:
            float: 0-1
        """
        stopwords_count = sum(1 for w in words if w in self.stopwords)
        
        # Normaliser : on s'attend à 30-40% de stopwords
        ratio = stopwords_count / len(words)
        
        # Fonction en cloche centrée sur 0.35
        if ratio > 0.5:
            return 1.0
        elif ratio > 0.2:
            return ratio / 0.5
        else:
            return ratio / 0.2 * 0.5
    
    def _score_entropy(self, text):
        """
        Score basé sur l'entropie des caractères
        Anglais ≈ 4.1-4.5 bits/caractère
        
        Returns:
            float: 0-1
        """
        text_clean = ''.join(c.lower() for c in text if c.isalpha())
        
        if not text_clean:
            return 0.0
        
        freq = Counter(text_clean)
        n = len(text_clean)
        
        entropy = -sum((count/n) * math.log2(count/n) 
                      for count in freq.values())
        
        # Normaliser : entropie optimale autour de 4.2
        ideal_entropy = 4.2
        diff = abs(entropy - ideal_entropy)
        
        # Score diminue avec la distance à l'idéal
        score = max(0, 1 - (diff / 2))
        return score
    
    def _score_bigrams(self, text):
        """
        Score basé sur les bigrams (paires de lettres) communs
        
        Returns:
            float: 0-1
        """
        # Bigrams les plus fréquents en anglais
        common_bigrams = {
            'th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd',
            'ti', 'es', 'or', 'te', 'of', 'ed', 'is', 'it', 'al', 'ar',
            'st', 'to', 'nt', 'ng', 'se', 'ha', 'as', 'ou', 'io', 'le'
        }
        
        text_clean = ''.join(c.lower() for c in text if c.isalpha())
        
        if len(text_clean) < 2:
            return 0.0
        
        # Compter les bigrams
        bigrams = [text_clean[i:i+2] for i in range(len(text_clean)-1)]
        common_count = sum(1 for bg in bigrams if bg in common_bigrams)
        
        ratio = common_count / len(bigrams)
        return ratio


# Instance globale pour faciliter l'utilisation
_scorer = None

def score_text(text, data_dir='data'):
    """
    Fonction utilitaire pour scorer un texte
    
    Args:
        text (str): Texte à scorer
        data_dir (str): Répertoire des données
    
    Returns:
        float: Score (0-25)
    
    Exemple:
        >>> score_text("This is a valid english text")
        18.5
        >>> score_text("Xyzk zk z kzkzk")
        2.1
    """
    global _scorer
    if _scorer is None:
        _scorer = TextScorer(data_dir)
    return _scorer.score(text)