import json
from flask import Blueprint, request, jsonify, Response, current_app
from models import Usuario, Proyecto, db
from http import HTTPStatus

usuario = Blueprint('usuario', __name__)

@usuario.post('/')
def create():
    keys = ['nombres', 'apellidos', 'rut', 'fecha_nacimiento', 'cargo', 'edad']
    data = request.get_json()

    if not 'nombres' in data.keys():
        return Response(json.dumps({'error': 'Los nombres son requeridos'}),
                HTTPStatus.BAD_REQUEST,
                mimetype='application/json')
                
    if not 'apellidos' in data.keys():
        return Response(json.dumps({'error': 'Los apellidos son requeridos'}),
                HTTPStatus.BAD_REQUEST,
                mimetype='application/json')

    if not 'rut' in data.keys():
        return Response(json.dumps({'error': 'El RUT es requerido'}),
                HTTPStatus.BAD_REQUEST,
                mimetype='application/json')

    if not 'fecha_nacimiento' in data.keys() or data.get('fecha_nacimiento') == '':
        return Response(json.dumps({'error': 'La fecha de nacimiento es requerida'}),
                HTTPStatus.BAD_REQUEST,
                mimetype='application/json')

    if not 'cargo' in data.keys():
        return Response(json.dumps({'error': 'El cargo es requerido'}),
                HTTPStatus.BAD_REQUEST,
                mimetype='application/json')

    with current_app.app_context():
        # Check duplicate values
        count = Usuario.query.filter(Usuario.nombres.ilike(data.get('nombres'))).count()
        if count > 0:
            return Response(json.dumps({'error': 'Este usuario ya se encuentra registrado'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        value = Usuario()
        
        for item in data.keys():
            if not item in keys:
                return Response(json.dumps({'error': f"El valor '{item}' no corresponde al objeto Usuario"}),
                        HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')

            setattr(value, item, data.get(item, None))

        if not 'edad' in data.keys():
            from dateutil import relativedelta
            from datetime import datetime

            fecha_nacimiento = datetime.strptime(data.get('fecha_nacimiento'), '%Y-%m-%d')
            delta = relativedelta.relativedelta(datetime.now(), fecha_nacimiento)

            setattr(value, 'edad', delta.years)

        db.session.add(value)
        db.session.commit()

    return Response(json.dumps({'message': 'Registro creado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@usuario.get('/')
def read():
    data = Usuario.query.all()

    return jsonify(data)


@usuario.put('/<int:id>')
def update(id):
    keys = ['nombres', 'apellidos', 'rut', 'fecha_nacimiento', 'cargo', 'edad']
    data = request.get_json()

    with current_app.app_context():
        usuario = Usuario.query.filter(Usuario.id == id).first_or_404()

        if 'nombre' in data.keys():
            count = Usuario.query.filter(Usuario.nombre.ilike(data.get('nombre'))).count()

            if count > 0 and usuario.nombre != data.get('nombre'):
                return Response(json.dumps({'error': 'Este usuario ya se encuentra registrada'}),
                    HTTPStatus.BAD_REQUEST,
                    mimetype='application/json')

        for item in data.keys():
            if not item in keys:
                return Response(json.dumps({'error': f"El valor '{item}' no corresponde al objeto Usuario"}),
                        HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')

            setattr(usuario, item, data.get(item, None))

        # update in DB
        db.session.commit()

    return Response(json.dumps({'message': 'Registro actualizado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@usuario.delete('/<int:id>')
def delete(id):
    with current_app.app_context():
        value = Usuario.query.filter(Usuario.id==id).first_or_404()
        db.session.delete(value)
        db.session.commit()

    return Response(json.dumps({'message': 'Registro eliminado exitosamente'}),
            HTTPStatus.OK,
            mimetype='application/json')


@usuario.post('/search/rut')
def get_by_rut():
    '''
    Crear servicio para listar un usuario (filtro por Rut)
    con sus respectivos proyectos.
    
    Response => 404 usuario no encontrado | 200 OK
    '''
    data = request.get_json()
    rut_value  = data.get('rut', None)

    if rut_value is None or rut_value == '':
        return Response(json.dumps({'error': 'El RUT no puede estar vacío'}),\
                HTTPStatus.BAD_REQUEST,\
                mimetype='application/json')

    filtro_usuario = Usuario.query.filter(Usuario.rut.ilike(rut_value)).\
            outerjoin(Proyecto).\
            first_or_404()

    response = {
        'id': filtro_usuario.id,
        'nombres': filtro_usuario.nombres,
        'apellidos': filtro_usuario.apellidos,
        'rut': filtro_usuario.rut,
        'fecha_nacimiento': filtro_usuario.fecha_nacimiento.strftime('%d-%m-%Y %H:%M:%S'),
        'cargo': filtro_usuario.cargo,
        'edad': filtro_usuario.edad
    }

    proyectos = []

    for proyecto in filtro_usuario.proyectos:
        value = {
            'id': proyecto.id,
            'nombre': proyecto.nombre,
        }

        proyectos.append(value)

    response['proyectos'] = proyectos if len(proyectos) > 0 else None
    return jsonify(response)
