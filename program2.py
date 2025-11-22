class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}', Linha: {self.linha})"

# --- CLASSE ANALISADOR LÉXICO ---
class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.posicao = 0
        self.linha = 1
        self.char_atual = self.codigo[self.posicao] if self.posicao < len(self.codigo) else None
        
        # 1. REQUISITO: Inicializar a tabela de símbolos com mais de uma palavra-chave
        self.tabela_simbolos = {
            'se': Token('PALAVRA_CHAVE', 'se', 0),
            'entao': Token('PALAVRA_CHAVE', 'entao', 0),
            'senao': Token('PALAVRA_CHAVE', 'senao', 0),
            'enquanto': Token('PALAVRA_CHAVE', 'enquanto', 0),
            'faca': Token('PALAVRA_CHAVE', 'faca', 0),
            'retorne': Token('PALAVRA_CHAVE', 'retorne', 0),
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
            # 6. REQUISITO: Remover espaços em branco
            if self.char_atual.isspace():
                self.avancar()
                continue
            
            # 7. REQUISITO: Remover os dois tipos de comentários (// e /* */)
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
        
        # 2. REQUISITO: Reconhecer números decimais
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
        
        # Verifica se é palavra-chave já existente
        token = self.tabela_simbolos.get(resultado, None)
        if token:
            return Token(token.tipo, token.valor, self.linha)
        
        # 5. REQUISITO: Reconhecer identificadores e armazená-los na tabela
        token = Token('IDENTIFICADOR', resultado, self.linha)
        self.tabela_simbolos[resultado] = token
        return token

    def obter_proximo_token(self):
        while self.char_atual is not None:
            self.pular_espacos_e_comentarios()

            if self.char_atual is None:
                break

            if self.char_atual.isdigit():
                return self.extrair_numero()
            
            if self.char_atual.isalpha() or self.char_atual == '_':
                return self.extrair_identificador()

            # 3. REQUISITO: Reconhecer os quatro operadores aritméticos
            if self.char_atual == '+':
                self.avancar()
                return Token('OP_ARITMETICO', '+', self.linha)
            if self.char_atual == '-':
                self.avancar()
                return Token('OP_ARITMETICO', '-', self.linha)
            if self.char_atual == '*':
                self.avancar()
                return Token('OP_ARITMETICO', '*', self.linha)
            if self.char_atual == '/':
                self.avancar()
                return Token('OP_ARITMETICO', '/', self.linha)
            if self.char_atual == '%':
                self.avancar()
                return Token('OP_ARITMETICO', '%', self.linha)

            # 4. REQUISITO: Reconhecer operadores relacionais
            if self.char_atual == '=':
                if self.peek() == '=':
                    self.avancar(); self.avancar()
                    return Token('OP_RELACIONAL', '==', self.linha)
                else:
                    self.avancar()
                    return Token('ATRIBUICAO', '=', self.linha)
            
            if self.char_atual == '!':
                if self.peek() == '=':
                    self.avancar(); self.avancar()
                    return Token('OP_RELACIONAL', '!=', self.linha)
            
            if self.char_atual == '<':
                self.avancar()
                if self.char_atual == '=':
                    self.avancar()
                    return Token('OP_RELACIONAL', '<=', self.linha)
                return Token('OP_RELACIONAL', '<', self.linha)
            
            if self.char_atual == '>':
                self.avancar()
                if self.char_atual == '=':
                    self.avancar()
                    return Token('OP_RELACIONAL', '>=', self.linha)
                return Token('OP_RELACIONAL', '>', self.linha)

            # Símbolos extras (parênteses, ponto e vírgula)
            if self.char_atual == '(':
                self.avancar()
                return Token('PARENTESE_ESQ', '(', self.linha)
            if self.char_atual == ')':
                self.avancar()
                return Token('PARENTESE_DIR', ')', self.linha)
            if self.char_atual == ';':
                self.avancar()
                return Token('PONTO_VIRGULA', ';', self.linha)
            
            # 8. e 9. REQUISITOS: Tratar erros (imprimir linha) e Recuperar erro (continuar)
            char_invalido = self.char_atual
            linha_erro = self.linha
            self.avancar() # Recuperação: Ignora o char e vai pro próximo
            print(f"ERRO LÉXICO: Caractere inválido '{char_invalido}' detectado na linha {linha_erro}.")
            continue # Reinicia o loop para pegar o próximo token válido

        return Token('FIM_DE_ARQUIVO', None, self.linha)


# --- ÁREA DE TESTE E VALIDAÇÃO ---
if __name__ == "__main__":
    
    # Este código fonte cobre TODOS os 9 requisitos do professor
    codigo_validacao = """
    /* TESTE DE REQUISITOS 
       Comentario de bloco (Req 7) 
    */
    
    // Declaracao de variaveis (Req 5 e 6)
    media_final = 0.0;
    
    se (nota1 >= 7.5) entao // (Req 1, 4 e 2)
        contador = contador + 1; // (Req 3)
    senao
        // Teste de ERRO e RECUPERACAO (Req 8 e 9)
        // O caractere '@' e invalido, mas o codigo deve ler o '100' depois dele
        valor_invalido = 10 @ 100;
        
    faca calculo_final;
    """

    print("="*50)
    print("INICIANDO VALIDAÇÃO COMPLETA DOS REQUISITOS")
    print("="*50)
    
    analisador = AnalisadorLexico(codigo_validacao)
    
    while True:
        token = analisador.obter_proximo_token()
        
        # Se for fim de arquivo, para
        if token.tipo == 'FIM_DE_ARQUIVO':
            break
            
        print(token)

    print("\n" + "="*50)
    print("VERIFICAÇÃO DA TABELA DE SÍMBOLOS (Requisito 5)")
    print("Identificadores encontrados devem estar listados abaixo:")
    print("-" * 50)
    for chave, valor in analisador.tabela_simbolos.items():
        if valor.tipo == 'IDENTIFICADOR':
            print(f" [NOVO ID] '{chave}' armazenado na tabela.")
        elif valor.tipo == 'PALAVRA_CHAVE':
             pass # Não precisa imprimir as palavras chaves padrão para não poluir
             
    print("\n" + "="*50)
    print("TESTE INTERATIVO (Para você digitar seu código)")
    print("Digite 'FIM' numa nova linha para processar ou 'SAIR' para fechar")
    print("-" * 50)

    # Loop interativo corrigido para funcionar no terminal
    while True:
        linhas = []
        while True:
            try:
                linha = input()
                if linha.strip().upper() == 'FIM':
                    break
                if linha.strip().lower() == 'sair':
                    exit()
                linhas.append(linha)
            except EOFError:
                break
        
        if not linhas: continue
        
        codigo_user = "\n".join(linhas)
        analisador_interativo = AnalisadorLexico(codigo_user)
        
        print("\n--- Tokens Identificados ---")
        while True:
            t = analisador_interativo.obter_proximo_token()
            if t.tipo == 'FIM_DE_ARQUIVO':
                break
            print(t)
        print("-" * 30 + "\n")
