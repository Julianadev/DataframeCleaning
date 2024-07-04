import pandas as pd
import os
import openpyxl

class GerenciamentoArquivos:
    def __init__(self, arquivo, aprovacao=7.0):
        self.arquivo = self._ler_arquivo(arquivo)
        self.alunos = self.arquivo['Aluno']
        self.notas = self.arquivo[['Nota 1', 'Nota 2', 'Nota 3', 'Nota 4']]
        self.faltas = self.arquivo['Faltas']
        self.aprovacao = aprovacao

    def _ler_arquivo(self, arquivo):
        try:
            df = pd.read_csv(arquivo, delimiter=';')
            df = df.drop(columns=['ID'])
            return df
        except FileNotFoundError:
            print(f'Arquivo {arquivo} não existe')
        except pd.errors.EmptyDataError:
            print(f'Arquivo {arquivo} está vazio')
        except Exception as e:
            print('Ocorreu um erro: ', e)


    def limpeza_arquivo(self):

        for _, linha in self.arquivo.iterrows():
            df = linha.values.tolist()
            print(df)

    def calcular_media(self):
        self.arquivo['Média'] = self.notas.mean(axis=1)

    def verificar_aprovacao(self):

        def verificando_aprovacao(row):
            return 'Aprovado' if row['Média'] >= self.aprovacao else 'Não aprovado'
        self.arquivo['Aprovação'] = self.arquivo.apply(verificando_aprovacao, axis=1)

    def agrupando_escolas(self, pasta_arquivo='escolas'):

        if not os.path.exists(pasta_arquivo):
            os.makedirs(pasta_arquivo)

        grupos = self.arquivo.groupby('Escola')

        for nome_escola, grupo in grupos:
            nome_arquivo = f"{nome_escola.replace(' ', '_')}.xlsx"
            caminho_arquivo = os.path.join(pasta_arquivo, nome_arquivo)
            grupo.to_excel(caminho_arquivo, index=False)
            print(f'Arquivo {nome_arquivo} salvo em {caminho_arquivo}')

    def exibir_arquivo(self):

        print(self.arquivo.to_string(index=False))

    def exportar_arquivo(self, novo_arquivo='df_alunos.xlsx'):

        self.arquivo.to_excel(novo_arquivo, index=False)
        print('Arquivo alunos limpo salvo com sucesso!')


if __name__ == "__main__":

    gerenciador = GerenciamentoArquivos('Alunos.txt')

    gerenciador.limpeza_arquivo()

    gerenciador.calcular_media()

    gerenciador.verificar_aprovacao()

    gerenciador.exibir_arquivo()

    gerenciador.exportar_arquivo()

    gerenciador.agrupando_escolas()


