from sys import exception

import azure.functions as func
import logging
from app.core.config import settings
from app.api.ingest import ingest_rss

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="rss/ingest")
async def process_rss(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    response = ingest_rss(req_body)
    return func.HttpResponse(response)


# @app.route(route="http_trigger")
# def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')
#     logging.info(f"Database: {settings.DATABASE_URL}")
#     logging.info(f"Redis: {settings.REDIS_URL}")
#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )