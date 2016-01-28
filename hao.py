#!/usr/bin/python

from argparse import ArgumentParser
from hackalunoonline import HackAlunoOnline
from threading import Thread

# Programa para recuperar os dados de um aluno da UERJ atraves de sua matricula

def get_matriculas_by_name( name ):
	indices    = []
	matriculas = []

	with open( 'nomes-2015.2.txt' , 'r' ) as file:
		for index, line in enumerate( file ) :
			if name in line.strip( '\n' ).lower():
				indices.append( index )

	file = open( 'matriculas-2015.2.txt' , 'r' )

	for indice in indices:
		file.seek( indice * 13 )
		matriculas.append( file.readline() )
		
	file.close()

	return matriculas

def get_data( matricula , verbose , uerjlinks ):
	hao = HackAlunoOnline( matricula.strip( '\n' ) , verbose , uerjlinks )
	print( hao )

def Main():
	parser = ArgumentParser( description = "Recupera informacoes de alunos da UERJ atraves de falhas do sistema academico Aluno Online" )
	
	parser.add_argument( 'matricula' , help = "Matricula do aluno" )

	parser.add_argument( '-i' , '--inputfile' , help = "Utilizar um arquivo contendo uma lista de matriculas com uma matricula por linha como entrada" , action = "store_true" )
	parser.add_argument( '-v' , '--verbose' , help = "Saida com mais conteudo textual" , action = "store_true" )
	parser.add_argument( '-u' , '--uerjlinks' , help = "Links de pdfs da uerj (Em geral arquivos de classificacao no vestibular)" , action = "store_true" )
	parser.add_argument( '-r' , '--reverse' , help = "Procura reversa -> busca matricula por nome (para alunos do IPRJ)" , action = "store_true" )
	
	args = parser.parse_args()

	matriculas = []

	if args.reverse:
		matriculas = get_matriculas_by_name( args.matricula.lower() )
	elif args.inputfile:
		file = open( args.matricula , 'r' )
		matriculas = file.readlines()
	else:
		matriculas.append( args.matricula )

	for matricula in matriculas:
		thread = Thread( target = get_data , args = ( matricula , args.verbose , args.uerjlinks ) )
		thread.start()

# End Main

if __name__ == '__main__':
	Main()