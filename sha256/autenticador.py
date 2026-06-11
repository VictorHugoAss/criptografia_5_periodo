"""
Autenticador de Documentos
Usa o SHA-256 implementado do zero (sha256.py) para garantir
que o documento não sofreu adulteração (Integridade).
"""

import sys
import os
from sha256 import sha256

def gerar_hash(caminho: str) -> str:
    """Lê um arquivo e retorna o hash SHA-256 do seu conteúdo."""
    with open(caminho, 'rb') as f:
        conteudo = f.read()
    return sha256(conteudo)

def cmd_gerar(caminho: str):
    if not os.path.exists(caminho):
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        sys.exit(1)

    h = gerar_hash(caminho)
    print(f"Arquivo: {caminho}\nSHA-256: {h}")

    hash_file = caminho + '.hash'
    with open(hash_file, 'w') as f:
        f.write(h)
    print(f"Hash salvo em: {hash_file}")

def cmd_verificar(caminho: str, hash_fornecido: str):
    if not os.path.exists(caminho):
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        sys.exit(1)

    hash_calculado = gerar_hash(caminho)
    print(f"Arquivo:        {caminho}")
    print(f"Hash esperado:  {hash_fornecido}")
    print(f"Hash calculado: {hash_calculado}")

    if hash_calculado == hash_fornecido:
        print("\n[AUTENTICO] O arquivo não foi alterado.")
    else:
        print("\n[INVALIDO] O arquivo foi modificado ou o hash está errado!")

if __name__ == '__main__':
    uso = "Uso:\n  python autenticador.py gerar <arquivo>\n  python autenticador.py verificar <arquivo> <hash>"
    if len(sys.argv) < 3:
        print(uso)
        sys.exit(1)

    comando = sys.argv[1].lower()
    if comando == 'gerar':
        cmd_gerar(sys.argv[2])
    elif comando == 'verificar':
        if len(sys.argv) < 4:
            print("Erro: informe o arquivo e o hash.")
            sys.exit(1)
        cmd_verificar(sys.argv[2], sys.argv[3])
    else:
        print(uso)