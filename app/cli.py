import os
import click


from glob import glob
from subprocess import call
from app import db
from app.models import (
    CatalogItem,
    Category,
    Permission,
    Role,
    User
)
import config
from config import Config
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def register(app):
    @app.cli.command('seed-db')
    @click.command()
    def seed():
        print('Starting DB seed')
        db.create_all()

        seed_users()
        seed_categories()
        seed_catalog()

        db.session.commit()
        print('DB seed complete')
    

    def seed_users():
        print('Adding roles, demo-user, demo-admin, and admin')
        Role.insert_roles()

        
        demo = User(
            username='demo',
            password=Config.DEMO_PASSWORD,
            email=Config.DEMO_EMAIL,
            role=Role.query.filter_by(permissions=Permission.GENERAL).first())
        demo_admin = User(
            username='demo_admin',
            password=Config.DEMO_ADMIN_PASSWORD,
            email=Config.DEMO_ADMIN_EMAIL,
            role=Role.query.filter_by(permissions=Permission.DEMO_ADMINISTER).first())
        admin = User(
            username='admin',
            password=Config.ADMIN_PASSWORD,
            email=Config.ADMIN_EMAIL,
            role=Role.query.filter_by(permissions=Permission.ADMINISTER).first())

        db.session.add(demo)
        db.session.add(demo_admin)
        db.session.add(admin)

    
    def seed_categories():
        print('Adding categories')
        Role.insert_roles()

        food = Category(
            name = 'Food Commodities'
        )

        nonfood = Category(
            name = 'Non-Food Commodities'
        )

        hard = Category(
            name = 'Hard Commodities'
        )

        db.session.add(food)
        db.session.add(nonfood)
        db.session.add(hard)

    
    def seed_catalog():
        print('Adding catalog')
        if config.DevelopmentConfig:
            baseurl = 'http://localhost:5000/static/'
        else:
            baseurl = '/static/'

        coffee = CatalogItem(
            name = "Coffee",
            description = "3 tonnes of pure arabica coffee from the ethopian highlands picked carefully and of the highest quality",
            image_url = "/static/images/products/coffee.jpg",
            price = 1000,
            category_id = 1
        )

        sugar = CatalogItem(
            name = "Sugar",
            description = "10 bales of sugar at an affordable price",
            image_url = "/static/images/products/sugar.jpg",
            price = 100,
            category_id = 1
        )

        wheat = CatalogItem(
            name = "Wheat",
            description = "Wheat 1 tonne. Already sorted for processing. Contact for further details.",
            image_url = "/static/images/products/wheat.jpg",
            price = 1500,
            category_id = 1
        )

        maize = CatalogItem(
            name = "Maize",
            description = "10 tonnes of maize corn. All at an affordable price.",
            image_url = "/static/images/products/maize-corn.jpg",
            price = 3000,
            category_id = 1
        )

        db.session.add(coffee)
        db.session.add(sugar)
        db.session.add(wheat)
        db.session.add(maize)


        oil = CatalogItem(
            name = "Oil",
            description = "100 barrels of crude oil. Raw quality. Contact for further details.",
            image_url = "/static/images/products/oil.jpg",
            price = 10000,
            category_id = 2
        )

        rubber = CatalogItem(
            name = "Rubber",
            description = "50 barrels of tree rubber.",
            image_url = "/static/images/products/rubber.jpg",
            price = 1000,
            category_id = 2
        )

        db.session.add(oil)
        db.session.add(rubber)

        copper = CatalogItem(
            name = "Copper",
            description = "3 tonnes copper wire. Pure quality. Call for details",
            image_url = "/static/images/products/copper.jpg",
            price = 5000,
            category_id = 3
        )

        crystal = CatalogItem(
            name = "Crystal",
            description = "Pure amethyst crystal. 3kg.",
            image_url = "/static/images/products/crystal.jpg",
            price = 15000,
            category_id = 3
        )

        diamond = CatalogItem(
            name = "Diamond",
            description = "5kg finely cut diamond. Raj Investments. Call formore info. ",
            image_url = "/static/images/products/diamond.jpg",
            price = 1000,
            category_id = 3
        )

        gold = CatalogItem(
            name = "Gold",
            description = "1 tonne gold bars. Finest Quality ",
            image_url = "/static/images/products/gold.jpg",
            price = 100000,
            category_id = 3
        )

        jewels = CatalogItem(
            name = "Jewels",
            description = "Jewels for sale. Family heirlooms. Call for info. ",
            image_url = "/static/images/products/jewels.jpg",
            price = 5000,
            category_id = 3
        )


        db.session.add(copper)
        db.session.add(crystal)
        db.session.add(diamond)
        db.session.add(gold)
        db.session.add(jewels)
    
    @click.command()
    @click.option('-f', '--fix-imports', default=False, is_flag=True,
                    help='Fix imports using isort, before linting')
    def lint(fix_imports):
        skip = ['node_modules', 'requirements']
        root_files = glob('*.py')
        root_directories = [
            name for name in next(os.walk('.'))[1] if not name.startswith('.')
        ]
        files_and_directories = [
            arg for arg in root_files + root_directories if arg not in skip
        ]

        def execute_tool(description, *args):
            ''' Execute a checking tool with its arguments. '''
            command_line = list(args) + files_and_directories
            click.echo('{}: {}'.format(description, ''.join(command_line)))
            rv = call(command_line)
            if rv != 0:
                exit(rv)

        if fix_imports:
            execute_tool('Fixing import order', 'isort', '-rc')
        execute_tool('Checking code style', 'flake8')

    @click.command()
    def clean():
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith('.pyc') or filename.endswith('.pyc'):
                    full_pathname = os.path.join(dirpath, filename)
                    click.echo('Removing {}'.format(full_pathname))
                    os.remove(full_pathname)

    
    @click.command()
    @click.option('--url', default=None,
                    help='Url to test (ex. /static/image.jpg)')
    @click.option('--order', default='rule',
                    help='Property on Rule to order by (default: rule)')
    @with_appcontext
    def urls(url, order):
        rows = []
        column_length = 0
        column_headers = ('Rule', 'Endpoint', 'Arguments')

        if url:
            try:
                rule, arguments = (
                    current_app.url_map
                                .bind('localhost')
                                .match(url, return_rule=True)
                )
                rows.append((rule.rule, rule.endpoint, arguments))
                column_length = 3
            except (NotFound, MethodNotAllowed) as e:
                rows.append(('<{}>'.format(e), None, None))
                column_length = 1
        else:
            rules = sorted(
                current_app.url_map.iter_rules(),
                key=lambda rule: getattr(rule, order)
            )
            for rule in rules:
                rows.append((rule.rule, rule.endpoint, None))
            column_length = 2


        str_template = ''
        table_width = 0

        if column_length >= 1:
            max_rule_length = max(len(r[0]) for r in rows)
            max_rule_length = max_rule_length if max_rule_length > 4 else 4
            str_template += '{:' + str(max_rule_length) + '}'
            table_width += 2 + max_rule_length

        if column_length >= 2:
            max_endpoint_length = max(len(str(r[1])) for r in rows)
            max_endpoint_length = (
                max_endpoint_length if max_endpoint_length > 8 else 8
            )
            str_template += '{:' + str(max_endpoint_length) + '}'
            table_width += 2 + max_endpoint_length

        if column_length >= 3:
            max_arguments_length = max(len(r[2]) for r in rows)
            max_arguments_length = max_arguments_length if max_arguments_length > 9 else 9
            str_template += '{:' + str(max_arguments_length) + '}'
            table_width += 2 + max_arguments_length

        click.echo(str_template.format(*column_headers[:column_length]))
        click.echo('-' * table_width)

        for row in rows:
            click.echo(str_template.format(*row[:column_length]))

    @app.cli.command("test")
    def test():
        import pytest
        rv = pytest.main([TEST_PATH, '--verbose'])
        exit(rv)