# Copyright (c) 2018-2025 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Guest Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def guest_slugs(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[str]:
    """Retrieve a list of existing Not My Job guest slugs."""
    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT guestslug FROM ww_guests
        WHERE guestslug IS NOT NULL
        OR TRIM(guestslug) <> '';
        """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    slugs = []
    for row in results:
        slugs.append(row["guestslug"])

    return slugs


def slugify_guests(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    """Generate slug strings for Not My Job Guests."""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT guestid, guest from ww_guests "
        "WHERE guestslug IS NULL "
        "OR TRIM(guestslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        slugs = guest_slugs(database_connection=database_connection)

        for row in result:
            guest_id = row["guestid"]
            guest = row["guest"]
            guest_slug = slugify(guest)

            if guest_slug in slugs:
                guest_slug = f"{guest_slug}-{guest_id}"
                slugs.append(guest_slug)

            query = "UPDATE ww_guests SET guestslug = %s WHERE guestid = %s;"
            cursor.execute(
                query,
                (
                    guest_slug,
                    guest_id,
                ),
            )

    cursor.close()
