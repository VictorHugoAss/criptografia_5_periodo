"""
Cofre de Senhas - Aplicação prática do AES-256-CBC.
Professor, criei um script interativo que encripta textos usando a matemática AES
construída do zero. Ele gera Salt e IV aleatórios para manter a segurança.
"""

import os
import json
import base64
import hmac
import hashlib
import struct
from aes import cbc_encrypt, cbc_decrypt

# Implementação do PBKDF2 exigida nos slides da aula (no braço)
def hmac_sha256(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()

def pbkdf2_hmac_sha256(password: bytes, salt: bytes, iterations: int, dklen: int) -> bytes:
    num_blocks = -(-dklen // 32)
    dk = b''
    for block_num in range(1, num_blocks + 1):
        u = hmac_sha256(password, salt + struct.pack('>I', block_num))
        result = u
        for _ in range(iterations - 1):
            u = hmac_sha256(password, u)
            result = bytes(a ^ b for a, b in zip(result, u))
        dk += result
    return dk[:dklen]

class CofreSenhas:
    def __init__(self, senha_mestre: str):
        self.senha = senha_mestre.encode('utf-8')
    
    def trancar_mensagem(self, texto: str) -> str:
        salt = os.urandom(16)
        iv = os.urandom(16)
        
        print("\n[Trancando] Derivando chave com PBKDF2 (100.000 iterações)...")
        chave = pbkdf2_hmac_sha256(self.senha, salt, 100_000, 32)
        
        texto_cifrado = cbc_encrypt(texto.encode('utf-8'), chave, iv)
        pacote = salt + iv + texto_cifrado
        return base64.b64encode(pacote).decode('utf-8')

    def destrancar_mensagem(self, pacote_b64: str) -> str:
        dados = base64.b64decode(pacote_b64)
        salt, iv, ciphertext = dados[:16], dados[16:32], dados[32:]
        
        print("[Destrancando] Recalculando a chave...")
        chave = pbkdf2_hmac_sha256(self.senha, salt, 100_000, 32)
        
        try:
            texto_claro = cbc_decrypt(ciphertext, chave, iv)
            return texto_claro.decode('utf-8')
        except ValueError:
            return "ERRO DE SEGURANÇA: Senha Incorreta ou Dados Corrompidos."

if __name__ == "__main__":
    print("=== Cofre de Senhas Local (AES do zero) ===")
    cofre = CofreSenhas("SenhaSegura123")
    
    mensagem = "Senha do banco de dados: admin123"
    print(f"Original: {mensagem}")
    
    cifrado = cofre.trancar_mensagem(mensagem)
    print(f"Cifrado Base64:\n{cifrado}\n")
    
    decifrado = cofre.destrancar_mensagem(cifrado)
    print(f"Texto Recuperado: {decifrado}")