# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Guest Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def slugify_guests(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT guestid, guest from ww_guests "
        "WHERE guestslug IS NULL "
        "OR TRIM(guestslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            guest_id = row["guestid"]
            guest = row["guest"]
            guest_slug = slugify(guest)
            query = "UPDATE ww_guests SET guestslug = %s WHERE guestid = %s;"
            cursor.execute(
                query,
                (
                    guest_slug,
                    guest_id,
                ),
            )

    cursor.close()
