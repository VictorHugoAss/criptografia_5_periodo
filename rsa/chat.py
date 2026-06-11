"""
Simulador de Troca de Chaves.
Professor, aqui eu utilizo as funções construídas em rsa.py para 
demonstrar que a Alice só consegue mandar mensagem para o Bob usando
a Chave Pública dele, e só ele consegue abrir com a Privada.
"""

from rsa import gerar_chaves, cifrar, decifrar

def simulador_comunicacao():
    print("=== Iniciando Simulador RSA (Algoritmo Próprio) ===")
    
    print("\n1. Gerando par de chaves para Bob (512 bits)...")
    chave_pub_bob, chave_priv_bob = gerar_chaves(512)
    print(f"Chave Pública do Bob (n, e):\n {chave_pub_bob}")
    
    print("\n2. Alice quer enviar uma mensagem para Bob.")
    mensagem = "Oi Bob, o algoritmo RSA esta funcionando perfeitamente!"
    print(f"Mensagem da Alice: '{mensagem}'")
    
    print("\n3. Alice usa a Chave Pública do Bob para trancar a mensagem.")
    cifrado_bytes = cifrar(mensagem.encode('utf-8'), chave_pub_bob)
    print(f"Tráfego de rede (interceptado):\n {cifrado_bytes[:5]}... (array de inteiros)")
    
    print("\n4. Bob recebe a mensagem e a destranca usando sua Chave Privada.")
    recuperado_bytes = decifrar(cifrado_bytes, chave_priv_bob)
    print(f"Bob leu: '{recuperado_bytes.decode('utf-8')}'")

if __name__ == "__main__":
    simulador_comunicacao()