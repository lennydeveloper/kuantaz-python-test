from http import HTTPStatus
from flask import Blueprint, jsonify, request, Response, current_app
from models import Institucion, Proyecto, Usuario, db
import json

institucion = Blueprint('institucion', __name__)

@institucion.post('/')
def create():
    keys = ['nombre', 'descripcion', 'direccion', 'fecha_creacion']
    data = request.get_json()

    with current_app.app_context():
        if not 'nombre' in data.keys():
            return Response(json.dumps({'error': 'El nombre es requerido'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        if not 'direccion' in data.keys():
            return Response(json.dumps({'error': 'La dirección es requerida'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        # Check duplicate values
        count = Institucion.query.filter(Institucion.nombre.ilike(data.get('nombre'))).count()
        if count > 0:
            return Response(json.dumps({'error': 'Esta institución ya se encuentra registrada'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        value = Institucion()
        
        for item in data.keys():
            if not item in keys:
                return Response(json.dumps({'error': f"El valor '{item}' no corresponde al objeto Institución"}),
                        HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')

            setattr(value, item, data.get(item, None))

        db.session.add(value)
        db.session.commit()

    return Response(json.dumps({'message': 'Registro creado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@institucion.get('/')
def read():
    data = Institucion.query.all()

    return jsonify(data)


@institucion.put('/<int:id>')
def update(id):
    keys = ['nombre', 'descripcion', 'direccion', 'fecha_creacion']
    data = request.get_json()

    with current_app.app_context():
        institucion = Institucion.query.filter(Institucion.id == id).first_or_404()

        if 'nombre' in data.keys():
            count = Institucion.query.filter(Institucion.nombre.ilike(data.get('nombre'))).count()

            if count > 0 and institucion.nombre != data.get('nombre'):
                return Response(json.dumps({'error': 'Esta institución ya se encuentra registrada'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        for item in data.keys():
            if not item in keys:
                return Response(json.dumps({'error': f"El valor '{item}' no corresponde al objeto Institución"}),
                        HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')

            setattr(institucion, item, data.get(item, None))

        # update in DB
        db.session.commit()

    return Response(json.dumps({'message': 'Registro actualizado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@institucion.delete('/<int:id>')
def delete(id):
    with current_app.app_context():
        value = Institucion.query.filter(Institucion.id==id).first_or_404()
        db.session.delete(value)
        db.session.commit()

    return Response(json.dumps({'message': 'Registro eliminado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@institucion.get('/direcciones')
def obtener_direcciones():
    '''
    Crear servicio para listar instituciones donde a cada institución se agregue a la dirección
    la ubicación de google maps ejemplo: “https://www.google.com/maps/search/+ direccion” y la
    abreviación del nombre (solo los primeros tres caracteres).
    '''
    instituciones = Institucion.query.all()
    cp_value = instituciones.copy()

    for item in cp_value:
        # Google maneja como separador (espacio) el operador '+'
        format_direccion = item.direccion.replace(' ', '+').lower()
        format_nombre = item.nombre[:3].lower()
        
        val = f'https://www.google.com/maps/search/{format_direccion}/{format_nombre}'
        item.direccion = val

    return jsonify(cp_value)


@institucion.get('/search/<int:id>')
def get_by_id(id):
    '''
    Crear servicio para listar una institución (Filtro por id) con sus respectivos
    proyectos y responsable del proyecto.

    Response => 404 institución no encontrada | 200 OK
    '''
    filtro_institucion = Institucion.query.filter_by(id=id).\
            outerjoin(Proyecto).\
            outerjoin(Usuario).\
            first_or_404()

    response = {
        'id': filtro_institucion.id,
        'nombre': filtro_institucion.nombre,
        'descripcion': filtro_institucion.descripcion,
        'direccion': filtro_institucion.direccion,
        'fecha_creacion': filtro_institucion.fecha_creacion.strftime('%d-%m-%Y %H:%M:%S')
    }

    proyectos = []

    for proyecto in filtro_institucion.proyectos:
        usuario = proyecto.usuario
        value = {
            'id': proyecto.id,
            'nombre': proyecto.nombre,
        }

        if usuario is not None:
            value['usuario'] = {
                'id': usuario.id,
                'nombre': f'{usuario.nombres} {usuario.apellidos}'
            }

        proyectos.append(value)

    response['proyectos'] = proyectos if len(proyectos) > 0 else None
    return jsonify(response)
