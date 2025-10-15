# Copyright (c) 2018-2025 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Panelist Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def panelist_slugs(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[str]:
    """Retrieve a list of existing panelist slugs."""
    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT panelistslug FROM ww_panelists
        WHERE panelistslug IS NOT NULL
        OR TRIM(panelistslug) <> '';
        """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    slugs = []
    for row in results:
        slugs.append(row["panelistslug"])

    return slugs


def slugify_panelists(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    """Generate slug strings for Panelists."""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT panelistid, panelist from ww_panelists "
        "WHERE panelistslug IS NULL "
        "OR TRIM(panelistslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        slugs = panelist_slugs(database_connection=database_connection)
        for row in result:
            panelist_id = row["panelistid"]
            panelist = row["panelist"]
            panelist_slug = slugify(panelist)

            if panelist_slug in slugs:
                panelist_slug = f"{panelist_slug}-{panelist_id}"
                slugs.append(panelist_slug)

            query = "UPDATE ww_panelists SET panelistslug = %s WHERE panelistid = %s;"
            cursor.execute(
                query,
                (
                    panelist_slug,
                    panelist_id,
                ),
            )

    cursor.close()
