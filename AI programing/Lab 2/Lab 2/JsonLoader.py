from json import *

class JsonLoader:
    
	Data = None

	def LoadInJson():
		with open('Variables.json') as Data_File:
			JsonLoader.Data = load(Data_File)
			if JsonLoader.Data:
				print("Json Loaded")