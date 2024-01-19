# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Panelist Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def slugify_panelists(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT panelistid, panelist from ww_panelists "
        "WHERE panelistslug IS NULL "
        "OR TRIM(panelistslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            panelist_id = row["panelistid"]
            panelist = row["panelist"]
            panelist_slug = slugify(panelist)
            query = "UPDATE ww_panelists SET panelistslug = %s WHERE panelistid = %s;"
            cursor.execute(
                query,
                (
                    panelist_slug,
                    panelist_id,
                ),
            )

    cursor.close()
