PHONY: fastapi_run flask_run

PY_DIR_FASTAPI = fastapi
PY_DIR_FLASKAPI = flaskapi

fastapi_run:
	cd $(PY_DIR_FASTAPI) && uvicorn orders.app:app --reload

flask_run:
	cd $(PY_DIR_FLASKAPI) && flask run --reload

