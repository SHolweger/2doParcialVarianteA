from flask import Blueprint, request, current_app, jsonify
from models import Cliente, Asunto, Procurador, Abogado, Audiencia, Incidencia

replicacion_bp = Blueprint("replicacion", __name__)

# --- UTILIDAD GENERAL ---
def get_session():
    return current_app.config["SESSION_LOCAL"]

# --- CLIENTE ---
@replicacion_bp.route("/v1/replicar_cliente", methods=["POST", "PUT"])
def replicar_cliente():
    session = get_session()
    data = request.get_json()
    try:
        cliente = Cliente(**data)
        session.merge(cliente)
        session.commit()
        return jsonify({"message": "Cliente replicado/actualizado con éxito"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# --- ASUNTO ---
@replicacion_bp.route("/v1/replicar_asunto", methods=["POST", "PUT"])
def replicar_asunto():
    session = get_session()
    data = request.get_json()
    try:
        asunto = Asunto(**data)
        session.merge(asunto)
        session.commit()
        return jsonify({"message": "Asunto replicado/actualizado con éxito"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# --- PROCURADOR ---
@replicacion_bp.route("/v1/replicar_procurador", methods=["POST", "PUT"])
def replicar_procurador():
    session = get_session()
    data = request.get_json()
    try:
        procurador = Procurador(**data)
        session.merge(procurador)
        session.commit()
        return jsonify({"message": "Procurador replicado/actualizado con éxito"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# --- ABOGADO ---
@replicacion_bp.route("/v1/replicar_abogado", methods=["POST", "PUT"])
def replicar_abogado():
    session = get_session()
    data = request.get_json()
    try:
        abogado = Abogado(**data)
        session.merge(abogado)
        session.commit()
        return jsonify({"message": "Abogado replicado/actualizado con éxito"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# --- AUDIENCIA ---
@replicacion_bp.route("/v1/replicar_audiencia", methods=["POST", "PUT"])
def replicar_audiencia():
    session = get_session()
    data = request.get_json()
    try:
        audiencia = Audiencia(**data)
        session.merge(audiencia)
        session.commit()
        return jsonify({"message": "Audiencia replicada/actualizada con éxito"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# --- INCIDENCIA ---
@replicacion_bp.route("/v1/replicar_incidencia", methods=["POST", "PUT"])
def replicar_incidencia():
    session = get_session()
    data = request.get_json()
    try:
        incidencia = Incidencia(**data)
        session.merge(incidencia)
        session.commit()
        return jsonify({"message": "Incidencia replicada/actualizada con éxito"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
