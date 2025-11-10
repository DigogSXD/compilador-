def infix_para_posfixa(expressao):
    # Define a precedência dos operadores. Maior número = maior precedência.
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2}

    # Pilha para os operadores
    pilha_operadores = []
    # Lista para a saída pós-fixa
    saida_posfixa = []
    # Variável temporária para construir números com mais de um dígito
    numero_atual = ''

    # Adicionamos parênteses no início e fim para garantir que todos os operadores sejam desempilhados
    expressao_formatada = f"({expressao})"

    for caractere in expressao_formatada:
        # 1. Verifica se o caractere é um dígito
        if caractere.isdigit():
            numero_atual += caractere
            continue # Continua para o próximo caractere para formar o número completo

        # Se chegamos aqui, o número atual (se houver) terminou.
        if numero_atual:
            saida_posfixa.append(numero_atual)
            numero_atual = ''

        # 2. Verifica se o caractere é um operador aritmético
        if caractere in precedencia:
            # Enquanto houver operadores na pilha com precedência maior ou igual
            # ao operador atual, desempilhe-os para a saída.
            while (pilha_operadores and pilha_operadores[-1] in precedencia and
                   precedencia[pilha_operadores[-1]] >= precedencia[caractere]):
                saida_posfixa.append(pilha_operadores.pop())
            # Empilha o operador atual
            pilha_operadores.append(caractere)

        # 3. Verifica se é um parêntese de abertura
        elif caractere == '(':
            pilha_operadores.append(caractere)

        # 4. Verifica se é um parêntese de fechamento
        elif caractere == ')':
            # Desempilha operadores para a saída até encontrar o '('
            while pilha_operadores and pilha_operadores[-1] != '(':
                saida_posfixa.append(pilha_operadores.pop())
            # Remove o '(' da pilha
            if pilha_operadores and pilha_operadores[-1] == '(':
                pilha_operadores.pop()

        # 5. Ignora espaços em branco
        elif caractere.isspace():
            continue

        # Tratamento de erro simples para caracteres inválidos
        else:
            if caractere: 
                print(f"Aviso: Caractere '{caractere}' inválido e foi ignorado.")


    # Após percorrer toda a expressão, desempilha os operadores restantes
    while pilha_operadores:
        saida_posfixa.append(pilha_operadores.pop())

    # Retorna a expressão pós-fixa como uma string com espaços
    return ' '.join(saida_posfixa)

# --- Área de Testes ---
if __name__ == "__main__":
    # Exemplos de expressões para teste
    expressao1 = "3 + 4 * 2"
    expressao2 = "(3 + 4) * 2"
    # Expressão com números de mais de um dígito 
    expressao3 = "10 + 3 * 5 / (16 - 4)"
    expressao4 = "20 - 5 * 2 + 8 / 4"

    # Executa a conversão e imprime os resultados
    print("--- EXEMPLOS FIXOS ---")
    resultado1 = infix_para_posfixa(expressao1)
    print(f"Expressão Infixa: {expressao1}")
    print(f"Expressão Pós-fixa: {resultado1}")
    print("-" * 20)

    resultado2 = infix_para_posfixa(expressao2)
    print(f"Expressão Infixa: {expressao2}")
    print(f"Expressão Pós-fixa: {resultado2}")
    print("-" * 20)

    resultado3 = infix_para_posfixa(expressao3)
    print(f"Expressão Infixa: {expressao3}")
    print(f"Expressão Pós-fixa: {resultado3}")
    print("-" * 20)

    resultado4 = infix_para_posfixa(expressao4)
    print(f"Expressão Infixa: {expressao4}")
    print(f"Expressão Pós-fixa: {resultado4}")
    print("-" * 20)

    # --- NOVA SEÇÃO INTERATIVA ---
    print("\n--- TESTE INTERATIVO (AVALIAÇÃO) ---")
    while True:
        # Pede ao usuário para digitar a expressão
        expressao_usuario = input("Digite a expressão infixa (ou 'sair' para terminar): ")

        # Condição para sair do loop
        if expressao_usuario.lower() == 'sair':
            print("Programa encerrado.")
            break
        
        # Garante que a entrada não está vazia
        if not expressao_usuario.strip():
            continue

        # Chama a função e imprime o resultado
        resultado_usuario = infix_para_posfixa(expressao_usuario)
        print(f"  > Expressão Infixa: {expressao_usuario}")
        print(f"  > Expressão Pós-fixa: {resultado_usuario}\n")