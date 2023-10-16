from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Universidad, Facultad, Campus, Programa, Carrera, TipoPersona, db
from config import registros_por_pagina

class gestor_carreras(ResponseMessage):
	def __init__(self):
		super().__init__()

	campos_obligatorios = {
		'universidad': 'El nombre de la Universidad es obligatorio',
		'facultad': 'El nombre de la Facultad es obligatorio',
		'campus': 'El nombre del Campus es obligatorio',
		'programa': 'El nombre del Programa es obligatorio',
	}

	def _validar_campos_obligatorios(self, kwargs):
		for campo, mensaje in self.campos_obligatorios.items():
			if campo not in kwargs or kwargs[campo]=='':
				self.Exito = False
				self.MensajePorFallo = mensaje
				return False
		return True

	def obtener_pagina(self, pagina, **kwargs):
		query = Carrera.query
		if 'universidad' in kwargs:
			query = query.join(Universidad).filter(Universidad.nombre == kwargs['universidad'])
		if 'facultad' in kwargs:
			query = query.join(Facultad).filter(Facultad.nombre == kwargs['facultad'])
		if 'campus' in kwargs:
			query = query.join(Campus).filter(Campus.nombre == kwargs['campus'])
		if 'programa' in kwargs:
			query = query.join(Programa).filter(Programa.nombre == kwargs['programa'])
		carreras, total_paginas = Carrera.obtener_paginado(query, pagina, registros_por_pagina)
		return carreras, total_paginas

	def obtener(self, id):
		carrera = Carrera.query.get(id)
		if carrera==None:
			self.Exito = False
			self.MensajePorFallo = "La carrera no existe"
			return self.obtenerResultado()
		self.Resultado = carrera
		return self.obtenerResultado()

	def obtener_todo(self):
		return Carrera.query.filter(Carrera.activo==True).all()


	def obtener_universidades(self):
		return db.session.query(Universidad).filter(Universidad.activo==True).distinct().join(Carrera).all()
	

	def obtener_facultades(self, **kwargs):
		resultado = (
			db.session.query(Facultad)
			.filter(Facultad.activo==True)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.filter(Universidad.nombre == kwargs["universidad"])
			.all()
		)
		return resultado
	
	def obtener_campus(self, **kwargs):
		resultado = (
			db.session.query(Campus)
			.filter(Campus.activo==True)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.join(Facultad)
			.filter(Universidad.nombre == kwargs["universidad"])
			.filter(Facultad.nombre == kwargs["facultad"])
			.all()
		)
		return resultado

	def obtener_programas(self, **kwargs):
		resultado = (
			db.session.query(Programa)
			.filter(Programa.activo==True)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.join(Facultad)
			.join(Campus)
			.filter(Universidad.nombre == kwargs["universidad"])
			.filter(Facultad.nombre == kwargs["facultad"])
			.filter(Campus.nombre == kwargs["campus"])
			.all()
		)
		return resultado

	def obtener_roles(self, **kwargs):
		resultado = (
			db.session.query(TipoPersona).all()
		)
		return resultado
	

	def obtener_con_filtro(self, **kwargs):
		query = Carrera.query.filter(Carrera.activo==True)
		if 'universidad' in kwargs:
			query = query.join(Universidad).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
		if 'facultad' in kwargs:
			query = query.join(Facultad).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
		if 'campus' in kwargs:
			query = query.join(Campus).filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
		if 'programa' in kwargs:
			query = query.join(Programa).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
		return query.all() if any(kwargs.values()) else []
	
	def eliminar(self, id):
		carrera = Carrera.query.get(id)
		if carrera==None:
			self.Exito = False
			self.MensajePorFallo = "La carrera no existe"
			return self.obtenerResultado()
		resultado_borrar=carrera.activar(False)
		self.Exito=resultado_borrar["Exito"]
		self.MensajePorFallo=resultado_borrar["MensajePorFallo"]
		return self.obtenerResultado()


	def crear(self, **kwargs):
		if not self._validar_campos_obligatorios(kwargs):
			return self.obtenerResultado()

		universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
		facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
		campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
		programa=Programa.crear_y_obtener(nombre=kwargs['programa'])

		nueva_carrera=Carrera(universidad=universidad, facultad=facultad, campus=campus, programa=programa)

		resultado_crear=nueva_carrera.guardar()
		self.Resultado=resultado_crear["Resultado"]
		self.Exito=resultado_crear["Exito"]
		self.MensajePorFallo=resultado_crear["MensajePorFallo"]

		return self.obtenerResultado()


	def editar(self, id, **kwargs):
		carrera = Carrera.query.get(id)
		if carrera==None:
			self.Exito = False
			self.MensajePorFallo = "La carrera no existe"
			return self.obtenerResultado()

		#Validaciones
		for campo, mensaje in self.campos_obligatorios.items():
			if campo in kwargs and kwargs[campo]=='':
				self.Exito = False
				self.MensajePorFallo = mensaje
				return self.obtenerResultado()

		universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
		facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
		campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
		programa=Programa.crear_y_obtener(nombre=kwargs['programa'])

		carrera.universidad=universidad
		carrera.facultad=facultad
		carrera.campus=campus
		carrera.programa=programa

		resultado_editar=carrera.guardar()
		self.Exito=resultado_editar["Exito"]
		self.MensajePorFallo=resultado_editar["MensajePorFallo"]
		return self.obtenerResultado()