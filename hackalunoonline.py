from urllib.parse import urlencode
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pygoogle import pygoogle
import re


class HackAlunoOnline:

	def __init__( self , matricula , verbose_output = False , uerj_pdf_files = False ):
		self.aluno_online_url = 'http://www.alunoonline.uerj.br/requisicaoaluno/requisicao.php'
		self.matricula        = matricula
		self.verbose_output   = verbose_output
		self.uerj_pdf_files   = uerj_pdf_files
		self.AO_html          = self._get_aluno_online_html()
		self.name             = self._extract_name()
		self.cra              = self._extract_cra()
		self.curso            = self._extract_curso()
		self.situacao         = self._extract_situacao()
		self.periodo          = self._extract_periodo()

		if ( uerj_pdf_files and ( len( self.name ) > 0 ) ):
			self.uerj_pdf_files_url = self._get_uerj_pdf_links()

	def _get_aluno_online_html( self ):
		data     = urlencode( dict( requisicao = "SinteseFormacao" , matricula = self.matricula ) )
		request  = Request( self.aluno_online_url , data.encode( 'ascii' ) )
		response = urlopen( request )
		return BeautifulSoup( response.read() , 'html.parser' )

	def _get_uerj_pdf_links( self ):
		google_search = pygoogle( "site:vestibular.uerj.br filetype:pdf intext:\"{0}\"".format( self.name ) )
		return list( set( google_search.get_urls() ) )

	def _extract_name( self ):
		try:
			name = self.AO_html.find( id = "table_cabecalho_rodape" ).find_all( 'font' )[2].string[15:]
		except:
			name = ''

		return name

	def _extract_cra( self ):
		try:
			cra = float( self.AO_html.find_all( 'div' )[7].text[16:].replace( ',' , '.' ) )
		except:
			cra = ''

		return cra

	def _extract_curso( self ):
		try:
			curso = self.AO_html.find_all( 'div' )[6].text[8:]
		except:
			curso = ''

		return curso
	
	def _extract_situacao( self ):
		try:
			situacao = self.AO_html.find_all( 'div' )[4].text[11:]
		except:
			situacao = ''

		return situacao

	def _extract_periodo( self ):
		try:
			for element in self.AO_html.select( 'div > b' ):
				if ( element.text == "Períodos Utilizados/Em Uso para Integralização Curricular:" ):
					periodo = int( element.parent.text[59:] )
		except:
			periodo = ''

		return periodo

	def _truncate( self , string , width ):
		if ( len( string ) > width ):
			string = string[:( width - 3 )] + '...'

		return string

	def __str__( self ):
		if self.verbose_output:
			pattern    = "-----------------\nMatricula: {0}\nNome: {1}\nCurso: {2}\nSituacao: {3}\nPeriodo: {4}\nCRA: {5}"
			parameters = [ self.matricula , self.name , self.curso , self.situacao , self.periodo , self.cra ]
		else:
			pattern    = "{0:12}\t{1:30}\t{2:20}\t{3:10}\t{4:3}\t{5:4}"
			parameters = [ self.matricula , self._truncate( self.name , 30 ) ,  self._truncate( self.curso , 20 ) , self._truncate( self.situacao , 10 ) , self.periodo , self.cra ]
		
		if self.uerj_pdf_files:
			pattern += "\nUERJ PDF's: {6}" if self.verbose_output else "\t{6}"
			parameters.append( ( '\n' if self.verbose_output else ' , ' ).join( self.uerj_pdf_files_url ) )

		return pattern.format( *parameters )

# End class