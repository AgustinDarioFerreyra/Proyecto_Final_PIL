from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Universidad, Facultad, Campus, Programa, Carrera, TipoPersona, db


class gestor_carreras(ResponseMessage):
	def __init__(self):
		super().__init__()

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
	

	# def obtener_con_filtro(self, **kwargs):
	# 	query = Carrera.query.filter(Carrera.activo==True)
	# 	if 'universidad' in kwargs:
	# 		query = query.filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
	# 	if 'facultad' in kwargs:
	# 		query = query.filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
	# 	if 'campus' in kwargs:
	# 		query = query.filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
	# 	if 'programa' in kwargs:
	# 		query = query.filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
	# 	return query.all() if any(kwargs.values()) else []


	# def obtener_con_filtro(self, **kwargs):
	# 	query = Carrera.query.filter(Carrera.activo==True)
	# 	if 'universidad' in kwargs:
	# 		query = query.join(Universidad).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
	# 	if 'facultad' in kwargs:
	# 		query = query.join(Facultad).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
	# 	if 'campus' in kwargs:
	# 		query = query.join(Campus).filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
	# 	if 'programa' in kwargs:
	# 		query = query.join(Programa).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
	# 	return query.all() if any(kwargs.values()) else []

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