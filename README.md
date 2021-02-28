# prisma.ai-backend
Public release of our backend, it served the markers and zones as well as generate said zones

# Usage:

## Markers:
``` 
Get markers from a specific region:
    <ip_of_server>/get_markers?key=<key>&lat=<lat_round_to_int>&long=<long_round_to_int>
Add a marker:
    <ip_of_server>/add_marker?key=<key>&type=<type_of_data>&lat=<lat_exact>&long=<long_exact>
Delete markers:
    <ip_of_server>/del_markers?key=<key>&lat=<lat_exact>&long=<long_exact>
``` 

## Zones:
``` 
Get zones from a specific region:
    <ip_of_server>/get_zones?key=<key>&lat=<lat_round_to_int>&long=<long_round_to_int>
Add a zone:
    <ip_of_server>/add_zone?key=<key>&type=<type>&coords=<coords_that_form_the_zone>
Delete a zone:
    <ip_of_server>/del_zone?key=<key>&coords=<coords_that_form_the_zone>
``` 

## Examples:
``` 
http://<IP>:<PORT>/get_markers?key=<key>&lat=46&long=23
http://<IP>:<PORT>/add_marker?key=<key>&type=marker_low_danger&lat=46.123&long=23.345
http://<IP>:<PORT>/del_markers?key=<key>&lat=46.123&long=23.345
--------------------------------------------------------------------------------------
http://<IP>:<PORT>/get_zones?key=<key>&lat=46&long=23
http://<IP>:<PORT>/add_zone?key=<key>&type=75&coords=43.123,23.234#43.567,23.678
http://<IP>:<PORT>/del_zone?key=<key>&coords=43.123,23.234#43.567,23.678
``` 

# Running
* Make a keys.json file in /config:
``` 
{
    "private_keys": [
        "private_keys"
    ],
    "public_keys": [
        "public_keys"
    ],
    "db_user": "MYSQL Database User",
    "db_pass": "MYSQL Database Pass"
}
``` 
* Check config.json in /config to make sure it's correct (set port)
* Run `python3 main.py`

#### Dependecies:
* Python 3.7
* Flask 1.1.2
* Waitress
* mysql-connector-python

---

# What is prisma.ai?
prisma.ai is an upcoming start-up meant to increase you safety in the city

# Who is behind prisma.ai?
- David Pescariu - Co-founder & Developer
- Raul Popa - Co-founder & Developer & Designer

# License and Copyright
The sources are released under the GNU GPLv3 license, which requires you to credit us,
and keep the code open-source.

---

# Who was Team Entropy?
- The people behind Safe Signal, a new step in personal safety.
- We won 2nd Place during the 2020 DpIT Contest

# The OG Safe Signal Team
- David Pescariu - Lead Developer
- Raul Popa - Developer and Lead Designer
- Andra Bolboaca - Business Relations
- Ioana Gabor - Developer
- Ana Pop - Design and Public Relations
- Dorin Cuibus - Developer
