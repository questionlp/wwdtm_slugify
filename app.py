# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Linh Pham
# wwdtm-slugify is relased under the terms of the Apache License 2.0
"""Scan through Wait Wait Stats Page database and generate slugs for
guest, host, panelist and scorekeeper entries without corresponding
slug strings"""

import json
import mysql.connector
from wwdtm import guests, hosts, panelists, scorekeepers

#region Bootstrap Functions
def load_config():
    """Load configuration settings from config.json"""
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)

    return config_dict

#endregion

#region Application Initialization
def main():
    """Generate slugs"""
    config = load_config()
    database_connection = mysql.connector.connect(**config["database"])
    database_connection.autocommit = True

    guests.slugify_guests(database_connection)
    hosts.slugify_hosts(database_connection)
    panelists.slugify_panelists(database_connection)
    scorekeepers.slugify_scorekeepers(database_connection)

if __name__ == "__main__":
    main()

#endregion
