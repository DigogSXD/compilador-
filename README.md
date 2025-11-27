# 🔍 Analisador Léxico em Python

Este projeto implementa um **Analisador Léxico** (Scanner) simples, desenvolvido em Python. O objetivo principal é ler um código-fonte de entrada, identificar os lexemas e transformá-los em uma sequência de **Tokens**, ignorando espaços em branco e comentários, além de gerenciar uma Tabela de Símbolos.

## 📋 Funcionalidades e Requisitos Atendidos

O código foi projetado para cobrir 9 requisitos específicos de implementação:

1.  **Palavras-Chave:** Inicialização da tabela de símbolos com palavras reservadas (`se`, `entao`, `senao`, `enquanto`, `faca`, `retorne`).
2.  **Números Decimais:** Suporte para leitura de números inteiros e pontos flutuantes (floats).
3.  **Operadores Aritméticos:** Reconhecimento de `+`, `-`, `*`, `/`, `%`.
4.  **Operadores Relacionais:** Reconhecimento de `==`, `!=`, `<`, `<=`, `>`, `>=` e atribuição `=`.
5.  **Identificadores:** Reconhecimento e armazenamento de variáveis na **Tabela de Símbolos**.
6.  **Espaços em Branco:** O analisador ignora formatações (espaços, tabs, quebras de linha).
7.  **Comentários:** Suporte para dois tipos de comentários (estilo C):
    * Linha única: `// ...`
    * Múltiplas linhas (bloco): `/* ... */`
8.  **Tratamento de Erros:** Identifica caracteres inválidos e informa a linha do erro.
9.  **Recuperação de Erros:** O analisador não para no primeiro erro; ele descarta o token inválido e continua a análise.

## 🚀 Como Executar

### Pré-requisitos
* Python 3.x instalado.

### Passo a Passo
1.  Salve o código do analisador em um arquivo, por exemplo: `analisador_lexico.py`.
2.  Abra o terminal ou prompt de comando na pasta do arquivo.
3.  Execute o comando:

```bash
python analisador_lexico.py
```

### 💻 Modos de Uso
O script possui dois modos de operação que rodam sequencialmente:

### 1. Validação Automática
Ao iniciar, o script executa um código de teste pré-definido (codigo_validacao) que demonstra todos os requisitos funcionando (comentários, lógica, erros propositais, etc).

### 2. Modo Interativo
Após a validação, você pode digitar seu próprio código no terminal:

Digite as linhas de código desejadas.

Para processar, digite FIM em uma nova linha.

Para encerrar o programa, digite SAIR.

### 📂 Estrutura do Código
class Token: Representa a unidade mínima (tipo, valor e linha).

class AnalisadorLexico: O núcleo do sistema.

obter_proximo_token(): Método principal que decide qual regra aplicar baseada no caractere atual.

tabela_simbolos: Dicionário que armazena palavras-chave e identificadores encontrados.

pular_espacos_e_comentarios(): Limpa a entrada antes da tokenização.

### 📝 Exemplo de Saída
Para uma entrada como:
