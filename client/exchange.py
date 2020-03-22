import io
import click
import requests

from base64 import b64encode, b64decode
from urllib.parse import quote

from utils.signing import Key


HOST = 'https://csc8113.jinjo.co.uk/api'


# @click.command()
# @click.argument('name', required=True)
def sign_in(name, password):
    click.echo(f'⏳ Signing for {name} ...')
    r = requests.post(HOST + f'/users/{name}/{password}')
    if r.status_code != 200:
        click.echo(click.style('😭 Failed to sign in', fg='red'))
        click.echo(r.text)
        return None
    else:
        hint = '🎉 User signed in successfully'
        click.echo(click.style(hint, fg='green'))
        click.echo('🎫 Session ID: ' + r.json().get('token'))
        return r.json().get('token')


# @click.command()
# @click.option('-s', '--session', required=True, help='the session ID')
# @click.option('-k', '--key', required=True, help='the public key')
def key_reg(session, key):
    click.echo('⏳ Registering public key to session...')
    r = requests.post(HOST + f'/users/createKey/{session}/{quote(key, safe="")}')
    if r.status_code != 200:
        click.echo(click.style('😭 Failed to register the public key', fg='red'))
        click.echo(r.text)
        return False
    else:
        hint = '🎉 Public key registered successfully'
        click.echo(click.style(hint, fg='green'))
        return True


# @click.command()
# @click.option('-s', '--session', required=True, help='the session ID')
# @click.option('-e', '--email', required=True, help='the email of receiver')
# @click.option('-p', '--path', required=True, help='the file path')
# @click.option('-k', '--key', required=True, help='the private key for signing')
def upload(session, email, path, key):
    click.echo('⏳ Uploading file...')
    key = Key(private_key=key)
    data = open(path, 'rb').read()
    sig = key.sign(data)
    r = requests.post(HOST + f'/exchange/uploadedFile/{session}/{email}/secretfile', files={
        'uploadedFile': data,
        'signature': io.BytesIO(sig)
    })
    if r.status_code != 200:
        click.echo(click.style('😭 Failed to upload the document', fg='red'))
        click.echo(r.text)
        return False
    else:
        hint = '🎉 Document uploaded successfully'
        click.echo(click.style(hint, fg='green'))
        click.echo('🔑 Signature: ' + b64encode(sig).decode('ascii'))
        return True


# @click.command()
# @click.option('-s', '--session', required=True, help='the session ID')
# @click.option('-o', '--nro', required=True, help='the NRO')
# @click.option('-k', '--key', required=True, help='the private key for signing')
def accept(session, nro):
    click.echo('⏳ Accepting document...')
    nro = b64decode(nro)
    r = requests.post(HOST + f'/exchange/acceptDoc/{session}', files={
        'NRO': io.BytesIO(nro),
    })

    if r.status_code != 200:
        click.echo(click.style('😭 Failed to accept the document', fg='red'))
        click.echo(r.text)
        return False
    else:
        hint = '🎉 Document accepted successfully'
        click.echo(click.style(hint, fg='green'))
        return True


def sig_sig(session, nro, key):
    click.echo('⏳ Sending NRR...')
    nro = b64decode(nro)
    key = Key(private_key=key)
    r = requests.post(HOST + f'/exchange/provideNRR/{session}', files={
        'NRR': io.BytesIO(key.sign(nro)),
    })

    if r.status_code != 200:
        click.echo(click.style('😭 Failed to send NRR', fg='red'))
        click.echo(r.text)
        return False
    else:
        hint = '🎉 NRR sent successfully'
        click.echo(click.style(hint, fg='green'))
        return True


# @click.command()
# @click.argument('session', required=True)
def download(session):
    click.echo('⏳ Downloading file...')
    r = requests.get(HOST + f'/exchange/fetchDoc/{session}')
    if r.status_code != 200:
        click.echo(click.style('😭 Failed to download the document', fg='red'))
        click.echo(r.text)
        return False
    else:
        hint = '🎉 Document download successfully'
        click.echo(click.style(hint, fg='green'))
        return True


def keygen(key):
    hint = 'Key pair generated for the session' if key is not None else 'Key pair imported for the session'
    key = Key(private_key=key) if key is not None else Key()

    click.echo(click.style('✨ ' + hint, fg='green'))
    click.echo('🔑 Public key: ' + key.public_key)
    click.echo('🔑 Private key: ' + key.private_key)

    return key
