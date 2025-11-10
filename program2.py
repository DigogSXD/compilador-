class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}', Linha: {self.linha})"

# Classe principal do Analisador Léxico
class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.posicao = 0
        self.linha = 1
        self.char_atual = self.codigo[self.posicao] if self.posicao < len(self.codigo) else None
        
        # Requisito: Inicializar a tabela de símbolos com palavras-chave
        self.tabela_simbolos = {
            'se': Token('PALAVRA_CHAVE', 'se', 0),
            'entao': Token('PALAVRA_CHAVE', 'entao', 0),
            'senao': Token('PALAVRA_CHAVE', 'senao', 0),
            'enquanto': Token('PALAVRA_CHAVE', 'enquanto', 0),
            'faca': Token('PALAVRA_CHAVE', 'faca', 0),
        }

    def avancar(self):
        """Avança o ponteiro de posição no código fonte."""
        if self.char_atual == '\n':
            self.linha += 1
        
        self.posicao += 1
        if self.posicao < len(self.codigo):
            self.char_atual = self.codigo[self.posicao]
        else:
            self.char_atual = None

    def peek(self):
        """Olha o próximo caractere sem avançar a posição."""
        prox_pos = self.posicao + 1
        if prox_pos < len(self.codigo):
            return self.codigo[prox_pos]
        return None

    def pular_espacos_e_comentarios(self):
        """Pula espaços em branco e os dois tipos de comentários de C."""
        while self.char_atual is not None:
            # Requisito: Remover espaços em branco
            if self.char_atual.isspace():
                self.avancar()
                continue
            
            # Requisito: Remover os dois tipos de comentários da linguagem "C"
            if self.char_atual == '/':
                if self.peek() == '/': # Comentário de linha única: //
                    while self.char_atual is not None and self.char_atual != '\n':
                        self.avancar()
                    continue
                elif self.peek() == '*': # Comentário de múltiplas linhas: /* ... */
                    self.avancar() # Pula o '/'
                    self.avancar() # Pula o '*'
                    while self.char_atual is not None:
                        if self.char_atual == '*' and self.peek() == '/':
                            self.avancar() # Pula o '*'
                            self.avancar() # Pula o '/'
                            break
                        self.avancar()
                    continue
            
            break # Sai do loop se não for espaço nem comentário

    def extrair_numero(self):
        """Extrai um número inteiro ou decimal (float) do código."""
        resultado = ''
        while self.char_atual is not None and self.char_atual.isdigit():
            resultado += self.char_atual
            self.avancar()
        
        # Requisito: Reconhecer números decimais
        if self.char_atual == '.':
            resultado += '.'
            self.avancar()
            while self.char_atual is not None and self.char_atual.isdigit():
                resultado += self.char_atual
                self.avancar()
        
        return Token('NUMERO', float(resultado), self.linha)

    def extrair_identificador(self):
        """Extrai um identificador ou palavra-chave."""
        resultado = ''
        while self.char_atual is not None and (self.char_atual.isalnum() or self.char_atual == '_'):
            resultado += self.char_atual
            self.avancar()
        
        # Verifica se é uma palavra-chave
        token = self.tabela_simbolos.get(resultado, None)
        if token:
            return Token(token.tipo, token.valor, self.linha)
        
        # Requisito: Reconhecer identificadores e armazená-los na tabela de símbolos
        token = Token('IDENTIFICADOR', resultado, self.linha)
        self.tabela_simbolos[resultado] = token
        return token

    def obter_proximo_token(self):
        """Retorna o próximo token do código fonte."""
        while self.char_atual is not None:
            self.pular_espacos_e_comentarios()

            if self.char_atual is None:
                break

            if self.char_atual.isdigit():
                return self.extrair_numero()
            
            if self.char_atual.isalpha() or self.char_atual == '_':
                return self.extrair_identificador()

            # --- OPERADORES ARITMÉTICOS ---
            if self.char_atual == '+':
                self.avancar()
                return Token('OPERADOR_ARITMETICO', '+', self.linha)
            if self.char_atual == '-':
                self.avancar()
                return Token('OPERADOR_ARITMETICO', '-', self.linha)
            if self.char_atual == '*':
                self.avancar()
                return Token('OPERADOR_ARITMETICO', '*', self.linha)
            if self.char_atual == '/':
                self.avancar()
                return Token('OPERADOR_ARITMETICO', '/', self.linha)
            
            # --- NOVO TOKEN: MÓDULO (%) ---
            if self.char_atual == '%':
                self.avancar()
                return Token('OPERADOR_ARITMETICO', '%', self.linha)

            # --- OPERADORES RELACIONAIS E DE ATRIBUIÇÃO ---
            
            # --- MODIFICADO: Reconhece '=' (Atribuição) e '==' (Relacional) ---
            if self.char_atual == '=':
                if self.peek() == '=':
                    self.avancar()
                    self.avancar()
                    return Token('OPERADOR_RELACIONAL', '==', self.linha)
                else:
                    self.avancar()
                    return Token('ATRIBUICAO', '=', self.linha) # Novo token de Atribuição
            
            if self.char_atual == '!' and self.peek() == '=':
                self.avancar()
                self.avancar()
                return Token('OPERADOR_RELACIONAL', '!=', self.linha)
            if self.char_atual == '<':
                self.avancar()
                if self.char_atual == '=':
                    self.avancar()
                    return Token('OPERADOR_RELACIONAL', '<=', self.linha)
                return Token('OPERADOR_RELACIONAL', '<', self.linha)
            if self.char_atual == '>':
                self.avancar()
                if self.char_atual == '=':
                    self.avancar()
                    return Token('OPERADOR_RELACIONAL', '>=', self.linha)
                return Token('OPERADOR_RELACIONAL', '>', self.linha)

            # --- NOVOS TOKENS: PARÊNTESES ---
            if self.char_atual == '(':
                self.avancar()
                return Token('PARENTESE_ESQ', '(', self.linha)
            if self.char_atual == ')':
                self.avancar()
                return Token('PARENTESE_DIR', ')', self.linha)

            # --- DELIMITADOR ---
            if self.char_atual == ';':
                self.avancar()
                return Token('FIM_DE_LINHA', ';', self.linha)
            
            # --- TRATAMENTO DE ERRO ---
            # Se chegou até aqui, o caractere é inválido
            char_invalido = self.char_atual
            linha_erro = self.linha
            self.avancar() # Ignora o caractere inválido e continua a análise
            print(f"ERRO: Caractere inesperado '{char_invalido}' na linha {linha_erro}.")

        return Token('FIM_DE_ARQUIVO', None, self.linha)

# --- Área de Testes (MODIFICADA) ---
if __name__ == "__main__":
    
    # --- 1. ANÁLISE DO EXEMPLO FIXO ---
    # Este exemplo agora está (quase) sintaticamente correto
    # O único erro esperado é o '#' e o '@'
    codigo_exemplo = """
    // Exemplo atualizado para testar os novos tokens
    
    variavel_x = 10.5;
    
    se (variavel_x > 10) entao
        resto = variavel_x % 2;
    senao
        variavel_x = 0;
        
    // Teste de erro
    total = 100 # 5; @
    """

    print("--- 1. ANÁLISE DO EXEMPLO FIXO ---")
    
    analisador_fixo = AnalisadorLexico(codigo_exemplo)

    while True:
        token = analisador_fixo.obter_proximo_token()
        print(token)
        if token.tipo == 'FIM_DE_ARQUIVO':
            break
            
    print("\n--- TABELA DE SÍMBOLOS (EXEMPLO FIXO) ---")
    for simbolo, token_info in analisador_fixo.tabela_simbolos.items():
        print(f"'{simbolo}': {token_info.tipo}")


    # --- 2. NOVA SEÇÃO INTERATIVA ---
    print("\n" + "="*40)
    print("--- 2. TESTE INTERATIVO (AVALIAÇÃO) ---")
    print("Digite o código para analisar (ou 'sair' para terminar):")

    while True:
        try:
            # Pede ao usuário para digitar o código
            codigo_usuario = input("\n>>> ")

            # Condição para sair do loop
            if codigo_usuario.lower() == 'sair':
                print("Programa encerrado.")
                break
            
            # Garante que a entrada não está vazia
            if not codigo_usuario.strip():
                continue

            print(f"--- Analisando: '{codigo_usuario}' ---")
            
            # Cria um NOVO analisador para cada entrada do usuário
            analisador_interativo = AnalisadorLexico(codigo_usuario)
            
            tokens_encontrados = []
            # Loop para obter todos os tokens da entrada
            while True:
                token = analisador_interativo.obter_proximo_token()
                tokens_encontrados.append(str(token))
                if token.tipo == 'FIM_DE_ARQUIVO':
                    break
            
            print("Tokens:")
            for t in tokens_encontrados:
                print(f"    {t}")
                
            print("\nNovos Identificadores na Tabela de Símbolos:")
            # Mostra apenas os novos identificadores adicionados
            novos_identificadores = 0
            for simbolo, token_info in analisador_interativo.tabela_simbolos.items():
                if token_info.tipo == 'IDENTIFICADOR':
                    print(f"    '{simbolo}': {token_info.tipo}")
                    novos_identificadores += 1
            
            if novos_identificadores == 0:
                print("    (Nenhum novo identificador adicionado)")

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
