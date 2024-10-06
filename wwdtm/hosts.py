# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Host Slug Generator."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def host_slugs(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[str]:
    """Retrieve a list of existing host slugs."""
    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT hostslug FROM ww_hosts
        WHERE hostslug IS NOT NULL
        OR TRIM(hostslug) <> '';
        """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    slugs = []
    for row in results:
        slugs.append(row["hostslug"])

    return slugs


def slugify_hosts(database_connection: MySQLConnection | PooledMySQLConnection) -> None:
    """Generate slug strings for Hosts."""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT hostid, host from ww_hosts "
        "WHERE hostslug IS NULL "
        "OR TRIM(hostslug) = '';"
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        slugs = host_slugs(database_connection=database_connection)

        for row in result:
            host_id = row["hostid"]
            host = row["host"]
            host_slug = slugify(host)

            if host_slug in slugs:
                host_slug = f"{host_slug}-{host_id}"
                slugs.append(host_slug)

            query = "UPDATE ww_hosts SET hostslug = %s WHERE hostid = %s;"
            cursor.execute(
                query,
                (
                    host_slug,
                    host_id,
                ),
            )

    cursor.close()
