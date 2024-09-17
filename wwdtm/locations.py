# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Location Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def location_slugs(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[str]:
    """Retrieve a list of existing location slugs."""
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT locationslug FROM ww_locations
        WHERE locationslug IS NOT NULL
        OR TRIM(locationslug) <> '';
        """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    slugs = []
    for row in results:
        slugs.append(row.locationslug)

    return slugs


def slugify_locations(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    """Generate slug strings for Locations."""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT locationid, venue, city, state from ww_locations "
        "WHERE locationslug IS NULL "
        "OR TRIM(locationslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        slugs = location_slugs(database_connection=database_connection)

        for row in result:
            location_id = row["locationid"]
            venue = row["venue"]
            city = row["city"]
            state = row["state"]
            if venue and city and state:
                location_slug = slugify(f"{venue} {city} {state}")
            elif venue and city and not state:
                location_slug = slugify(f"{venue} {city}")
            elif location_id and venue and (not city and not state):
                location_slug = slugify(f"{location_id} {venue}")
            elif location_id and city and state and not venue:
                location_slug = slugify(f"{location_id} {city} {state}")
            elif location_id:
                location_slug = f"location-{location_id}"

            if location_slug in slugs:
                location_slug = f"{location_slug}-{location_id}"
                slugs.append(location_slug)

            query = "UPDATE ww_locations SET locationslug = %s WHERE locationid = %s;"
            cursor.execute(
                query,
                (
                    location_slug,
                    location_id,
                ),
            )

    cursor.close()
