from http import HTTPStatus
import json
from flask import Blueprint, request, jsonify, Response, current_app
from models import Proyecto, db

proyecto = Blueprint('proyecto', __name__)

@proyecto.post('/')
def create():
    keys = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_termino', 'institucion_id', 'usuario_id']
    data = request.get_json()

    with current_app.app_context():
        if not 'nombre' in data.keys():
            return Response(json.dumps({'error': 'El nombre es requerido'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        # Check duplicate values
        count = Proyecto.query.filter(Proyecto.nombre.ilike(data.get('nombre'))).count()
        if count > 0:
            return Response(json.dumps({'error': 'Este proyecto ya se encuentra registrado'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        value = Proyecto()
        
        for item in data.keys():
            if not item in keys:
                return Response(json.dumps({'error': f"El valor '{item}' no corresponde al objeto Proyecto"}),
                        HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')

            setattr(value, item, data.get(item, None))

        db.session.add(value)
        db.session.commit()

    return Response(json.dumps({'message': 'Registro creado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@proyecto.get('/')
def read():
    proyecto = Proyecto.query.all()

    return jsonify(proyecto)


@proyecto.put('/<int:id>')
def update(id):
    keys = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_termino', 'institucion_id', 'usuario_id']
    data = request.get_json()

    with current_app.app_context():
        proyecto = Proyecto.query.filter(Proyecto.id == id).first_or_404()

        if 'nombre' in data.keys():
            count = Proyecto.query.filter(Proyecto.nombre.ilike(data.get('nombre'))).count()

            if count > 0 and proyecto.nombre != data.get('nombre'):
                return Response(json.dumps({'error': 'Este proyecto ya se encuentra registrado'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        for item in data.keys():
            if not item in keys:
                return Response(json.dumps({'error': f"El valor '{item}' no corresponde al objeto Proyecto"}),
                        HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')

            setattr(proyecto, item, data.get(item, None))

        # update in DB
        db.session.commit()

    return Response(json.dumps({'message': 'Registro actualizado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@proyecto.delete('/<int:id>')
def delete(id):
    with current_app.app_context():
        value = Proyecto.query.filter(Proyecto.id==id).first_or_404()
        db.session.delete(value)
        db.session.commit()

    return Response(json.dumps({'message': 'Registro eliminado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@proyecto.get('/terminacion')
def get_dias_terminacion_proyecto():
    '''
    Crear servicio para listar los proyectos que la respuesta sea el nombre del
    proyecto y los días que faltan para su término.
    '''
    from datetime import datetime
    proyectos = Proyecto.query.all()

    if len(proyectos) == 0:
        return Response(json.dumps({'error': 'No se encontraron registros'}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                mimetype='application/json')

    response = []

    for item in proyectos:
        dias_restantes = item.fecha_termino - datetime.now()
        
        response.append({
            'id': item.id,
            'nombre': item.nombre,
            'dias_restantes': dias_restantes.days
        })

    return jsonify(response)