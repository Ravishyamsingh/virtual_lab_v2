"""
Mono-Alphabetic Cipher Implementation
This module provides the core functionality for the mono-alphabetic substitution cipher.
"""
import random
from typing import Dict, Optional, Tuple

class MonoAlphabeticCipher:
    """Implementation of the mono-alphabetic substitution cipher."""
    
    def __init__(self, key: Optional[Dict[str, str]] = None):
        """
        Initialize the cipher with an optional substitution key.
        If no key is provided, a random one will be generated.
        
        Args:
            key: Optional dictionary mapping plaintext letters to ciphertext letters
        """
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.key = key if key else self._generate_random_key()
        self.reverse_key = {v: k for k, v in self.key.items()}
    
    def _generate_random_key(self) -> Dict[str, str]:
        """Generate a random substitution key."""
        cipher_alphabet = list(self.alphabet)
        random.shuffle(cipher_alphabet)
        return dict(zip(self.alphabet, cipher_alphabet))
    
    def encrypt(self, plaintext: str) -> Tuple[str, Dict[str, int]]:
        """
        Encrypt the plaintext using the substitution cipher.
        
        Args:
            plaintext: The text to encrypt
        
        Returns:
            Tuple containing:
            - The encrypted text
            - Dictionary of character frequencies in the plaintext
        """
        plaintext = plaintext.upper()
        frequencies = {}
        ciphertext = []
        
        for char in plaintext:
            if char.isalpha():
                ciphertext.append(self.key[char])
                frequencies[char] = frequencies.get(char, 0) + 1
            else:
                ciphertext.append(char)
        
        return ''.join(ciphertext), frequencies
    
    def decrypt(self, ciphertext: str) -> Tuple[str, Dict[str, int]]:
        """
        Decrypt the ciphertext using the substitution cipher.
        
        Args:
            ciphertext: The text to decrypt
        
        Returns:
            Tuple containing:
            - The decrypted text
            - Dictionary of character frequencies in the ciphertext
        """
        ciphertext = ciphertext.upper()
        frequencies = {}
        plaintext = []
        
        for char in ciphertext:
            if char.isalpha():
                plaintext.append(self.reverse_key[char])
                frequencies[char] = frequencies.get(char, 0) + 1
            else:
                plaintext.append(char)
        
        return ''.join(plaintext), frequencies
    
    def get_substitution_table(self) -> Dict[str, str]:
        """Get the current substitution key."""
        return self.key.copy()
    
    def set_key(self, key: Dict[str, str]) -> None:
        """
        Set a new substitution key.
        
        Args:
            key: Dictionary mapping plaintext letters to ciphertext letters
        """
        if not all(k.isalpha() and v.isalpha() for k, v in key.items()):
            raise ValueError("All key mappings must be alphabetic characters")
        
        self.key = {k.upper(): v.upper() for k, v in key.items()}
        self.reverse_key = {v: k for k, v in self.key.items()}
