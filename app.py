import telebot, time, threading, log, atualiza_token
from telebot import types
from voalle import validacontrato, Atualiza_Conexao, Captura_Id_Cto
from cto import valida_cto, valida_porta, pon_cto
from olt import busca_onu_na_pon, provisiona, consulta_gpon, desprovisiona_gpon, desprovisiona_efetivo
from autenticacao import apresentacao, verifica_nome, cadastro_no_Mysql, consulta_id, timeout, valida_senha, atualiza_timeout, consulta_permissao
from geogrid import portas_livres, Forca_Integracao


# fica no loop atualizando os tokens 
def Atualiza_Token_External():
    while True:
        atualiza_token.Atualiza_Token_Mapas2()
        time.sleep(3500)

thread = threading.Thread(target=Atualiza_Token_External)
thread.start()

def Atualiza_Token_External():
    while True:
        atualiza_token.Atualiza_Token_External()
        time.sleep(3500)

thread2 = threading.Thread(target=Atualiza_Token_External)
thread2.start()

class Provisionamento():
    def __init__(self):
        self.token = '6472203862:AAHU4w7KoQXst1lnNbRulypcMVVGURtKr4o'
        self.bot = telebot.TeleBot(self.token)
        self.cto_validada = list()
        self.ponto_de_acesso = list()
        self.pppoe_cliente = list()
        self.desprovisiona_parametros = list()
        self.contrato_cliente = list()
        self.item_de_rede = list()
        self.porta_cliente = list()
        self.id_cto_atualiza_voalle = list()
        self.id_cliente_voalle = list()
        self.permissoes = ['tecnico', 'admin']


    def apresentacao_inicial(self, chat_id, username=None):
        id_usuario = chat_id
        msg = apresentacao(username)
        self.bot.send_message(id_usuario, msg, parse_mode="Markdown")
        
        self.criarconta(id_usuario)
        
        
    def verifica_se_ja_tem_cadastro(self, chat_id, username):
        consulta = consulta_id(chat_id)
        if consulta == 'usuario ainda não tem cadastro':
            self.apresentacao_inicial(chat_id, username)
            
        else:
            self.bot.send_message(chat_id, '⚠ Ja possui um cadastro *vinculado a esse dispositivo* ⚠', parse_mode="Markdown")
            self.verifica_time_out(chat_id)
            
    
    def verifica_time_out(self, chat_id):
        time_out = timeout(chat_id)
        #print('TIMEOUT: ', time_out)
        if time_out == 'timeout':
            # solicitar novamente a senha
            self.verifica_senha(chat_id)

        else:
            # seguir com o fluxo
            self.menu_principal(chat_id)
            

    def verifica_time_out_botoes(self, chat_id, funcao_redirecionamento, *args, **kwargs):
        time_out = timeout(chat_id)
        print('TIMEOUT: ', time_out)
        
        if time_out == 'timeout':
            # solicitar novamente a senha
            print('cai no timeout: ')
            self.verifica_senha(chat_id)

        else:
            # seguir com o fluxo
            funcao_redirecionamento(*args, **kwargs)         

    
    def verifica_senha(self, chat_id):
        id_usuario = chat_id
        
        #faz a consulta ao banco pra pegar a senha cadastrada conforme o id do usuario
        senha_bd = valida_senha(id_usuario)
        
        self.bot.send_message(id_usuario, '🔑 *Informe sua senha de acesso para continuar!* 🔑', parse_mode="Markdown")
        
        @self.bot.message_handler(func=lambda message: True)
        def valida_senha_usuario(mensagem):
            senha_informada = mensagem.text
            
            if senha_informada == senha_bd:
                #self.bot.send_message(id_usuario, '*🥳✅ Login efetuado com sucesso!* ✅🥳', parse_mode="Markdown")
                
                #atualiza o time-out
                atualiza_timeout(id_usuario)
                self.menu_principal(id_usuario)
                
            else:
                self.bot.send_message(id_usuario, '❌ *Senha incorreta!*', parse_mode="Markdown")
                self.verifica_senha(id_usuario)
                
        self.bot.register_next_step_handler_by_chat_id(chat_id, valida_senha_usuario)
        
        
    def criarconta(self, chat_id):
        id_usuario = chat_id
        
        self.bot.send_message(id_usuario, '🙎‍♂️ Qual o seu *NOME COMPLETO?*', parse_mode="Markdown")
        
        @self.bot.message_handler(func=lambda message: True)
        def captura_nome(mensagem):
            nome_informado = str(mensagem.text).upper()

            resp_nome = verifica_nome(nome_informado)
            
            if resp_nome == 'nome não encontrado':
                self.bot.send_message(id_usuario, '😥 Nome informado não existe em nossa base de dados', parse_mode="Markdown")
                self.criarconta(id_usuario)
                
            else:
                nome, usuario, email, permissao = resp_nome
                print(nome, usuario, email, permissao, sep='\n')
                
                self.bot.send_message(id_usuario, '📌 Qual o seu *USUÁRIO DE LOGIN* do erp voalle?', parse_mode="Markdown")
                
                @self.bot.message_handler(func=lambda message: True)
                def captura_usuario(mensagem):
                    usuario_informado = str(mensagem.text).lower()
                    
                    if usuario_informado == usuario:
                        #self.bot.send_message(id_usuario, 'Usuario correto!', parse_mode="Markdown")
                        
                        self.bot.send_message(id_usuario, '✉ Qual o seu *EMAIL CADASTRADO* no erp voalle?', parse_mode="Markdown")
                        
                        @self.bot.message_handler(func=lambda message: True)
                        def captura_email(mensagem):
                            email_informado = mensagem.text
                        
                            if email_informado == email:
                                #self.bot.send_message(id_usuario, 'Email correto!', parse_mode="Markdown")
                                
                                self.bot.send_message(id_usuario, '📝 Crie uma *SENHA DE ACESSO AO BOT*\ntamanho min: _6 caracteres_', parse_mode="Markdown")
                                
                                @self.bot.message_handler(func=lambda message: True)
                                def captura_senha1(mensagem):
                                    senha1 = mensagem.text
                                    
                                    if len(senha1) >= 6:
                                        self.bot.send_message(id_usuario, '💻 *Senha armazenada!*\nconfirme novamente a senha.', parse_mode="Markdown")
                                        
                                        @self.bot.message_handler(func=lambda message: True)
                                        def captura_senha2(mensagem):
                                            senha2 = mensagem.text
                                            username = mensagem.chat.username

                                            if senha1 == senha2:
                                                cadastro = cadastro_no_Mysql(id_usuario, username, nome, usuario, email, senha1, permissao)
                                                self.bot.send_message(id_usuario, cadastro, parse_mode="Markdown")
                                                time.sleep(2)
                                                self.menu_principal(id_usuario)
                                                
                                            else:
                                                self.bot.send_message(id_usuario, '❌ *Senhas não conferem!*', parse_mode="Markdown")
                                                time.sleep(1)
                                                self.criarconta(id_usuario)
                                            
                                        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_senha2)
                                    
                                    else:
                                        self.bot.send_message(id_usuario, '❌ *Senha muito curta!*', parse_mode="Markdown")
                                        time.sleep(1)
                                        self.criarconta(id_usuario)                                 
                                                                               
                                self.bot.register_next_step_handler_by_chat_id(chat_id, captura_senha1)

                            else:
                                self.bot.send_message(id_usuario, '❌ Email incorreto!', parse_mode="Markdown")
                                time.sleep(1)
                                self.criarconta(id_usuario)
                                
                        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_email)
                                               
                    else:
                        self.bot.send_message(id_usuario, '❌ Usuario incorreto!', parse_mode="Markdown")
                        time.sleep(1)
                        self.criarconta(id_usuario)
            
                self.bot.register_next_step_handler_by_chat_id(chat_id, captura_usuario)
            
        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_nome)
        
        
    def menu_principal(self, chat_id):
        mensagem = 'Escolha uma opção:'
        id_usuario = chat_id

        # Criando o layout do teclado inline
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        # Criando os botões
        provisionar = types.InlineKeyboardButton("Provisionar ONU", callback_data='provisionamento')
        desprovisionar = types.InlineKeyboardButton("Desprovisionar ONU", callback_data='desprovisionar')
        consulta = types.InlineKeyboardButton("Consultar ONU", callback_data='consulta')

        # Adicionando os botões ao teclado inline
        teclado_inline.add(provisionar, desprovisionar, consulta)

        # Enviando a mensagem com o teclado inline
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_nova_tentativa(self, chat_id):
        id_usuario = chat_id

        # Criando o layout do teclado inline
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        # Criando os botões
        voltar_menu = types.InlineKeyboardButton("Voltar - Menu", callback_data='voltar_menu')
        tentar_novamente = types.InlineKeyboardButton("Tentar Novamente", callback_data='tentar_novamente')

        # Adicionando os botões ao teclado inline
        teclado_inline.add(voltar_menu, tentar_novamente)

        # Enviando a mensagem com o teclado inline
        mensagem = "Não consegui localizar o contrato desse cliente 🙁\nO que você deseja fazer?"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_confirmacao_olt(self, chat_id):
        id_usuario = chat_id

        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        confirmar = types.InlineKeyboardButton("Tudo certo!", callback_data='tudo_certo_olt')
        tentar_novamente = types.InlineKeyboardButton("Tentar Novamente", callback_data='tentar_novamente_cto')

        teclado_inline.add(confirmar, tentar_novamente)
        mensagem = "Antes de continuar, por favor confirme as informações"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_confirmacao_olt_onu_n_encontrada(self, chat_id):
        id_usuario = chat_id

        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        tentar_novamente = types.InlineKeyboardButton("Tentar Novamente", callback_data='tentar_novamente_cto')
        volta_menu = types.InlineKeyboardButton("Volta Menu", callback_data='volta_menu')

        teclado_inline.add(tentar_novamente, volta_menu)

        mensagem = "Não consegui localizar nenhuma ONU discando nessa pon 🙁\nO que você deseja fazer?"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_confirmacao(self, chat_id):
        id_usuario = chat_id

        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        correto = types.InlineKeyboardButton("Tudo certo!", callback_data='correto')
        incorreto = types.InlineKeyboardButton("Tentar novamente", callback_data='incorreto')

        teclado_inline.add(correto, incorreto)

        mensagem = "Antes de continuar, por favor confirme as informações"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)
        
        
    def menu_confirma_desprovisionamento(self, chat_id):
        id_usuario = chat_id
        
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)
        
        confirma = types.InlineKeyboardButton("Sim!", callback_data='desprovisiona-olt')
        tentar_novamente = types.InlineKeyboardButton("Buscar Outra!", callback_data='tenta-novamente-consulta')
        menu = types.InlineKeyboardButton("Menu", callback_data='volta_menu')
        
        teclado_inline.add(confirma, tentar_novamente, menu)
        
        mensagem = "Deseja desprovisionar essa ONU?"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline) 
        
           
    def menu_porta_ocupada(self, porta, chat_id):
        id_usuario = chat_id
        
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)
        
        sim = types.InlineKeyboardButton("Sim!", callback_data='adiciona-cliente')
        não = types.InlineKeyboardButton("Não!", callback_data='nao-adiciona-cliente')
        
        teclado_inline.add(sim, não)
        
        mensagem = f"Verifiquei que a porta {porta} já está ocupada por outro cliente.\nDeseja sobrescrever para o seu cliente?"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)    


    def provisionamento(self, chat_id):
        permissao = consulta_permissao(chat_id)
        if permissao in self.permissoes:
            
            mensagem = '> Informe o número do contrato, por favor!'
            id_usuario = chat_id
            self.bot.send_message(id_usuario, mensagem)

            # escuta a resposta do contrato
            @self.bot.message_handler(func=lambda message: True)
            def captura_contrato(mensagem): 
                contrato = mensagem.text
                
                self.contrato_cliente.clear()
                self.contrato_cliente.append(contrato)
                
                mensagem_validacao, id_cliente_voalle = validacontrato(contrato)

                if mensagem_validacao is False:
                    mensagem = 'Opa, não aceitamos caracteres por aqui 😊\nDigite apenas números, por favor!'
                    self.bot.send_message(id_usuario, mensagem)
                    self.provisionamento(id_usuario)

                elif mensagem_validacao == 'contrato não localizado':
                    self.menu_nova_tentativa(id_usuario)

                else:
                    # se cair aqui significa que achou um contrato valido
                    self.bot.send_message(id_usuario, mensagem_validacao)
                    self.ponto_de_acesso.clear()
                    self.ponto_de_acesso.append(mensagem_validacao.split('\n')[6].split(':')[1].strip())
                    print(self.ponto_de_acesso)
                    self.pppoe_cliente.clear()
                    self.pppoe_cliente.append(mensagem_validacao.split('\n')[11].split(':')[1].strip())
                    print(self.pppoe_cliente)
                    
                    print('id do cliente no voalle é:', id_cliente_voalle)
                    self.id_cliente_voalle.clear()
                    self.id_cliente_voalle.append(id_cliente_voalle)
                    
                    
                    time.sleep(1)
                    self.menu_confirmacao(id_usuario)

            self.bot.register_next_step_handler_by_chat_id(chat_id, captura_contrato)
            
        else:
            self.bot.send_message(chat_id, '😕 Você não tem *permissão* pra ultilizar essa funcionalidade 😕', parse_mode="Markdown")
            with open('sticker.png', 'rb') as adesivo:
                self.bot.send_sticker(chat_id, adesivo)


    def solicita_cto(self, chat_id):
        mensagem = 'Informe a CTO que conectou o cliente:\n_Sugestão: AAA1-1_'
        id_usuario = chat_id
        self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")

        @self.bot.message_handler(func=lambda message: True)
        def captura_cto(cto):
            cto = cto.text

            cto_validacao = valida_cto(cto)
            
            if cto_validacao == 'cto não encontrada':
                self.bot.send_message(id_usuario, "CTO não encontrada!\n> Tente novamente ")
                time.sleep(1)
                self.solicita_cto(id_usuario)
                
            else:
                # se a cto for valida ele cai aqui
                #self.bot.send_message(id_usuario, f'CTO VÁLIDA {cto_validacao[0]}')

                # separa o item de rede da cto
                self.item_de_rede.clear()
                self.item_de_rede.append(cto_validacao[1])

                #adiciona cto validada na lista
                self.cto_validada.append(cto_validacao[0])
                
                #captura o id da cto pra atualizar no voalle
                id_cto_voalle = Captura_Id_Cto(cto_validacao[0])
                
                if id_cto_voalle == 'id da cto não localizado':
                    self.bot.send_message(id_usuario, f'id da cto não localizado {cto_validacao[0]}')
                    
                else:
                    # se cair aqui é pq achou o id da cto correspondente no voalle
                    self.id_cto_atualiza_voalle.clear()
                    self.id_cto_atualiza_voalle.append(id_cto_voalle)
                    
                    
                time.sleep(1)
                self.solicita_porta_cto(id_usuario)

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_cto)


    def solicita_porta_cto(self, chat_id):
        mensagem = 'Informe a PORTA que conectou o cliente:\n_Sugestão: 1 à 16_'
        id_usuario = chat_id
        self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")

        @self.bot.message_handler(func=lambda message: True)
        def captura_porta(porta):
            porta = porta.text

            porta_cto = valida_porta(porta)

            if porta_cto == 'não é numero':
                self.bot.send_message(id_usuario, "Digite apenas numeros, por favor!")
                time.sleep(1)
                self.solicita_porta_cto(id_usuario)

            elif porta_cto == 'porta invalida':
                self.bot.send_message(id_usuario, "Digite apenas valores entre 1 e 16")
                time.sleep(1)
                self.solicita_porta_cto(id_usuario)

            else:
                # porta válida
                #self.bot.send_message(id_usuario, f"PORTA VÁLIDA {porta_cto}")
                self.porta_cliente.clear()
                self.porta_cliente.append(porta_cto)
                time.sleep(1)

                # pegando qual é a pon da cto informada
                pon_consulta = pon_cto(self.cto_validada[0])
                print(pon_consulta)

                # verifica se tem algum ponto de acesso na agulha
                if len(self.ponto_de_acesso) == 0:
                    self.bot.send_message(id_usuario, 'Digite o contrato do cliente para continuar')
                    self.provisionamento(id_usuario)

                else:
                    #chama  afunção pra tratar os retornos da olt
                    print(self.ponto_de_acesso[0])
                    self.consulta_olt(id_usuario, self.ponto_de_acesso[0], pon_consulta)

                # limpando a lista para uma nova consulta
                self.cto_validada.clear()
                self.ponto_de_acesso.clear()
                #self.pppoe_cliente.clear()

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_porta)


    def consulta_olt(self, chat_id, ponto_de_acesso, pon):
        id_usuario = chat_id
        self.bot.send_message(id_usuario, "Buscando ONU...\nPor favor, aguarde!")
        self.bot.send_chat_action(id_usuario, 'typing')
        try:
            print('chamei a função busca onu na pon')
            retorno = busca_onu_na_pon(ponto_de_acesso, pon)
            
            if retorno == False:
                print('cai no false')
                
                time.sleep(1)
                self.menu_confirmacao_olt_onu_n_encontrada(id_usuario)
                
            else:
                try:
                    print('cai no else, com os paramentros')
                    
                    self.itbs, self.serial, self.modelo, self.modelo_permtido, self.posicao_na_pon, self.pon_atual, self.ponto_acesso = retorno

                    retorno_final = f'''
📌 *PROVISIONAMENTO PREENCHIDO* 📌

ℹ️ *ONU ENCONTRADA:* ℹ️

🔒 *Serial GPON:* {self.itbs}{self.serial}
💡 *Modelo:* {self.modelo}
    ''' 
                    self.bot.send_message(id_usuario, retorno_final, parse_mode="Markdown")

                    time.sleep(1)
                    self.menu_confirmacao_olt(id_usuario)
                    
                except Exception as e:
                    onus_discando, posicao_na_pon, pon_atual, ponto_acesso, quantidade_onu = retorno
                       
                    print(f'erro foi: {str(e)}')
                        
                    print(onus_discando, posicao_na_pon, pon_atual, ponto_acesso, quantidade_onu)

                    mensagem = f'''
ℹ️ *Encontramos {quantidade_onu} ONU(s) disponíveis:* ℹ️
'''
                    for i, onu in enumerate(onus_discando):
                        indice = i + 1
                        fabricante = onu[1]
                        serial = onu[2]
                        modelo = onu[3]

                        mensagem += f'''
🆔 *ID:* 0{indice}
🔒 *Serial GPON:* `{fabricante}{serial}`
💡 *Modelo:* {modelo}
'''                    
                    self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")

                    self.trata_mais_de_uma_onu(onus_discando, posicao_na_pon, pon_atual, ponto_acesso, id_usuario)

        except:
            print('cai no except')
            retorno_final = busca_onu_na_pon(ponto_de_acesso, pon)

            if retorno_final == False:
                time.sleep(1)
                self.menu_confirmacao_olt_onu_n_encontrada(id_usuario)
                
                
    def trata_mais_de_uma_onu(self, onus_discando, posicao_na_pon, pon_atual, ponto_acesso, chat_id):
        id_usuario = chat_id
        mensagem = 'Copie o *Serial GPON* da _ONU_ que quer provisionar e cole aqui:'
        
        self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")
        
        self.itbs = None
        self.serial = None
        self.modelo_permtido = None
        self.posicao_na_pon = None
        self.pon_atual = None
        self.ponto_acesso = None    
        
        @self.bot.message_handler(func=lambda message: True)
        def captura_gpon(mensagem): 
            achei = False
            mensagem = mensagem.text

            for gpon  in onus_discando:
                gpon_sn = gpon[1] + gpon[2]
                modelo = gpon[3]
                
                if mensagem == gpon_sn:
                    achei = True
                    self.itbs = gpon[1]
                    self.serial = gpon[2]
                    self.modelo_permtido = gpon[-1]
                    self.posicao_na_pon = posicao_na_pon
                    self.pon_atual = pon_atual
                    self.ponto_acesso = ponto_acesso
                    
                    retorno_final = f'''
📌 *PROVISIONAMENTO PREENCHIDO* 📌

ℹ️ *ONU SELECIONADA:* ℹ️

🔒 *Serial GPON:* {gpon_sn}
💡 *Modelo:* {modelo}
''' 
                    self.bot.send_message(id_usuario, retorno_final, parse_mode="Markdown")
                    time.sleep(1)
                    self.menu_confirmacao_olt(id_usuario)
                     
            if achei is False:
                
                self.bot.send_message(id_usuario, '😥 *Não encontrei esse GPON-SN*, verifique novamente, por favor', parse_mode="Markdown")
            
                self.trata_mais_de_uma_onu(onus_discando, posicao_na_pon, pon_atual, ponto_acesso, chat_id)
            
        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_gpon)
    
        
    def provisiona_onu(self, itbs, serial, modelo_permtido, posicao_na_pon, pon_atual, ponto_de_acesso, pppoe, chat_id):
        id_usuario = chat_id
        gpon_sn = itbs + serial
        modelo_profile = modelo_permtido
        gpon = pon_atual
        posi_disponivel = posicao_na_pon
        usuario_pppoe = pppoe
        pontode_acesso = ponto_de_acesso

        self.bot.send_message(id_usuario, '*INICIANDO O PROVISIONAMENTO...*', parse_mode="Markdown")

        resultado = provisiona(gpon, posi_disponivel, gpon_sn, modelo_profile, usuario_pppoe, pontode_acesso)

        self.bot.send_message(id_usuario, resultado, parse_mode="Markdown")
        
        self.pppoe_cliente.clear()

        print(self.pppoe_cliente, self.ponto_de_acesso, self.cto_validada)
        time.sleep(2)
        self.menu_principal(id_usuario)
        
        
    # atualiza no geogrid
    def add_geogrid(self, item_rede, porta_cliente, contrato, usuario_pppoe, id_usuario):
        
        atualiza = portas_livres(item_rede, porta_cliente, contrato, usuario_pppoe)
        
        if atualiza == 'porta ocupada para uso':
            self.menu_porta_ocupada(self.porta_cliente[0], id_usuario)
            
        else:
            self.bot.send_message(id_usuario, atualiza, parse_mode="Markdown")
            
            # valida se caturou o id da cto no voalle
            if len(self.id_cto_atualiza_voalle) >= 1:
                
                # chamar pra atualizar no voalle aqui
                serial_gpon_voalle = self.itbs + self.serial
                
                atualiza_no_voalle = Atualiza_Conexao(self.id_cliente_voalle[0], self.posicao_na_pon, serial_gpon_voalle, self.id_cto_atualiza_voalle[0], porta_cliente)
                
                self.bot.send_message(id_usuario, 'Voalle: ' + atualiza_no_voalle, parse_mode="Markdown")
            else:
                self.bot.send_message(id_usuario, '*Erro - Voalle* >> Não conseguir capturar o ID do cliente no sistema', parse_mode="Markdown")
                

            self.provisiona_onu(self.itbs, self.serial, self.modelo_permtido, self.posicao_na_pon, self.pon_atual, self.ponto_acesso, self.pppoe_cliente[0], id_usuario)
            
            
    def add_geogrid_forcando(self, item_rede, porta_cliente, contrato, usuario_pppoe, id_usuario):
    
        forca_integração = Forca_Integracao(item_rede, porta_cliente, contrato, usuario_pppoe)
    
        self.bot.send_message(id_usuario, forca_integração, parse_mode="Markdown")
        
        # valida se caturou o id da cto no voalle
        if len(self.id_cto_atualiza_voalle) >= 1:
            
            # chamar pra atualizar no voalle aqui
            serial_gpon_voalle = self.itbs + self.serial
            
            atualiza_no_voalle = Atualiza_Conexao(self.id_cliente_voalle[0], self.posicao_na_pon, serial_gpon_voalle, self.id_cto_atualiza_voalle[0], porta_cliente)
            
            self.bot.send_message(id_usuario, 'Voalle: ' + atualiza_no_voalle, parse_mode="Markdown")
        else:
            self.bot.send_message(id_usuario, '*Erro - Voalle* >> Não conseguir capturar o ID do cliente no sistema', parse_mode="Markdown")

        
        self.provisiona_onu(self.itbs, self.serial, self.modelo_permtido, self.posicao_na_pon, self.pon_atual, self.ponto_acesso, self.pppoe_cliente[0], id_usuario)
    
        
        
    # pra consultar a onu
    def pega_ponto_de_acesso(self, chat_id):
        id_usuario = chat_id
        msg_informativa = '''
*Pontos de Acesso permitidos:*
1º  `Rod Alca OLT FTTH`
2º  `Vila Jamic OLT FTTH`
3º  `bujaru` (vilas)
'''
        self.bot.send_message(id_usuario, "Digite o *Ponto de Acesso* que queres fazer a consulta", parse_mode="Markdown")
        self.bot.send_message(id_usuario, msg_informativa, parse_mode="Markdown")
        
        @self.bot.message_handler(func=lambda message: True)
        def captura_localidade(mensagem): 
            mensagem = mensagem.text
            permitidos = ['Rod Alca OLT FTTH', 'Vila Jamic OLT FTTH', 'bujaru', '1', '2', '3']
            
            if mensagem == '/sair':
                self.menu_principal(id_usuario)
            
            elif mensagem in permitidos:
                #self.bot.send_message(id_usuario, f"✅ Ponto de acesso *{mensagem}* permitido!", parse_mode="Markdown")
                time.sleep(0.7)
                self.consulta(id_usuario, mensagem)
                 
            else:
                self.bot.send_message(id_usuario, "❌ Ponto de acesso não permitido", parse_mode="Markdown")
                time.sleep(0.7)
                self.pega_ponto_de_acesso(id_usuario)
            
        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_localidade)
        
    # consulta onu
    def consulta(self, chat_id, ponto_de_acesso):
        id_usuario = chat_id
        self.bot.send_message(id_usuario, "Digite os ultimos 8 números do *GPON-SN* da _ONU_", parse_mode="Markdown")
        
        @self.bot.message_handler(func=lambda message: True)
        def captura_gpon_consulta(mensagem): 
            mensagem = mensagem.text
            
            if mensagem == '/sair':
                self.menu_principal(id_usuario)
            
            else:
                
                self.bot.send_message(id_usuario, "Buscando ONU...\nPor favor, aguarde!", parse_mode="Markdown")
                self.bot.send_chat_action(id_usuario, 'typing')
            
                retorno = consulta_gpon(mensagem, ponto_de_acesso)
            
                if retorno == 'tamanho inválido':
                    self.bot.send_message(id_usuario, "Tamanho inválido 😕\nO serial gpon contém 8 caracteres alfanuméricos", parse_mode="Markdown")
                    time.sleep(1)
                    self.consulta(id_usuario, ponto_de_acesso)
                    
                elif retorno == 'alfanumericos false':
                    self.bot.send_message(id_usuario, "Caracteres inválidos 😕\nDigite somente letras e números", parse_mode="Markdown")
                    time.sleep(1)
                    self.consulta(id_usuario, ponto_de_acesso)
                    
                elif retorno == 'erro na busca':
                    self.bot.send_message(id_usuario, "Ocorreu um erro em buscar a *ONU* 😕\nPor favor, tente novamente!", parse_mode="Markdown")
                    time.sleep(1)
                    self.pega_ponto_de_acesso(id_usuario)
                
                else:
                    self.bot.send_message(id_usuario, retorno, parse_mode="Markdown")
                    #time.sleep(0.7)
                    #self.bot.send_message(id_usuario, '✅ *Consulta finalizada* ✅', parse_mode="Markdown")
                    time.sleep(1)
                    self.menu_principal(id_usuario)
                
        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_gpon_consulta)


    # pra desprovisionar a onu
    def pega_ponto_de_acesso2(self, chat_id):
        id_usuario = chat_id
        permissao = consulta_permissao(id_usuario)
        if permissao in self.permissoes:
            msg_informativa = '''
*Pontos de Acesso permitidos:*
1º  `Rod Alca OLT FTTH`
2º  `Vila Jamic OLT FTTH`
3º  `bujaru` (vilas)
'''
            self.bot.send_message(id_usuario, "Digite o *Ponto de Acesso* para buscar ONU", parse_mode="Markdown")
            self.bot.send_message(id_usuario, msg_informativa, parse_mode="Markdown")

            @self.bot.message_handler(func=lambda message: True)
            def captura_localidade2(mensagem): 
                mensagem = mensagem.text
                permitidos = ['Rod Alca OLT FTTH', 'Vila Jamic OLT FTTH', 'bujaru', '1', '2', '3']

                if mensagem in permitidos:
                    #self.bot.send_message(id_usuario, f"✅ Ponto de acesso *{mensagem}* permitido!", parse_mode="Markdown")
                    time.sleep(0.7)
                    self.consulta2(id_usuario, mensagem)
                    
                else:
                    self.bot.send_message(id_usuario, "❌ Ponto de acesso não permitido", parse_mode="Markdown")
                    time.sleep(0.7)
                    self.pega_ponto_de_acesso2(id_usuario)

            self.bot.register_next_step_handler_by_chat_id(chat_id, captura_localidade2)
            
        else:
            self.bot.send_message(chat_id, '😕 Você não tem *permissão* pra ultilizar essa funcionalidade 😕', parse_mode="Markdown")
            with open('sticker.png', 'rb') as adesivo:
                self.bot.send_sticker(chat_id, adesivo)


    def consulta2(self, chat_id, ponto_de_acesso):
        id_usuario = chat_id
        self.bot.send_message(id_usuario, "Digite os ultimos 8 números do *GPON-SN* da _ONU_", parse_mode="Markdown")
        
        @self.bot.message_handler(func=lambda message: True)
        def captura_gpon_consulta2(mensagem): 
            mensagem = mensagem.text
            
            self.bot.send_message(id_usuario, "Buscando ONU...\nPor favor, aguarde!", parse_mode="Markdown")
            self.bot.send_chat_action(id_usuario, 'typing')
            
            retorno = desprovisiona_gpon(mensagem, ponto_de_acesso) 
            
            if retorno == 'tamanho inválido':
                self.bot.send_message(id_usuario, "Tamanho inválido 😕\nO serial gpon contém 8 caracteres alfanuméricos", parse_mode="Markdown")
                time.sleep(1)
                self.consulta2(id_usuario, ponto_de_acesso)
                
            elif retorno == 'alfanumericos false':
                self.bot.send_message(id_usuario, "Caracteres inválidos 😕\nDigite somente letras e números", parse_mode="Markdown")
                time.sleep(1)
                self.consulta2(id_usuario, ponto_de_acesso)
                
            elif retorno == 'erro na busca':
                self.bot.send_message(id_usuario, "Ocorreu um erro em buscar a *ONU* 😕\nPor favor, tente novamente!", parse_mode="Markdown")
                time.sleep(1)
                self.pega_ponto_de_acesso2(id_usuario)
            
            else:
                if type(retorno) is list:
                    print('é uma lista', retorno)
                    
                    mensagem_form = f'''
ℹ️ INFORMAÇÕES DO GPON-SN ℹ️

🔍 *GPON-SN:* ITBS{retorno[4]}
🔍 *Modelo:* {retorno[-2]}
🔍 *Ativo na PON:* {retorno[1]}
🔍 *Posição:* {retorno[3]}
'''                 
                    pon_desprovisiona = retorno[1]
                    posicao_onu_desprovisiona = retorno[3]
                    ponto_de_acesso_desprovisiona = retorno[-1]
                    
                    self.desprovisiona_parametros.clear()
                    self.desprovisiona_parametros.append(pon_desprovisiona)
                    self.desprovisiona_parametros.append(posicao_onu_desprovisiona)
                    self.desprovisiona_parametros.append(ponto_de_acesso_desprovisiona)
                    
                    print('listaaaaaaaaaa', self.desprovisiona_parametros)
                    
                    self.bot.send_message(id_usuario, mensagem_form, parse_mode="Markdown")
                    time.sleep(0.7)
                    self.menu_confirma_desprovisionamento(id_usuario)
                    
                else:
                    print('retorno não é uma lista')
                    
                    self.bot.send_message(id_usuario, retorno, parse_mode="Markdown")
                    #self.bot.send_message(id_usuario, '✅ *Consulta finalizada* ✅', parse_mode="Markdown")
                    time.sleep(1.5)
                    self.menu_principal(id_usuario)
                
        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_gpon_consulta2)


    def trata_desprovisionamento(self, pon, onu, ponto_de_acesso, id_usuario):
        
        self.bot.send_message(id_usuario, '*INICIANDO O DESPROVISIONAMENTO...*', parse_mode="Markdown")
        
        desprovisiona = desprovisiona_efetivo(pon, onu, ponto_de_acesso)
        
        self.bot.send_message(id_usuario, desprovisiona, parse_mode="Markdown")
        time.sleep(1)
        self.menu_principal(id_usuario)       
    

    def tratativa_dos_botoes(self, call):
        id_usuario = call.message.chat.id

        if call.data == 'provisionamento':
            print('botão provisionamento chamado')
            self.verifica_time_out_botoes(id_usuario, self.provisionamento, id_usuario)
            
        elif call.data == 'desprovisionar':
            print('botão desprovisionar chamado')
            self.verifica_time_out_botoes(id_usuario, self.pega_ponto_de_acesso2, id_usuario)
            
        elif call.data == 'consulta':
            print('botão consulta chamado')
            self.verifica_time_out_botoes(id_usuario, self.pega_ponto_de_acesso, id_usuario)
            
        elif call.data == 'voltar_menu':
            print('botão voltar menu chamado')
            self.verifica_time_out_botoes(id_usuario, self.menu_principal, id_usuario)
        
        elif call.data == 'tentar_novamente':
            print('botão tentar novamente chamado')
            self.verifica_time_out_botoes(id_usuario, self.provisionamento, id_usuario)     

        elif call.data == 'correto':
            print('botão tudo certo chamado')
            self.verifica_time_out_botoes(id_usuario, self.solicita_cto, id_usuario)            

        elif call.data == 'incorreto':
            print('botão incorreto chamado')
            self.verifica_time_out_botoes(id_usuario, self.provisionamento, id_usuario)
            
        elif call.data == 'tudo_certo_olt':
            print('botão tudo certo olt chamado')
            self.verifica_time_out_botoes(id_usuario, self.add_geogrid, self.item_de_rede[0], self.porta_cliente[0], self.contrato_cliente[0], self.pppoe_cliente[0], id_usuario)

        elif call.data == 'tentar_novamente_cto':
            print('botão tentar novamente cto chamado')
            self.verifica_time_out_botoes(id_usuario, self.solicita_cto, id_usuario)

        elif call.data == 'volta_menu':
            print('botão tentar novamente cto chamado')
            self.desprovisiona_parametros.clear()
            self.verifica_time_out_botoes(id_usuario, self.menu_principal, id_usuario)

        elif call.data == 'desprovisiona-olt':
            print('botão desprovisionar chamado')
            self.verifica_time_out_botoes(id_usuario, self.trata_desprovisionamento, self.desprovisiona_parametros[0], self.desprovisiona_parametros[1], self.desprovisiona_parametros[2], id_usuario)

        elif call.data == 'tenta-novamente-consulta':
            print('botão tenta novamente desprovi. chamado')
            self.desprovisiona_parametros.clear()
            self.verifica_time_out_botoes(id_usuario, self.pega_ponto_de_acesso2, id_usuario)
            
        elif call.data == 'adiciona-cliente':
            print('botão adiciona cliente no geogrid chamado')
            self.verifica_time_out_botoes(id_usuario, self.add_geogrid_forcando, self.item_de_rede[0], self.porta_cliente[0], self.contrato_cliente[0], self.pppoe_cliente[0], id_usuario)
            
        elif call.data == 'nao-adiciona-cliente':
            print('botão não adiciona cliente no geogrid chamado')
            
            self.bot.send_message(id_usuario, '*⚠ Operação Cancelada, solicite suporte ao time INTERNO! ⚠*', parse_mode="Markdown")
            
            self.verifica_time_out_botoes(id_usuario, self.menu_principal, id_usuario)
            
            
            #self.verifica_time_out_botoes(id_usuario, self.provisiona_onu, self.itbs, self.serial, self.modelo_permtido, self.posicao_na_pon, self.pon_atual, self.ponto_acesso, self.pppoe_cliente[0], id_usuario)
            
            
    def inicia_bot(self):
        @self.bot.message_handler(func=lambda message: True)
        def escuta_msg(mensagem):
            id_usuario = mensagem.chat.id
            username = mensagem.chat.username
            retorno_usuario = mensagem.text

            #print('ID USUARIO', id_usuario, '>', retorno_usuario)
            log.info(f'Usuario {id_usuario}/{username} enviou > {retorno_usuario}')

            if retorno_usuario == '/start':
                self.verifica_se_ja_tem_cadastro(id_usuario, username)
            
            else:
                #log.info('verificando timeout')
                self.verifica_time_out(id_usuario)
            
        @self.bot.callback_query_handler(func=lambda call: True)
        def escuta_botoes(call):
            self.tratativa_dos_botoes(call)

        self.bot.infinity_polling()


# Uso da classe Provisionamento
provisionamento1 = Provisionamento()
provisionamento1.inicia_bot()