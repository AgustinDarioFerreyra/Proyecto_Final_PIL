from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.models.entities import Campus, Carrera, Facultad, Programa, Universidad
from modules.common.gestor_carreras import gestor_carreras
from flask import Blueprint
from modules.auth import csrf


carreras_bp = Blueprint('routes_carreras', __name__)

@carreras_bp.route('/carreras', methods=['GET'])
@login_required
def obtener_carreras():
    programa_nombre = request.args.get('programa_nombre')
    facultad_nombre = request.args.get('facultad_nombre')
    universidad_nombre = request.args.get('universidad_nombre')
    campus_nombre = request.args.get('campus_nombre')

    carreras = Carrera.query

    if programa_nombre:
        carreras = carreras.join(Programa).filter(Programa.nombre == programa_nombre)

    if facultad_nombre:
        carreras = carreras.join(Facultad).filter(Facultad.nombre == facultad_nombre)
        
    if universidad_nombre:
        carreras = carreras.join(Universidad).filter(Universidad.nombre == universidad_nombre)

    if campus_nombre:
        carreras = carreras.join(Campus).filter(Campus.nombre == campus_nombre)

    carreras = carreras.all()
    return render_template('carreras/carreras.html', carreras = carreras)