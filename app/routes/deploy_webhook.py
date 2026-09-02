import os
import subprocess
from flask import Blueprint, request, jsonify

deploy_bp = Blueprint("deploy", __name__, url_prefix="/api/deploy")

@deploy_bp.route("", methods=["POST"])
def deploy():
    expected_token = os.environ.get("DEPLOY_SECRET_TOKEN", "jet_hr_secret_token_2026")
    provided_token = request.headers.get("X-Deploy-Token") or request.args.get("token")

    if not provided_token or provided_token != expected_token:
        return jsonify({"status": "forbidden", "message": "Token di deploy non valido"}), 403

    try:
        # Esegue git pull nel repository
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cmd_output = subprocess.check_output(
            ["git", "pull", "origin", "main"],
            cwd=repo_dir,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Se siamo su PythonAnywhere, tocca il file wsgi per ricaricare l'app web
        wsgi_path = os.environ.get("WSGI_FILE_PATH")
        if wsgi_path and os.path.exists(wsgi_path):
            os.utime(wsgi_path, None)

        return jsonify({
            "status": "success",
            "message": "Aggiornamento completato con successo",
            "git_output": cmd_output
        }), 200
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": "Errore durante il git pull",
            "output": e.output
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
