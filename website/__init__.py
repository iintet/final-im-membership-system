from flask import Flask, session
from .views import views
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.secret_key = 'p0w3rpuffG1RL$!'
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.template_folder = 'templates'
    app.static_folder = 'static'

    @app.route('/test')
    def test_connection():
        from .supabase_client import supabase
        try:
            response = supabase.table('member').select('*').limit(1).execute()
            return {"connected": True, "data": response.data}, 200
        except Exception as e:
            return {"connected": False, "error": str(e)}, 500

    return app