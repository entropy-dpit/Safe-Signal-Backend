# Copyright (c) Team Entropy 2020
# All rights reserved

__author__ = 'David Pescariu'

from waitress import serve
from flask import Flask
from flask import request
import api.request_handler as handler

api = Flask(__name__)

def start_serving(config) -> None:
    """
    Start serving the API

    Args:
        config (models.Config): configs (instance of Config)
    """
    
    @api.route("/", methods=["GET"])
    def base() -> dict:
        return handler.handle_base(request)

    @api.route("/public", methods=["GET"])
    def public() -> dict:
        return handler.handle_public(request, config)

    @api.route("/get_markers", methods=["GET"])
    def get_markers() -> dict:
        return handler.handle_get_markers(request, config)

    @api.route("/add_marker", methods=["GET"])
    def add_marker() -> dict:
        return handler.handle_add_marker(request, config)

    @api.route("/del_markers", methods=["GET"])
    def del_markers() -> dict:
        return handler.handle_del_markers(request, config)

    @api.route("/get_zones", methods=["GET"])
    def get_zones() -> dict:
        return handler.handle_get_zones(request, config)

    @api.route("/add_zone", methods=["GET"])
    def add_zone() -> dict:
        return handler.handle_add_zone(request, config)

    @api.route("/del_zone", methods=["GET"])
    def del_zone() -> dict:
        return handler.handle_del_zone(request, config)

    serve(
        api,
        port=int(config.SERVE_PORT),
        ipv6=False
    )