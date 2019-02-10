#!/usr/bin/env python3

import connexion
from flask_cors import CORS

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('swagger.yaml')
CORS(app.app)

if __name__ == '__main__':
    app.run(port=8000)
