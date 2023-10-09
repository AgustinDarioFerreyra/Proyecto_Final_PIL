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
    universidad = request.args.get('universidad', default="", type=str)
    facultad = request.args.get('facultad', default="", type=str)
    campus = request.args.get('campus', default="", type=str)
    programa = request.args.get('programa', default="", type=str)
    filtros = {
        'universidad': universidad,
        'facultad': facultad,
        'campus':campus,
        'programa': programa
    }
    carreras = gestor_carreras().obtener_con_filtro(**filtros)
    return render_template('carreras/carreras.html', carreras = carreras, csrf=csrf, filtros=filtros)

@carreras_bp.route('/carreras/<int:carrera_id>', methods=['POST'])
@login_required
def eliminar_carrera(carrera_id):
    resultado=gestor_carreras().eliminar(carrera_id)
    if resultado["Exito"]:
        flash('Carrera eliminada correctamente', 'success')
    else:
        flash('Error al eliminar carrera', 'success')
    return redirect(url_for('routes_carreras.obtener_carreras'))
