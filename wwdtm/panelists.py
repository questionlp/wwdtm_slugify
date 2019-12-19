# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Linh Pham
# wwdtm-slugify is relased under the terms of the Apache License 2.0
"""Generate slugs for panelist records in the Wait Wait Stats Database"""

import mysql.connector
from slugify import slugify

def slugify_panelists(database_connection: mysql.connector.connect):
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT panelistid, panelist from ww_panelists "
             "WHERE panelistslug IS NULL "
             "OR TRIM(panelistslug) = '';")
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            panelist_id = row["panelistid"]
            panelist = row["panelist"]
            panelist_slug = slugify(panelist)
            query = ("UPDATE ww_panelists SET panelistslug = %s "
                     "WHERE panelistid = %s;")
            cursor.execute(query, (panelist_slug, panelist_id,))

    cursor.close()
