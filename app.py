# Copyright (c) 2018-2024 Linh Pham
# wwdtm-slugify is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Slugify Guests, Hosts, Locations, Panelists and Scorekeepers."""

import json
from pathlib import Path

from mysql.connector import connect

from wwdtm import guests, hosts, locations, panelists, scorekeepers


def load_config():
    """Load configuration settings from config.json."""
    config_file_path = Path("config.json")
    with config_file_path.open(mode="r", encoding="utf-8") as config_file:
        config_dict = json.load(config_file)

    return config_dict


def main():
    """Generate slugs."""
    config = load_config()
    database_connection = connect(**config["database"])
    database_connection.autocommit = True

    guests.slugify_guests(database_connection)
    hosts.slugify_hosts(database_connection)
    locations.slugify_locations(database_connection)
    panelists.slugify_panelists(database_connection)
    scorekeepers.slugify_scorekeepers(database_connection)


if __name__ == "__main__":
    main()
