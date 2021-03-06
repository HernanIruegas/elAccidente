# version mejorada pero con erroes del runtime memory

# Clase de la memoria en ejecución que contiene:
# 1) Los rangos de las memorias dependiendo de su tipo
# 2) Las estructuras de las memorias
# 3) Métodos para conseguir un valor a partir de una dirección de memoria o bien para asignar un valor a una dirección de memoria

class RuntimeMemory( object ):
	def __init__( self, scope, returnQuad ):

		self.scope = scope
		self.returnQuad = returnQuad

		# Rangos para variables globales
		
		self.gIntStart = 1000
		self.gIntEnd = 1999
		self.gFloatStart = 2000
		self.gFloatEnd = 2999
		self.gBoolStart = 3000
		self.gBoolEnd = 3999
		self.gStringStart = 4000
		self.gStringEnd = 4999

		# Rangos para variables locales
		
		self.lIntStart = 5000
		self.lIntEnd = 5999
		self.lFloatStart = 6000
		self.lFloatEnd = 6999
		self.lBoolStart = 7000
		self.lBoolEnd = 7999
		self.lStringStart = 8000
		self.lStringEnd = 8999

		# Rangos para variables temporales
		
		self.tIntStart = 9000
		self.tIntEnd = 9999
		self.tFloatStart = 10000
		self.tFloatEnd = 10999
		self.tBoolStart = 11000
		self.tBoolEnd = 11999
		self.tStringStart = 12000
		self.tStringEnd = 12999

		# Estructuras para memorias

		self.intMemory = {}
		self.floatMemory = {}
		self.boolMemory = {}
		self.strMemory = {}
		self.tempMemory = {}


	# Recibe una dirección de memoria de un rango conocido, pero se desconoce el tipo al que pertenece dentro de ese rango
	# Determina a que tipo de dato pertenece dentro del rango conocido
	# Regresa el valor almacenado que representa la dirección de memoria
	def getValueFromAddressHelper( self, memoryAddress ):
		#print(f"memoryAddress: {memoryAddress} {self.validateAddress( memoryAddress, self.gIntStart, self.gIntEnd, self.lIntStart, self.lIntEnd )}")
		if self.validateAddress( memoryAddress, self.gIntStart, self.gIntEnd, self.lIntStart, self.lIntEnd ):
		    return self.intMemory[ memoryAddress ]
		elif self.validateAddress( memoryAddress, self.gFloatStart, self.gFloatEnd, self.lFloatStart, self.lFloatEnd ): 
		    return self.floatMemory[ memoryAddress ]
		elif self.validateAddress( memoryAddress, self.gBoolStart, self.gBoolEnd, self.lBoolStart, self.lBoolEnd ):
		    return self.boolMemory[ memoryAddress ]
		elif self.validateAddress( memoryAddress, self.gStringStart, self.gStringEnd, self.lStringStart, self.lStringEnd ):
		    return self.strMemory[ memoryAddress ]
		else:
			#print( self.tempMemory[ memoryAddress ] )
			return self.tempMemory[ memoryAddress ]


	# Recibe una dirección de memoria de un rango conocido, pero se desconoce el tipo al que pertenece dentro de ese rango
	# Determina a que tipo de dato pertenece dentro del rango conocido
	# Asigna un valor a una dirección de memoria dependiendo del tipo al que pertenezca
	def setValueToAddressHelper( self, value, memoryAddress ):

		if self.validateAddress( memoryAddress, self.gIntStart, self.gIntEnd, self.lIntStart, self.lIntEnd ):
			self.intMemory[ memoryAddress ] = value
		elif self.validateAddress( memoryAddress, self.gFloatStart, self.gFloatEnd, self.lFloatStart, self.lFloatEnd ): 
			self.floatMemory[ memoryAddress ] = value
		elif self.validateAddress( memoryAddress, self.gBoolStart, self.gBoolEnd, self.lBoolStart, self.lBoolEnd ):
			self.boolMemory[ memoryAddress ] = value
		elif self.validateAddress( memoryAddress, self.gStringStart, self.gStringEnd, self.lStringStart, self.lStringEnd ):
			self.strMemory[ memoryAddress ] = value
		else: 
			self.tempMemory[ memoryAddress ] = value


	# Valida si una dirección de memoria pertenece a un cierto rango especificado como parametro
	def validateAddress( self, memoryAddress, gStartRange, gEndRange, lStartRange, lEndRange ):

	    if self.scope == "global":
	        return self.validateRange( memoryAddress, gStartRange, gEndRange )
	    else:
	        return self.validateRange( memoryAddress, lStartRange, lEndRange )
	    return False


	# Helper para validar que una dirección de memoria esté dentro de un rango en específico
	def validateRange( self, memoryAddress, startRange, endRange):
		#print(f"memoryAddress {memoryAddress},{startRange},{endRange}")
		if memoryAddress >= startRange and memoryAddress <= endRange:
			return True
		return False


	# Valida si una dirección de memoria pertenece al rango de los temporales
	def ValidateTempAddress( self, memoryAddress, startTempRange, endTempRange ):

	    return self.validateRange( memoryAddress, startTempRange, endTempRange )
