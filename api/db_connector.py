# Copyright (c) prisma.ai 2021
# All rights reserved

__author__ = 'David Pescariu'

import mysql.connector
from datetime import datetime
from api.zone_builder import ZoneBuilder

def __connect(config) -> (
    mysql.connector.cursor, 
    mysql.connector.connection):
    """
    Connect to the database and get the cursor

    Args:
        config (models.Config): Config instance

    Returns:
        cnx.cursor() (function <- mysql.connector.cursor): The mysql cursor
        cnx (mysql.connector.connection): The mysql connection
    """

    db_user = config.DB_LOGIN_USER
    db_pass = config.DB_LOGIN_PASS

    cnx = mysql.connector.connect(
        user=db_user, password=db_pass,
        host='127.0.0.1', database='data')

    return cnx.cursor(), cnx

def __disconnect(
    cursor: mysql.connector.cursor, 
    cnx: mysql.connector.connection) -> None:
    """
    Disconect from the database

    Args:
        cnx.cursor (function <- mysql.connector.cursor): The mysql cursor
        cnx (mysql.connector.connection): The mysql connection
    """

    cnx.commit()
    cursor.close()
    cnx.close()

################################################################################
################################## MARKERS #####################################
################################################################################

def return_markers(config, req_lat: int, req_long: int) -> list:
    """
    Return the markers

    Args:
        config (models.Config): Config instance
        req_lat (int): Zone lat
        req_long (int): Zone long

    Returns:
        list: The list of markers
    """
    cursor, cnx = __connect(config)
    query_zone = f"{req_lat}{req_long}"
    query = (f"select exactlat, exactlong, type, submitdate, submittime from marker_data where zone like \"{query_zone}\";")
    cursor.execute(query)
    
    markers = []
    for (exactlat, exactlong, type_, date_added, time_added) in cursor:
        markers.append(f"{exactlat}&{exactlong}&{type_}&{date_added}&{time_added}")

    markers.append("end")

    __disconnect(cursor, cnx)
    return markers

def add_marker(config, exact_lat: float, exact_long: float, _type: str) -> int:
    """
    Add a marker to the database

    Args:
        config (models.Config): Config instance
        exact_lat (float): The exact lat of the marker
        exact_long (float): The exact long of the marker
        _type (str): The type of the marker

    Returns:
        int: Status code -> -1=Unknown fail, check log, 0=OK, 1=mysql.connector.errors.ProgrammingError
    """
    status_code = -1

    cursor, cnx = __connect(config)
    query_zone = f"{int(exact_lat)}{int(exact_long)}"
    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.now().strftime("%H:%M:%S")
    query = (f"insert into marker_data values (\"{query_zone}\", {exact_lat}, {exact_long}, \"{_type}\", \"{date}\", \"{time}\");")
    
    try:
        cursor.execute(query)
        status_code = 0
    except mysql.connector.errors.ProgrammingError:
        status_code = 1

    __disconnect(cursor, cnx)
    return status_code

def del_markers(config, exact_lat: float, exact_long: float) -> int:
    """
    Delete markers from exact coords from the database

    Args:
        config (models.Config): Config instance
        exact_lat (float): The exact lat of the marker(s)
        exact_long (float): The exact long of the marker(s)

    Returns:
        int: Status code -> -1=Unknown fail, check log, 0=OK, 1=mysql.connector.errors.ProgrammingError
    """
    status_code = -1

    cursor, cnx = __connect(config)
    query = (f"delete from marker_data where exactlat like {exact_lat} and exactlong like {exact_lat};")

    try:
        cursor.execute(query)
        cnx.commit()
        status_code = 0
    except mysql.connector.errors.ProgrammingError:
        status_code = 1

    __disconnect(cursor, cnx)
    return status_code

################################################################################
################################### ZONES ######################################
################################################################################

def return_zones(config, req_lat: int, req_long: int) -> list:
    """
    Return the zones

    Args:
        config (models.Config): Config instance
        req_lat (int): Zone lat
        req_long (int): Zone long

    Returns:
        list: The list of zones
    """
    # The way this is implemented is absolutely terrible. Too bad...
    # But it works as long as there aren't too many calls or too many markers.
    #
    # To implement it right you would run zone_builder on a schedule and add the
    # results to the database
    #
    # Unused code atm, but don't delete:
    # cursor, cnx = __connect(config)
    # query_zone = f"{req_lat}{req_long}"
    # query = (f"select type, coords, submitdate, submittime from zone_data where zone like \"{query_zone}\";")
    # cursor.execute(query)

    # zones = []
    # for (_type, coords, _date, _time) in cursor:
    #     zones.append(f"{_type}&{coords}&{_date}&{_time}")
        
    # zones.append("end")

    # __disconnect(cursor, cnx)
    zones = ZoneBuilder(return_markers(config, req_lat, req_long)) # This is such a nasty work-around, I both hate it and love it
    _zones = zones.get_zones()
    _zones.append("end")
    return _zones

def add_zone(config, _type: int, coords: str) -> int:
    """
    Add a zone to the database

    Args:
        config (models.Config): Config instance
        _type (int): The type/danger level of the zone (ie. 75)
        coords (str): Format should be lat1,long1%lat2,long2%...

    Returns:
        int: Status code -> -1=Unknown fail, check log, 0=OK, 1=ValueError, 2=mysql.connector.errors.ProgrammingError
    """
    status_code = -1
    cursor, cnx = __connect(config)

    try:
        first_coords = coords.split(',')[0]
        __split = first_coords.split('@')
        query_zone = f"{int(float(__split[0]))}{int(float(__split[1]))}"
    except ValueError:
        status_code == 1
        __disconnect(cursor, cnx)
        return status_code
    
    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.now().strftime("%H:%M:%S")

    query = (f"insert into zone_data values(\"{query_zone}\", {_type}, \"{coords}\", \"{date}\", \"{time}\");")
    try:
        cursor.execute(query)
        status_code = 0
    except mysql.connector.errors.ProgrammingError:
        status_code = 2

    __disconnect(cursor, cnx)
    return status_code

def del_zone(config, coords: str) -> int:
    """
    Delete a zone from the database

    Args:
        config (models.Config): Config instance
        coords (str): Format should be lat1,long1%lat2,long2%...

    Returns:
        int: Status code -> -1=Unknown fail, check log, 0=OK, 1=mysql.connector.errors.ProgrammingError
    """
    status_code = -1

    cursor, cnx = __connect(config)
    query = (f"delete from zone_data where coords like {coords};")

    try:
        cursor.execute(query)
        cnx.commit()
        status_code = 0
    except mysql.connector.errors.ProgrammingError:
        status_code = 1

    __disconnect(cursor, cnx)
    return status_code
