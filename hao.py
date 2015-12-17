#!/usr/bin/python

from argparse import ArgumentParser
from hackalunoonline import HackAlunoOnline

#from pdfextractor import PDFExtractor

# Programa para recuperar os dados de um aluno da UERJ através de sua matrícula

	
def Main():
	parser = ArgumentParser( description = "Recupera informações de alunos da UERJ através de falhas do sistema acadêmico Aluno Online" )
	
	parser.add_argument( 'matricula' , help = "Matricula do aluno" )

	parser.add_argument( '-i' , '--inputfile' , help = "Utilizar um arquivo contendo uma lista de matrículas com uma matrícula por linha como entrada" , action = "store_true" )
	parser.add_argument( '-v' , '--verbose' , help = "Saída com mais conteúdo textual" , action = "store_true" )
	parser.add_argument( '-u' , '--uerjlinks' , help = "Links de pdfs da uerj (Em geral arquivos de classificação no vestibular)" , action = "store_true" )
	
	parser.add_argument( '-r' , '--reverse' , help = "Procura reversa -> busca matricula por nome" , action = "store_true" )
	parser.add_argument( '-f' , '--facebook' , help = "Link para o facebook do aluno" , action = "store_true" )
	parser.add_argument( '-b' , '--bruteforce' , help = "Ataque de força bruta para acesso ao Aluno Online" , action = "store_true" )

	args = parser.parse_args()

	#p = PDFExtractor( 'http://www.vestibular.uerj.br/portal_vestibular_uerj/arquivos/arquivos2014/2_eq_2014/Resultado/T-Z.pdf' )
	#print( p.get_text() )
	#raise SystemExit

	if ( args.reverse or args.facebook or args.bruteforce ):
		print( "Opção ainda não implementada :(" )
		raise SystemExit

	if args.inputfile:
		with open( args.matricula , 'r' ) as file:
			for line in file:
				matricula = line.strip( '\r\n' )
				hao = HackAlunoOnline( matricula , args.verbose , args.uerjlinks )
				print( hao )
	else:
		hao = HackAlunoOnline( args.matricula , args.verbose , args.uerjlinks )
		print( hao )

# End Main

if __name__ == '__main__':
	Main()