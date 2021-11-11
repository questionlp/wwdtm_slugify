# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 Linh Pham
# wwdtm-slugify is relased under the terms of the Apache License 2.0
"""Generate slugs for location records in the Wait Wait Stats Database"""

import mysql.connector
from slugify import slugify

def slugify_locations(database_connection: mysql.connector.connect):
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT locationid, venue, city, state from ww_locations "
             "WHERE locationslug IS NULL "
             "OR TRIM(locationslug) = '';")
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            location_id = row["locationid"]
            venue = row["venue"]
            city = row["city"]
            state = row["state"]
            if venue and city and state:
                location_slug = slugify("{} {} {}".format(venue, city, state))
            elif venue and city and not state:
                location_slug = slugify("{} {}".format(venue, city))
            elif id and venue and (not city and not state):
                location_slug = slugify("{} {}".format(location_id, venue))
            elif id and city and state and not venue:
                location_slug = slugify("{} {} {}".format(location_id,
                                                          city,
                                                          state))
            elif id:
                location_slug = "location-{}".format(location_id)

            query = ("UPDATE ww_locations SET locationslug = %s "
                     "WHERE locationid = %s;")
            cursor.execute(query, (location_slug, location_id,))

    cursor.close()
