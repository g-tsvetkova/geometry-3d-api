# # from flask import Flask


# # def create_app():
# #     app = Flask(__name__)

# #     # Initialize Flask extensions here

# #     # Register blueprints here

# #     @app.route("/test/")
# #     def test_page():
# #         return "<h1>Testing the Flask Application Factory Pattern</h1>"

# #     return app

# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # File: app/main/__init__.py
# # Description: Application factory


# from flask import Flask
# from flasgger import Swagger
# from app.points.routes import bp_points
# from app.polygons.routes import bp_polygons
# from app.mesh.routes import bp_meshes


# def create_app(config_name):
#     app = Flask(__name__)
#     # initialize Swagger
#     swagger = Swagger(app, template_file="../config/swagger.yml")

#     try:
#         # Register blueprints
#         app.register_blueprint(bp_points)
#         app.register_blueprint(bp_polygons)
#         app.register_blueprint(bp_meshes)
#     except Exception as e:
#         print(f"An error occurred when registering blueprints: {e}")

#     return app

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: app/__init__.py
# Description: Application factory


from flask import Flask
from flasgger import Swagger
from .routes.point_routes import bp_points
from .routes.polygon_routes import bp_polygons
from .routes.mesh_routes import bp_meshes


def create_app():
    app = Flask(__name__)
    # initialize Swagger
    swagger = Swagger(app, template_file="config/swagger.yml")

    try:
        # Register blueprints
        app.register_blueprint(bp_points)
        app.register_blueprint(bp_polygons)
        app.register_blueprint(bp_meshes)
    except Exception as e:
        print(f"An error occurred when registering blueprints: {e}")

    return app
