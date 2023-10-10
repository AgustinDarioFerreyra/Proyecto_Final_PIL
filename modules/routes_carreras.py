from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.models.entities import Campus, Carrera, Facultad, Programa, Universidad
from modules.common.gestor_carreras import gestor_carreras
from modules.common.gestor_comun import exportar
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
    return render_template('carreras/carreras.html', carreras=carreras, csrf=csrf, filtros=filtros)

@carreras_bp.route('/carreras/crear', methods=['GET', 'POST'])
@login_required
def crear_carrera():
    formulario_data = {}
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_carreras().crear(**formulario_data)
        if resultado["Exito"]:
            flash('Carrera creada correctamente', 'success')
            return redirect(url_for('routes_carreras.obtener_carreras'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')
    return render_template('carreras/crear_carrera.html', formulario_data=formulario_data, csrf=csrf)

@carreras_bp.route('/carreras/<int:carrera_id>', methods=['POST'])
@login_required
def eliminar_carrera(carrera_id):
    resultado=gestor_carreras().eliminar(carrera_id)
    if resultado["Exito"]:
        flash('Carrera eliminada correctamente', 'success')
    else:
        flash('Error al eliminar carrera', 'success')
    return redirect(url_for('routes_carreras.obtener_carreras'))

@carreras_bp.route('/carreras/generar_excel', methods=['GET', 'POST'])
@login_required
def generar_excel():
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
    carreras_data=[]
    for carrera in carreras:
        cd={}
        cd["Universidad"] = carrera.universidad.nombre
        cd["Facultad"] = carrera.facultad.nombre
        cd["Campus"] = carrera.campus.nombre
        cd["Programa"] = carrera.programa.nombre
        carreras_data.append(cd)
        
    return exportar.exportar_excel(carreras_data)

