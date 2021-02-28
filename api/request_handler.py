# Copyright (c) prisma.ai 2021
# All rights reserved

__author__ = 'David Pescariu'

from datetime import datetime
import utils.console_messages as msg
import api.db_connector as db
from models.types import TYPES

def isValidKey(_type: str, key: str, config) -> bool:
    """
    Checks if a given key is valid

    Args:
        _type (str): "public" / "private"
        key (str): Recieved key
        config (models.Config): Config instance

    Returns:
        bool: If key is valid true else false
    """
    if _type == "public":
        try:
            if config.PUBLIC_KEYS[key] == "valid":
                return True 
            else:
                msg.fail(f"Invalid key: {key}")
                return False
        except KeyError:
            msg.fail(f"Non-existant key: {key}")
            return False
    elif _type == "private":
        try:
            if config.PRIVATE_KEYS[key] == "valid":
                return True 
            else:
                msg.fail(f"Invalid key: {key}")
                return False
        except KeyError:
            msg.fail(f"Non-existant key: {key}")
            return False
    else:
        msg.debug("In method isValidKey :: Invalid type of key")
        return False

################################################################################
################################### PUBLIC #####################################
################################################################################

def handle_base(req) -> dict:
    """
    Handle the root page, show some info

    Args:
        req (werkzeug.local.LocalProxy): Flask request

    Returns:
        dict: Response
    """
    return {
            "safe-signal-api-v3":
                f"server_datetime={datetime.now()}," + 
                f"incoming_ip={req.remote_addr}," +
                f"incoming_headers={req.headers}" 
        }

def handle_public(req, config) -> dict:
    """
    Handle the public request

    Args:
        req (werkzeug.local.LocalProxy): Flask request
        config (models.Config): Config instance

    Returns:
        dict: Response
    """
    if not config.ALLOW_PUBLIC:
        return dict(UNAVAILABLE="PUBLIC_REQUESTS_NOT_AVAILABLE_AT_THIS_TIME")

    key = req.args.get('key')
    # If the key is invalid just return INVALID_KEY
    if not isValidKey("public", key, config):
        msg.fail(f"Requested from {req.remote_addr}")
        return dict(FAIL="INVALID_KEY")

    return dict(UNIMPLEMENTED="NOT_IMPLEMENTED_YET")

################################################################################
################################## MARKERS #####################################
################################################################################

def handle_get_markers(req, config) -> dict:
    """
    Handle the get markers call

    Args:
        req (werkzeug.local.LocalProxy): Flask request
        config (models.Config): Config instance

    Returns:
        dict: Response
    """
    key = req.args.get('key')
    # If the key is invalid just return INVALID_KEY
    if not isValidKey("private", key, config):
        msg.fail(f"Requested from {req.remote_addr}")
        return dict(FAIL="INVALID_KEY")

    _lat, _long = req.args.get('lat'), req.args.get('long')
    
    # Convert to ints
    try:
        recv_lat, recv_long = int(float(_lat)), int(float(_long))
    except ValueError:
        return dict(FAIL="INVALID_DATA")
    
    msg.info(f"[REQ_GET_MKS] Received request from {req.remote_addr} for lat: {recv_lat} and long: {recv_long}")
    try:
        markers = db.return_markers(config, recv_lat, recv_long)
        return dict(data=markers)
    except Exception as e:
        msg.exception(e)
        return dict(FAIL="UNKNOWN_FAIL")

def handle_add_marker(req, config) -> dict:
    """
    Handle the add marker call

    Args:
        req (werkzeug.local.LocalProxy): Flask request
        config (models.Config): Config instance

    Returns:
        dict: Response
    """
    key = req.args.get('key')
    # If the key is invalid just return INVALID_KEY
    if not isValidKey("private", key, config):
        msg.fail(f"Requested from {req.remote_addr}")
        return dict(FAIL="INVALID_KEY")

    _lat, _long, _type = req.args.get('lat'), req.args.get('long'), req.args.get('type')
    
    # Convert to float
    try:
        recv_lat, recv_long = float(_lat), float(_long)
    except ValueError:
        return dict(FAIL="INVALID_DATA")

    # Check to see if the type is valid
    try:
        if TYPES[_type] == "valid": pass
    except KeyError:
        msg.debug(f"[RUNTIME_DEBUG] Type {_type} is NOT valid!")
        return dict(FAIL="INVALID_TYPE")

    msg.info(f"[REQ_ADD_MKS] Received request from {req.remote_addr} for lat: {recv_lat}, long: {recv_long} and type: {_type}")
    try:
        response = db.add_marker(config, recv_lat, recv_long, _type)
        if response == 0:
            return dict(SUCCESS="DATA_ADDED")
        else:
            msg.fail(f"Recieved {response} from method add_marker")
            return dict(FAIL=str(response))
    except Exception as e:
        msg.exception(e)
        return dict(FAIL="UNKNOWN_FAIL")

def handle_del_markers(req, config) -> dict:
    """
    Handle the delete markers call

    Args:
        req (werkzeug.local.LocalProxy): Flask request
        config (models.Config): Config instance

    Returns:
        dict: Response
    """
    key = req.args.get('key')
    # If the key is invalid just return INVALID_KEY
    if not isValidKey("private", key, config):
        msg.fail(f"Requested from {req.remote_addr}")
        return dict(FAIL="INVALID_KEY")

    _lat, _long = req.args.get('lat'), req.args.get('long')
    
    # Convert to float
    try:
        recv_lat, recv_long = float(_lat), float(_long)
    except ValueError:
        return dict(FAIL="INVALID_DATA")

    msg.info(f"[REQ_DEL_MKS] Received DELETE request from {req.remote_addr} for lat: {recv_lat}, long: {recv_long}")
    try:
        response = db.del_markers(config, recv_lat, recv_long)
        if response == 0:
            return dict(SUCCESS="DATA_DELETED")
        else:
            msg.fail(f"Recieved {response} from method del_markers")
            return dict(FAIL=str(response))
    except Exception as e:
        msg.exception(e)
        return dict(FAIL="UNKNOWN_FAIL")

################################################################################
################################### ZONES ######################################
################################################################################

def handle_get_zones(req, config) -> dict:
    """
    Handle the get zones call

    Args:
        req (werkzeug.local.LocalProxy): Flask request
        config (models.Config): Config instance

    Returns:
        dict: Response
    """
    key = req.args.get('key')
    # If the key is invalid just return INVALID_KEY
    if not isValidKey("private", key, config):
        msg.fail(f"Requested from {req.remote_addr}")
        return dict(FAIL="INVALID_KEY")

    _lat, _long = req.args.get('lat'), req.args.get('long')
    
    # Convert to ints
    try:
        recv_lat, recv_long = int(float(_lat)), int(float(_long))
    except ValueError:
        return dict(FAIL="INVALID_DATA")
    
    msg.info(f"[REQ_GET_ZNS] Received request from {req.remote_addr} for lat: {recv_lat} and long: {recv_long}")
    try:
        zones = db.return_zones(config, recv_lat, recv_long)
        return dict(data=zones)
    except Exception as e:
        msg.exception(e)
        return dict(FAIL="UNKNOWN_FAIL")


def handle_add_zone(req, config) -> dict:
    """
    Handle the add zone call

    Args:
        req (werkzeug.local.LocalProxy): Flask request
        config (models.Config): Config instance

    Returns:
        dict: Response
    """
    key = req.args.get('key')
    # If the key is invalid just return INVALID_KEY
    if not isValidKey("private", key, config):
        msg.fail(f"Requested from {req.remote_addr}")
        return dict(FAIL="INVALID_KEY")

    _type = req.args.get('type')
    _coords = req.args.get('coords')

    try:
        _type = int(_type)
    except ValueError:
        return dict(FAIL="INVALID_DATA")

    coords = str(_coords)
    # Check to see if it can find at least one set of delimiters
    if coords.find(',') == -1:
        return dict(FAIL="INVALID_DATA")
    if coords.find('@') == -1:
        return dict(FAIL="INVALID_DATA")

    msg.info(f"[REQ_ADD_ZNS] Received request from {req.remote_addr} with type: {_type} and coords: {coords}")
    try:
        response = db.add_zone(config, _type, coords)
        if response == 0:
            return dict(SUCCESS="DATA_ADDED")
        else:
            msg.fail(f"Recieved {response} from method add_zone")
            return dict(FAIL=str(response))
    except Exception as e:
        msg.exception(e)
        return dict(FAIL="UNKNOWN_FAIL")


def handle_del_zone(req, config) -> dict:
    """
    Handle the delete zones call

    Args:
        req (werkzeug.local.LocalProxy): Flask request
        config (models.Config): Config instance

    Returns:
        dict: Response
    """
    key = req.args.get('key')
    # If the key is invalid just return INVALID_KEY
    if not isValidKey("private", key, config):
        msg.fail(f"Requested from {req.remote_addr}")
        return dict(FAIL="INVALID_KEY")

    _coords = req.args.get('coords')
    coords = str(_coords)
    # Check to see if it can find at least one set of delimiters
    if coords.find(',') == -1:
        return dict(FAIL="INVALID_DATA")
    if coords.find('@') == -1:
        return dict(FAIL="INVALID_DATA")

    msg.info(f"[REQ_DEL_ZNS] Received DELETE request from {req.remote_addr} for coords: {coords}")
    try:
        response = db.del_markers(config, coords)
        if response == 0:
            return dict(SUCCESS="DATA_DELETED")
        else:
            msg.fail(f"Recieved {response} from method del_zone")
            return dict(FAIL=str(response))
    except Exception as e:
        msg.exception(e)
        return dict(FAIL="UNKNOWN_FAIL")
