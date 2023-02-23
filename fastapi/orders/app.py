import yaml

from pathlib import Path
from fastapi import FastAPI

app = FastAPI(
    debug=True,
    openapi_url='/openapi/kitchen.json',
    docs_url='/docs/kitchen',
)

oas_doc = yaml.safe_load(
    (Path(__file__).parent / './oas.yaml').read_text()
)

app.openapi = lambda: oas_doc

from api import api
