def exemplo(condicao):
    if condicao:
        resultado1 = 10 + 20
        resultado2 = "teste" + "abc"
        return resultado1, resultado2
    else:
        resultado3 = 30 - 15
        resultado4 = "outro" + " valor"
        return resultado3, resultado4

resultado1, resultado2 = exemplo(True)
print(resultado1)  # Saída: 30
print(resultado2)  # Saída: testeabc

