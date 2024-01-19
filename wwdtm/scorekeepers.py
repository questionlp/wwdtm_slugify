# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Scorekeeper Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def slugify_scorekeepers(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> None:
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT scorekeeperid, scorekeeper from ww_scorekeepers "
        "WHERE scorekeeperslug IS NULL "
        "OR TRIM(scorekeeperslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            scorekeeper_id = row["scorekeeperid"]
            scorekeeper = row["scorekeeper"]
            scorekeeper_slug = slugify(scorekeeper)
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
