import json
from random import randint
import os
from datetime import datetime as dt
import csv

os.system('cls')
        
class Menu:
    
    def valida_cpf(self, cpf_inicial):   # VALIDA CPF
        try:
            cpf_inicial = str(cpf_inicial)
            cpf_inicial9 = cpf_inicial[:9]
            acumulador = 0
            contador = 10
            for i in cpf_inicial9:
                acumulador += int(i)*contador
                contador -= 1

            x = 11 - (acumulador % 11)
            digito1 = 0 if  x > 9 else x
            acumulador = 0
            contador = 11
            cpf_inicial9 += str(digito1)

            for i in cpf_inicial9:
                acumulador += int(i)*contador
                contador -= 1

            digito2 = 11 - (acumulador % 11)

            
            return cpf_inicial if cpf_inicial == cpf_inicial9+str(digito2) else 0/0
        except:
            self.valida_cpf(input('CPF inválido, digite novamente: '))   # RECURSIVIDADE

    def cadastrar_ferramenta(self):   # CADASTRA FERRAMENTA
        os.system('cls')
        print(f"""{'-'*10} Cadastro de Ferramenta {'-'*10}""")
        valores = ['descricao', 'part_number', 'tamanho_cm', 'tipo', 'material', 'tempo_max']
        dicionario = dict()
        try:
            with open('ferramentas.json') as file:   # UTILIZAÇÃO DE ARQUIVOS JSON
                lista_ferramentas = json.load(file)
            
        except:
            lista_ferramentas = []

        dicionario['id'] = randint(1111, 9999)

        for i in valores:
            dicionario[i] = input(f'{i.upper()}: ')
        

        lista_ferramentas.append(dicionario)
        with open('ferramentas.json', 'w+') as file:
            json.dump(lista_ferramentas, file, indent=True)

    def cadastrar_tecnico(self):   # CADASTRA TÉCNICO
        os.system('cls')
        print(f"""{'-'*10} Cadastro de Tecnico {'-'*10}""")
        valores = ['nome', 'cpf', 'telefone', 'e_mail', 'nome_da_equipe', 'turno']
        dicionario = dict()
        try:
            with open('tecnicos.json') as file:
                lista_tecnicos = json.load(file)
            
        except:
            lista_tecnicos = []

        for i in valores:
            dicionario[i] = input(f'{i.upper()}: ') if i != 'cpf' else self.valida_cpf(input(f'{i.upper()}: '))

        lista_tecnicos.append(dicionario)
        with open('tecnicos.json', 'w+') as file:
            json.dump(lista_tecnicos, file, indent=True)

    def consultar_ferramentas(self):   # CONSULTA FERRAMENTAS
        os.system('cls')
        print(f"""{'-'*10} Ferramentas Cadastradas {'-'*10}""")

        try:
            with open('ferramentas.json') as file:
                lista_ferramentas = json.load(file)
            
        except:
            print('Ainda não existem ferramentas cadastradas!')
            return

        for i in lista_ferramentas:
            for k, v in i.items():
                print(f'{k}: {v}')
            print('-'*45)

    def consultar_tecnicos(self):   # CONSULTA TÉCNICOS
        os.system('cls')
        print(f"""{'-'*10} Tecnicos Cadastrados {'-'*10}""")
        try:
            with open('tecnicos.json') as file:
                lista_tecnicos = json.load(file)
            
        except:
            print('Ainda não existem tecnicos cadastrados!')
            return

        for i in lista_tecnicos:
            for k, v in i.items():
                print(f'{k}: {v}')
            print('-'*42)

    def reservar_ferramenta(self):   # RESERVA FERRAMENTAS
        os.system('cls')
        self.consultar_ferramentas()
        print(f"""{'-'*10} Reserva de ferramenta {'-'*10}""")
        escolha_id = input('\nDigite o ID da ferramenta desejada: ')
        try:
            with open('ferramentas.json') as file:
                lista_ferramentas = json.load(file)
            
        except:
            lista_ferramentas = []

        achou = False
        for ferramenta in lista_ferramentas:
            if str(ferramenta['id']) == escolha_id:
                id_ferramenta = ferramenta['id']
                descricao = ferramenta['descricao']
                horas = ferramenta['tempo_max']
                achou = True

        if not achou: 
            self.reservar_ferramenta()

        self.consultar_tecnicos()
        tecnico_cpf = self.valida_cpf(input('Para reservar sua ferramenta preciso te localizar na minha base de dados para isso digite seu CPF: '))
        try:
            with open('tecnicos.json') as file:
                lista_tecnicos = json.load(file)
            
        except:
            lista_tecnicos = []

        
        for tecnico in lista_tecnicos:
            if tecnico['cpf'] == tecnico_cpf:
                nome_tecnico =  tecnico['nome']
        
        cadastro = [id_ferramenta, descricao, horas, dt.now().strftime("%d/%m/%Y %H:%M"), nome_tecnico]
        print(f'Reserva efetuada com sucesso para {nome_tecnico}! {dt.now().strftime("%d/%m/%Y %H:%M")}, duração: {horas}')
        try:
            with open('reservas.csv', 'a+') as file:   # UTILIZAÇÃO DE ARQUIVOS CSV
                escreve = csv.writer(file)
                escreve.writerow(cadastro)        
        except:
            print('Erro inesperado tente novamente')
        
    def consultar_reservas(self):   # CONSULTA RESERVAS
        os.system('cls')
        print(f"""{'-'*10} Consulta Reservas {'-'*10}""")

        with open('reservas.csv') as file:
            lista = [x for x in list(csv.reader(file)) if x]
        
        for i in lista:
            print(*i, sep=' / ')
            print()

    def start(self):   # RECURSIVIDADE
        try:
            print()
            print(f"""{'-'*10} Menu Principal {'-'*10}""")
            print('Escolha uma das opções abaixo para continuar.')
            opcao = input('\n1 - Cadastrar Técnico\n\n2 - Cadastrar Ferramenta\n\n3 - Consultar Técnicos\n\n4 - Consultar Ferramentas\n\n5 - Reservar Ferramenta\n\n6 - Consultar Reservas\n\n-- Ou digite "E" para sair --\n\nSua Escolha: ')
            dicio_opcoes = {
                '1': self.cadastrar_tecnico,
                '2': self.cadastrar_ferramenta,
                '3': self.consultar_tecnicos,
                '4': self.consultar_ferramentas,
                '5': self.reservar_ferramenta,
                '6': self.consultar_reservas,
            }
            if opcao in 'eE': return
            dicio_opcoes[opcao]()
            self.start()
        except:
            print('---- ERRO INESPERADO TENTE NOVAMENTE! ----')
            self.start()


if __name__ == '__main__':
    Menu().start()
