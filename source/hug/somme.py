"""Simple application effectuant une somme de deux nombres"""
import hug

@hug.get()
def somme(val1, val2):
  	"""Retourne la somme des deux nombres passés en paramètre"""
  	return val1 + val2
