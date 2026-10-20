#!/usr/bin/env python3
"""Copy only this mail hostname's renewed Traefik certificate into Stalwart."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess

HOST = 'email.krafton.my.id'
ACME = Path('/var/lib/docker/volumes/traefik_data/_data/acme.json')
STAMP = Path('/opt/someless-mail/tls-fingerprint')
INSTALL = '''
import json,sys
from someless import create_app
from someless.engine import client
payload=json.load(sys.stdin)
with create_app().app_context():
    e=client()
    matches=[x for x in e.get('Certificate') if 'email.krafton.my.id' in x.get('subjectAlternativeNames',{})]
    if matches:
        ident=matches[0]['id']; e.update('Certificate',ident,payload)
    else:
        ident=e.create('Certificate',payload)['id']
    e.update('SystemSettings','singleton',{'defaultCertificateId':ident})
    e.action('ReloadSettings')
    e.action('ReloadTlsCertificates')
print('SMTP certificate synchronized')
'''

def main():
    data=json.loads(ACME.read_text())
    cert=next(item for resolver in data.values() for item in resolver.get('Certificates',[]) if HOST in [item['domain']['main'],*item['domain'].get('sans',[])])
    digest=hashlib.sha256(cert['certificate'].encode()).hexdigest()
    if STAMP.exists() and STAMP.read_text()==digest:
        return
    payload={'certificate':{'@type':'Text','value':base64.b64decode(cert['certificate']).decode()},'privateKey':{'@type':'Text','secret':base64.b64decode(cert['key']).decode()}}
    subprocess.run(['docker','exec','-i','-u','someless','someless-mail','python','-c',INSTALL],input=json.dumps(payload),text=True,check=True,timeout=90)
    STAMP.write_text(digest)

if __name__=='__main__':
    main()
