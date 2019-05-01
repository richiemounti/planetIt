# planetIt

E-commerce application where users may browse the catalog, manage their
shopping cart, and submit orders (dummy or through stripe). Admin  users may
manage the catalog. Features include a distributed session store, full-text search (with
PostgreSQL), and asynchronous emails (via threads).

Technology
----------
* Flask
* PostgreSQL
* Bootstrap 4
* DataTables
* Noty


Run
---

Create a database named 'carthage'. Open `config.py` and point the database to your
servers.

After configuring the settings, set the `FLASK_APP` env variable to
manage.py, and install the javascript (e.g `npm install`) and python
dependencies (e.g. `pip install -r requirements.txt`). Be sure to install the
python dependencies using `requirements.txt` located in `./planetIt/`.

`cd` into `./planetIt` (if you are not already); then run:
```
flask db upgrade
flask seed-db
flask run
Go to http://localhost:5000
```

