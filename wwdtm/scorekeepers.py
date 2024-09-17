# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Scorekeeper Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def scorekeeper_slugs(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[str]:
    """Retrieve a list of existing scorekeeper slugs."""
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT scorekeeperslug FROM ww_scorekeepers
        WHERE scorekeeperslug IS NOT NULL
        OR TRIM(scorekeeperslug) <> '';
        """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    slugs = []
    for row in results:
        slugs.append(row.scorekeeperslug)

    return slugs


def slugify_scorekeepers(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    """Generate slug strings for Scorekeepers."""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT scorekeeperid, scorekeeper from ww_scorekeepers "
        "WHERE scorekeeperslug IS NULL "
        "OR TRIM(scorekeeperslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        slugs = scorekeeper_slugs(database_connection=database_connection)
        for row in result:
            scorekeeper_id = row["scorekeeperid"]
            scorekeeper = row["scorekeeper"]
            scorekeeper_slug = slugify(scorekeeper)

            if scorekeeper_slug in slugs:
                scorekeeper_slug = f"{scorekeeper_slug}-{scorekeeper_id}"
                slugs.append(scorekeeper_slug)

            query = (
                "UPDATE ww_scorekeepers SET scorekeeperslug = %s "
                "WHERE scorekeeperid = %s;"
            )
            cursor.execute(
                query,
                (
                    scorekeeper_slug,
                    scorekeeper_id,
                ),
            )

    cursor.close()
