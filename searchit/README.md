Project 02: SearchIt
====================

The second project is to create **SearchIt**, a music database web application
written in [Tornado] and [SQLite].

Overview
--------

The project has the following layout:

    searchit
        \_ assets
                \_ html
                        \_ album.html       SearchIt Album Template
                        \_ base.html        SearchIt Base Template
                        \_ gallery.html     SearchIt Gallery Template
                        \_ index.html       SearchIt Index Template
                        \_ track.html       SearchIt Track Template
                \_ yaml
                        \_ data.yaml        Music data YAML
        \_ searchit
                \_ __init__.py
                \_ __main__.py              Package Main Execution Module
                \_ database.py              SearchIt Database Module
                \_ web.py                   SearchIt Web Module

For this project, you need to modify the following files:

1. `album.html`: This should display a table consisting of the tracks found in
   the album.

2. `gallery.html`: This should display a series of thumbnails for the items
   found in the group.

3. `index.html`: This should display your group name, group members, and group
   logo.

4. `track.html`: This should display information about the track.

5. `database.py`: This implements the [SQLite] database.

6. `web.py`: This implements the [Tornado] web application.

Run
---

To run web application, you can do the following:

    $ python -m searchit

[Tornado]:      http://www.tornadoweb.org/
[SQLite]:       https://www.sqlite.org/
