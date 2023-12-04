# Define a função para criar uma pilha vazia
def cria_pilha():
    return {}

# Define a função para criar um bloco na pilha ou atualizar o valor de uma variável no bloco existente
def cria_bloco(pilha, tk_identificador, tk_lexema, tipo, valor):
    # Verifica se o identificador do bloco já existe na pilha, caso não existir, cria um novo bloco vazio
    if tk_identificador not in pilha:
        pilha[tk_identificador] = {}
    # Adiciona ou atualiza a variável no bloco identificado pelo tk_identificador
    pilha[tk_identificador][tk_lexema] = {'valor': valor, 'tipo': tipo, 'tk_lexema': tk_lexema}

# Define a função para remover um bloco da pilha
def remove_bloco(pilha, tk_identificador):
    # Remove e retorna o bloco identificado por 'tk_identificador'
    return pilha.pop(tk_identificador, None)

# Define a função para imprimir o valor de uma variável na pilha
def str_pilha(pilha, tk_identificador, lexema):
    if tk_identificador is not None and lexema is not None:
        tk_pilha = pilha.get(tk_identificador, {})
        if lexema in tk_pilha:
            return str(tk_pilha[lexema]['valor'])
        else:
            # Procura a variável nos blocos anteriores, se necessário
            for id_pilha in reversed(list(pilha.keys())):
                if id_pilha == tk_identificador:
                    continue
                pilha_ant = pilha.get(id_pilha, {})
                if lexema in pilha_ant:
                    return str(pilha_ant[lexema]['valor'])
            # Imprime uma mensagem de erro se a variável não for encontrada
            print(f"-------- ERRO: variável {lexema} não declarada. ")

# Define a função principal para processar o exemplo
def exemplo(exemplo, pilha):
    pilhaAtual = None
    pilhaL = []

    for linha in exemplo:
        tokens = linha.split()

        if not tokens:
            continue

        if tokens[0] == "BLOCO":
            # Inicia um novo bloco na pilha
            pilhaAtual = tokens[1]
            pilhaL.append(pilhaAtual)
        elif tokens[0] == 'NUMERO' or tokens[0] == 'CADEIA':
            # Processa a declaração de variáveis do tipo numero ou cadeia
            if len(tokens) == 2:
                tk_lexema = tokens[1]
                if '=' in tk_lexema:
                    tk_lexema, valor = tk_lexema.split('=')
                    tipo = tokens[0]
                    cria_bloco(pilha, pilhaAtual, tk_lexema, tipo, valor)
                else:
                    tipo = tokens[0]
                    valor = None
                    cria_bloco(pilha, pilhaAtual, tk_lexema, tipo, valor)
            else:
                # Processa a declaração de variáveis com varios lexemas ou valores
                if len(tokens) > 4:
                    tipo = tokens[0]
                    atual_l = None

                    for tk_token in tokens:
                        tk_token = tk_token.replace(",", "")
                        if tk_token == '=':
                            continue
                        elif tk_token.isalpha():
                            atual_l = tk_token
                        elif tk_token.isdigit():
                            valor_atual = tk_token
                            cria_bloco(pilha, pilhaAtual, atual_l, tipo, valor_atual)
                            atual_l = None
                        else:
                            cria_bloco(pilha, pilhaAtual, tk_token, tipo, None)

                    if atual_l is not None:
                        cria_bloco(pilha, pilhaAtual, atual_l, tipo, None)
                else:
                    # Processa a declaração de variáveis com lexemas e valores intercalados
                    tipo = tokens[0]
                    tokens_temp = []
                    lex_aux = 1
                    valor_aux = 2

                    for tk_token in tokens:
                        atualiza_token = []
                        atualiza_token.extend(tk_token.split('='))
                      # Filtra elementos vazios na lista 'atualiza_token'
                        atualiza_token = [elem for elem in atualiza_token if elem]
                      
                        if atualiza_token:
                            tokens_temp.extend(atualiza_token)
                        # Verifica se 'atualiza_token' contém elementos
                            if len(tokens_temp) >= 3:
                                indice_lex = lex_aux
                                valor_index = valor_aux
                        # Obtém lexema e valor da lista 'tokens_temp' com base nos índices calculados
                                tk_lexema = tokens_temp[indice_lex] if indice_lex < len(tokens_temp) else None
                                valor = tokens_temp[valor_index].replace(",", "") if valor_index < len(tokens_temp) else None

                                lex_aux += 2
                                valor_aux += 2

                                cria_bloco(pilha, pilhaAtual, tk_lexema, tipo, valor)
        elif tokens[0] == 'PRINT':
            # Processa a instrução de impressão
            tk_lexema = tokens[1]
            print(f"-> {str_pilha(pilha, pilhaAtual, tk_lexema)}")
        elif tokens[0] == "FIM":
            # Remove o bloco atual da pilha
            pilhaAtual = tokens[1]
            remove_bloco(pilha, pilhaAtual)
            if len(pilhaL) != 0:
                pilhaL.pop()
                pilhaAtual = pilhaL[-1] if pilhaL else None
            else:
                pilhaAtual = None
        else:
            # Processa atribuições e expressões
            valor_esperado = []
            aux = []
          # Itera sobre cada token presente na lista 'tokens
            for tk_token in tokens:
                if '=' in tk_token:
                    aux.extend(tk_token.split('='))
                elif tk_token.startswith('“'):
                    aux.append(tk_token[1:])
                elif tk_token.endswith('“'):
                    aux[-1] += ' ' + tk_token[:-1]
                elif tk_token.replace('.', '').isdigit():
                    aux.append(tk_token)
                else:
                    aux.append(tk_token)
# Cria uma nova lista 'lista' contendo os elementos não vazios de 'aux'
            lista = [tk_token for tk_token in aux if tk_token != '']
            valor_esperado = lista

            if valor_esperado:
                tk_lexema = valor_esperado[0]
                if len(valor_esperado) > 1 and valor_esperado[1] in pilha.get(pilhaAtual, {}):
                    # Processa atribuições entre variáveis
                    if valor_esperado[0] in pilha.get(pilhaAtual, {}) and valor_esperado[1] in pilha.get(pilhaAtual, {}):
                        if pilha[pilhaAtual][valor_esperado[0]]['tipo'] == pilha[pilhaAtual][valor_esperado[1]]['tipo']:
                            valorAtual = pilha[pilhaAtual][valor_esperado[1]]['valor']
                            cria_bloco(pilha, pilhaAtual, tk_lexema, pilha[pilhaAtual][valor_esperado[1]]['tipo'], valorAtual)
                        else:
                            print(f"-------- ERRO: Não é permitido atribuições entre variaveis. ")
                    else:
                        pilha_aux = []

                        for token in tokens:
                            if token == '=':
                                continue
                            elif '=' in token:
                                token = token.split('=')
                                pilha_aux.extend(token)
                            else:
                                pilha_aux.append(token)

                        ref_lex = pilha_aux[1]
                      # Itera sobre os identificadores da pilha em ordem reversa
                        for id_pilha in reversed(list(pilha.keys())):
                        # Se a referência de lexema estiver presente no bloco atual da pilha, obtém o valor existente e o tipo
                            if ref_lex in pilha[id_pilha]:
                                valorAtual = pilha[id_pilha][ref_lex]['valor']
                                tipo_existente = pilha[id_pilha][ref_lex]['tipo']
                                break
                       # Se o valor existir, cria um novo bloco com o identificador atual, o lexema da referência e o valor existente
                        if valorAtual is not None:
                            cria_bloco(pilha, pilhaAtual, pilha_aux[0], tipo_existente, valorAtual)
                        else:
                            print(f"ERRO: '{ref_lex}' nao é possivel encontrar ")
                else:
                    # Processa atribuições e expressões simples.
                    valor = ' '.join(map(str, valor_esperado[1:])).replace('“', '').replace('”', '')
                    tipo = tipo_lex(valor)
                  # Verifica se o bloco atual ('pilhaAtual') existe na pilha e se a variável ('tk_lexema') já foi declarada nesse bloco
                    if pilhaAtual in pilha and tk_lexema in pilha[pilhaAtual]:
                        if pilha[pilhaAtual][tk_lexema]['tipo'] == tipo:
                            valorAtual = pilha[pilhaAtual][tk_lexema]['valor']
                            if valor != valorAtual:
                                pilha[pilhaAtual][tk_lexema]['valor'] = valor
                        else:
                            print("Valor atribuido é diferente")
                    else:
                      # Se o bloco ou a variável ainda não existem, ou se os tipos são incompatíveis, cria um novo bloco na pilha
                      # Se o valor é uma string e não está entre aspas duplas, adiciona as aspas para representar uma cadeia
                        if '"' not in valor and '”' not in valor and tipo == 'CADEIA':
                            valor = "”" + valor + "”"
                        cria_bloco(pilha, pilhaAtual, tk_lexema, tipo, valor)

# Define a função para determinar o tipo de lexema (NUMERO ou CADEIA)
def tipo_lex(tk_lexema):
    try:
        float(tk_lexema)
        return 'NUMERO'
    except ValueError:
        return 'CADEIA'

# Função principal para ler o exemplo de um arquivo e executar o código
def main():
    exemplo_exemplo = []
    arq = 'exemplo.txt'

    # Lê o exemplo do arquivo e armazena em uma lista
    with open(arq, 'r') as arquivo:
        for linha in arquivo:
            exemplo_exemplo.append(linha.strip())

    pilha = cria_pilha()
    exemplo(exemplo_exemplo, pilha)

# Executa a função principal se este script for executado diretamente
if __name__ == "__main__":
    main()
