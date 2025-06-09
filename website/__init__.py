from flask import Flask
from flask_supabase import Supabase
from dotenv import load_dotenv
import os

load_dotenv()
supabase_extension = Supabase()

def create_app():
    app = Flask(__name__)
    app.config['SUPABASE_URL'] = os.getenv("SUPABASE_URL")
    app.config['SUPABASE_KEY'] = os.getenv("SUPABASE_KEY")
    
    supabase_extension.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    @app.route('/test')
    def test_connection():
        try:
            response = supabase_extension.client.table('member').select('*').limit(1).execute()
            return {"connected": True, "data": response.data}, 200
        except Exception as e:
            return {"connected": False, "error": str(e)}, 500

    return app