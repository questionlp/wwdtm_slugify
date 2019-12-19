# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Linh Pham
# wwdtm-slugify is relased under the terms of the Apache License 2.0
"""Generate slugs for guest records in the Wait Wait Stats Database"""

import mysql.connector
from slugify import slugify

def slugify_guests(database_connection: mysql.connector.connect):
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT guestid, guest from ww_guests "
             "WHERE guestslug IS NULL "
             "OR TRIM(guestslug) = '';")
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            guest_id = row["guestid"]
            guest = row["guest"]
            guest_slug = slugify(guest)
            query = ("UPDATE ww_guests SET guestslug = %s "
                     "WHERE guestid = %s;")
            cursor.execute(query, (guest_slug, guest_id,))

    cursor.close()
