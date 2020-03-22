from .exchange import *
from utils.signing import Key


@click.group()
def cli():
    pass


@click.command()
@click.option('-n', '--name', required=True, help='the name of user')
@click.option('-e', '--email', required=True, help='the email address of user')
def register(name, email):
    r = requests.post(HOST + '/users', json={
        'email': email,
        'username': name,
        'password': 12345678
    })
    if r.status_code != 201:
        click.echo(click.style('😭 Something went wrong', fg='red'))
        click.echo(r.text)
    else:
        hint = '🎉 New user created'
        click.echo(click.style(hint, fg='green'))
        click.echo('✉️ Email:      ' + r.json().get('email'))
        click.echo('👔 Name:       ' + r.json().get('name'))


@click.command()
@click.argument('session', required=True)
def get_nrr(session):
    r = requests.get(HOST + f'/exchange/fetchNRR/{session}')
    if r.status_code != 200:
        click.echo(click.style('😭 Something went wrong', fg='red'))
        click.echo(r.text)
    else:
        hint = '🎉 NRR received successfully'
        click.echo(click.style(hint, fg='green'))
        click.echo(b64encode(r.content).decode('ascii'))


@click.command()
@click.argument('session', required=True)
def abort(session):
    r = requests.post(HOST + f'/exchange/abort/{session}')
    if r.status_code != 200:
        click.echo(click.style('😭 Something went wrong', fg='red'))
        click.echo('Status code: ' + str(r.status_code))
        click.echo(r.text)
    else:
        hint = '🎉 Session aborted'
        click.echo(click.style(hint, fg='green'))


@click.command()
@click.option('-n', '--username', required=True, help='the name of sender')
@click.option('-p', '--password', required=True, help='the password of sender')
@click.option('-e', '--toemail', required=True, help='the email of receiver')
@click.option('-p', '--path', required=True, help='the file path')
@click.option('-k', '--key', help='the private key for signing')
def auto_upload(username, password, toemail, path, key):
    sid = sign_in(username, password)
    if sid is None:
        return

    key = keygen(key)

    if key_reg(sid, key.public_key):
        upload(sid, toemail, path, key.private_key)


@click.command()
@click.option('-n', '--username', required=True, help='the name of receiver')
@click.option('-p', '--password', required=True, help='the password of sender')
@click.option('-o', '--nro', required=True, help='the NRO')
@click.option('-k', '--key', help='the private key for signing')
def auto_download(username, password, nro, key):
    sid = sign_in(username, password)

    key = keygen(key)

    key_reg(sid, key.public_key) and accept(sid, nro) and sig_sig(sid, nro, key.private_key) and download(sid)


cli.add_command(register)
# cli.add_command(sign_in)
# cli.add_command(key_reg)
# cli.add_command(upload)
# cli.add_command(accept)
# cli.add_command(download)
cli.add_command(get_nrr)
cli.add_command(abort)
cli.add_command(auto_upload)
cli.add_command(auto_download)
