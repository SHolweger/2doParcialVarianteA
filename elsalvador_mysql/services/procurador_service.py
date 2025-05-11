from flask import jsonify
from models import Procurador

def get_procuradores(SessionLocal):
    try:
        session = SessionLocal()
        procuradores = session.query(Procurador).all()
        return jsonify([
            {
                "id": p.id_procurador,
                "nombre": p.nombre,
                "apellido": p.apellido,
                "telefono": p.telefono,
                "email": p.email
            }
            for p in procuradores
        ])
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500

def create_procurador(data, SessionLocal):
    session = SessionLocal()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    telefono = data.get("telefono")
    email = data.get("email")

    if not all([nombre, apellido, telefono, email]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        procurador = Procurador(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email
        )
        session.add(procurador)
        session.commit()
        return jsonify({"message": "Procurador creado correctamente", "status": 201})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def update_procurador(id, data, SessionLocal):
    session = SessionLocal()
    procurador = session.query(Procurador).filter_by(id_procurador=id).first()
    if not procurador:
        return jsonify({"error": "Procurador no encontrado", "status": 404})

    try:
        if data.get("telefono"):
            procurador.telefono = data.get("telefono")
        if data.get("email"):
            procurador.email = data.get("email")

        session.commit()
        return jsonify({"message": "Procurador actualizado correctamente", "status": 200})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()
