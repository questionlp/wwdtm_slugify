# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Linh Pham
# wwdtm-slugify is relased under the terms of the Apache License 2.0
"""Generate slugs for host records in the Wait Wait Stats Database"""

import mysql.connector
from slugify import slugify

def slugify_hosts(database_connection: mysql.connector.connect):
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT hostid, host from ww_hosts "
             "WHERE hostslug IS NULL "
             "OR TRIM(hostslug) = '';")
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            host_id = row["hostid"]
            host = row["host"]
            host_slug = slugify(host)
            query = ("UPDATE ww_hosts SET hostslug = %s "
                     "WHERE hostid = %s;")
            cursor.execute(query, (host_slug, host_id,))

    cursor.close()
