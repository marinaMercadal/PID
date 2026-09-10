from flask import Blueprint, request, jsonify
from flask.views import MethodView

from app.agenda.service import AgendaService
from app.agenda.validators import BloqueAgendaInvalido

agenda_bp = Blueprint("agenda", __name__, url_prefix="/agenda")


class AgendaResource(MethodView):
    def __init__(self):
        self.service = AgendaService()

    def post(self):
        data = request.get_json() or {}
        usuario_id = data.get("usuario_id")

        try:
            resultado = self.service.crear_bloque(usuario_id, data)
        except BloqueAgendaInvalido as e:
            return jsonify({"error": str(e)}), 400

        return jsonify(resultado), 201

    def get(self):
        usuario_id = request.args.get("usuario_id", type=int)
        resultado = self.service.listar_bloques(usuario_id)
        return jsonify(resultado), 200


agenda_bp.add_url_rule(
    "", view_func=AgendaResource.as_view("agenda_resource")
)