# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Location Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def slugify_locations(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT locationid, venue, city, state from ww_locations "
        "WHERE locationslug IS NULL "
        "OR TRIM(locationslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            location_id = row["locationid"]
            venue = row["venue"]
            city = row["city"]
            state = row["state"]
            if venue and city and state:
                location_slug = slugify(f"{venue} {city} {state}")
            elif venue and city and not state:
                location_slug = slugify(f"{venue} {city}")
            elif id and venue and (not city and not state):
                location_slug = slugify(f"{location_id} {venue}")
            elif id and city and state and not venue:
                location_slug = slugify(f"{location_id} {city} {state}")
            elif id:
                location_slug = f"location-{location_id}"

            query = "UPDATE ww_locations SET locationslug = %s WHERE locationid = %s;"
            cursor.execute(
                query,
                (
                    location_slug,
                    location_id,
                ),
            )

    cursor.close()
