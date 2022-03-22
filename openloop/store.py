"""
Database storing drivers (easy to add future database options)
"""

import json, os

from datetime import datetime

import openloop.templates

if not os.path.exists("database"):
    os.mkdir("database")

def backup(db):
    date = datetime.now().date()
    with open(f"database/current.json", "w") as f:
        json.dump(db, f)
    size = os.stat(f"database/current.json").st_size
    return size


def restore():
    snapshots = os.listdir("database")
    if len(snapshots) > 0:
        newest = snapshots[len(snapshots)-1]
        print(f" * Restoring Database from {newest}")

        with open(f"database/{newest}") as f:
            return json.load(f)
    else:
        print(" * No database found! Creating database from template...")
        return openloop.templates.default_config