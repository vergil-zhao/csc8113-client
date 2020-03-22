import click

from user.operations import all_users, register_user
from user.models import User

from utils.storage import Base, engine, session
from utils.signing import Key


@click.group()
def cli():
    pass


@click.command()
def migrate():
    Base.metadata.create_all(engine)


@click.command()
@click.argument('host', help='the root url of the TTP')
def set_ttp(host):
    pass


@click.command()
def users():
    for user in all_users():
        click.echo(user)


@click.command()
@click.option('-n', '--name', required=True, help='the name of user')
@click.option('-p', '--private', help='import the key if a private key is given')
def add_user(name, private):
    key = Key(private_key=private)
    user = User(name=name, public_key=key.public_key, private_key=key.private_key)
    session.add(user)
    session.commit()

    hint = '🎉 New user created' if private is not None else '🎉 A user imported'
    click.echo(click.style(hint, fg='green'))
    click.echo('- Local ID:   ' + str(user.id))
    click.echo('- Name:       ' + user.name)
    click.echo('- Public Key: ' + user.public_key)


@click.command()
@click.option('-u', '--uid', required=True, help='the local id of a user needed to be registered')
def register(uid):
    user = session.query(User).filter_by(id=uid).first()
    register_user(user)


cli.add_command(users)
cli.add_command(migrate)
cli.add_command(add_user)
cli.add_command(register)
