"""
Motor RSA implementado do zero.
Professor, implementei o teste de primalidade de Miller-Rabin e o 
Algoritmo Euclidiano Estendido para calcular o expoente privado 'd'.
"""

import random

def mdc(a: int, b: int) -> int:
    while b: a, b = b, a % b
    return a

def inverso_modular(e: int, phi: int) -> int:
    phi0, x0, x1 = phi, 0, 1
    if phi == 1: return 0
    while e > 1:
        q = e // phi
        phi, e = e % phi, phi
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += phi0
    return x1

def eh_primo(n: int, k: int = 20) -> bool:
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def gerar_primo(bits: int) -> int:
    while True:
        n = random.getrandbits(bits) | (1 << bits - 1) | 1
        if eh_primo(n): return n

def gerar_chaves(bits: int = 512):
    p = gerar_primo(bits)
    q = gerar_primo(bits)
    while q == p: q = gerar_primo(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if mdc(e, phi) != 1:
        e = 3
        while mdc(e, phi) != 1: e += 2
        
    d = inverso_modular(e, phi)
    return (n, e), (n, d)

def cifrar(mensagem: bytes, chave_publica: tuple) -> list:
    n, e = chave_publica
    return [pow(byte, e, n) for byte in mensagem]

def decifrar(cifrado: list, chave_privada: tuple) -> bytes:
    n, d = chave_privada
    return bytes([pow(c, d, n) for c in cifrado])