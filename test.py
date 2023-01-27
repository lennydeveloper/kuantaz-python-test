from app import db, app
from models import Institucion, Proyecto, Usuario

def test_limpiar_bd() -> None:
    with app.app_context():
        db.drop_all()
        db.create_all()

        count_institucion = Institucion.query.count()
        count_proyectos = Proyecto.query.count()
        count_usuarios = Usuario.query.count()

        assert count_institucion == 0 and count_proyectos == 0 and count_usuarios == 0


def test_agregar_institucion() -> None:
    with app.app_context():
        descripcion_ins = 'Descripcion de n1'
        direccion_ins = 'Calle 1'
        nombre_ins = 'Institucion n1'

        institucion = Institucion(descripcion=descripcion_ins, direccion=direccion_ins,\
                        nombre=nombre_ins)

        db.session.add(institucion)
        db.session.commit()

        assert Institucion.query.count() == 1


def test_agregar_usuario() -> None:
    with app.app_context():
        from datetime import datetime 

        nombre_usuario = 'Javier'  
        apellido_usuario = 'Castro'
        rut_usuario = 'A1234567890'
        cargo_usuario = 'Cargo de prueba'
        edad_usuario = 26
        fecha = datetime.strptime('13-07-1996', '%d-%m-%Y')

        usuario = Usuario(nombres=nombre_usuario, apellidos=apellido_usuario, rut=rut_usuario,\
                    fecha_nacimiento=fecha, cargo=cargo_usuario, edad=edad_usuario) 

        db.session.add(usuario)
        db.session.commit()

        assert Usuario.query.count() == 1


def test_agregar_proyecto() -> None:
    with app.app_context():
        from datetime import datetime, timedelta

        nombre_proyecto = 'Proyecto de prueba'
        fecha_fin = datetime.now() + timedelta(days=30)
        proyecto = Proyecto(nombre=nombre_proyecto, fecha_termino=fecha_fin) 

        usuario = Usuario.query.filter_by(id=1).first()
        institucion = Institucion.query.filter_by(id=1).first()

        usuario.proyectos.append(proyecto)
        institucion.proyectos.append(proyecto)

        db.session.add(proyecto)
        db.session.commit()

        assert Proyecto.query.count() == 1


def test_editar_proyecto() -> None:
    with app.app_context():
        nombre_proyecto = 'Proyecto de prueba - editado'
        proyecto = Proyecto.query.filter_by(id=1).first()

        proyecto.nombre = nombre_proyecto
        db.session.commit()

        get_proyecto = Proyecto.query.filter_by(id=1).first()
        assert get_proyecto.nombre == nombre_proyecto


def test_eliminar_usuario() -> None:
    with app.app_context():
        usuario = Usuario.query.filter_by(id=1).first()

        db.session.delete(usuario)
        db.session.commit()

        # proyecto => (institucion_id=1, usuario_id=None) -> ondelete = 'SET NULL' (default -> None)
        assert Usuario.query.count() == 0


def test_fk_institucion_proyectos() -> None:
    '''
    Este test evalúa las referencias entre Institución y Proyecto
    
    assert => El proyecto debe tener la institución referenciada
    '''
    with app.app_context():
        filtro_institucion = Institucion.query.filter_by(id=1).\
                                outerjoin(Proyecto).\
                                first()

        assert filtro_institucion.proyectos is not None


def test_eliminar_institucion() -> None:
    with app.app_context():
        institucion = Institucion.query.filter_by(id=1).first()

        db.session.delete(institucion)
        db.session.commit()

        assert Institucion.query.count() == 0


def test_eliminar_usuario() -> None:
    with app.app_context():
        usuario = Usuario.query.filter_by(id=1).first()

        db.session.delete(usuario)
        db.session.commit()

        assert Usuario.query.count() == 0


def test_check_fk_proyectos() -> None:
    '''
    Este test evalúa las referencias que tiene el proyecto con usuario e institución
    
    assert => El proyecto debe tener institucion_id = None && proyecto_id = None
    '''
    with app.app_context():
        proyecto = Proyecto.query.filter_by(id=1).first()

        assert proyecto.institucion_id is None and proyecto.usuario_id is None


def test_eliminar_proyecto() -> None:
    with app.app_context():
        nombre_edit = 'Proyecto de prueba - editado'
        proyecto = Proyecto.query.filter_by(nombre=nombre_edit).first()

        db.session.delete(proyecto)
        db.session.commit()

        assert Proyecto.query.count() == 0
