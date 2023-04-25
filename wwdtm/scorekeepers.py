# -*- coding: utf-8 -*-
# Copyright (c) 2018-2023 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
"""Generate slugs for scorekeeper records in the Wait Wait Stats
Database"""

import mysql.connector
from slugify import slugify


def slugify_scorekeepers(database_connection: mysql.connector.connect):
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
