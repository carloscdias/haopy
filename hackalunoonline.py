from urllib.parse import urlencode
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pygoogle import pygoogle


class HackAlunoOnline:

	def __init__( self , matricula , verbose_output = False , uerj_pdf_files = False ):
		self.aluno_online_url = 'https://www.alunoonline.uerj.br/requisicaoaluno/requisicaoacesso.php'
		self.matricula        = matricula
		self.verbose_output   = verbose_output
		self.uerj_pdf_files   = uerj_pdf_files
		self.AO_html          = self._get_aluno_online_html()
		self.name             = self._extract_name()

		if ( uerj_pdf_files and ( len( self.name ) > 0 ) ):
			self.uerj_pdf_files_url = self._get_uerj_pdf_links()

	def _get_aluno_online_html( self ):
		data     = urlencode( dict( requisicao = "CadastroSenha" , matricula = self.matricula ) )
		request  = Request( self.aluno_online_url , data.encode( 'ascii' ) )
		response = urlopen( request )
		return BeautifulSoup( response.read() , 'html.parser' )

	def _get_uerj_pdf_links( self ):
		google_search = pygoogle( "site:vestibular.uerj.br filetype:pdf intext:\"{0}\"".format( self.name ) )
		return list( set( google_search.get_urls() ) )

	def _extract_name( self ):
		try:
			element = self.AO_html.find_all( "input" , dict( name = 'nome' ) )
			name = element[0]['value']
		except:
			name = ''

		return name

	def __str__( self ):
		pattern    = "{0}\t{1}"
		parameters = [ self.matricula , self.name ]
		
		if self.verbose_output:
			pattern = "-----------------\nMatrícula: {0}\nNome: {1}"
		
		if self.uerj_pdf_files:
			pattern += "\nUERJ PDF's: {2}" if self.verbose_output else "\t{2}"
			parameters.append( ( '\n' if self.verbose_output else ' , ' ).join( self.uerj_pdf_files_url ) )

		return pattern.format( *parameters )

# End class