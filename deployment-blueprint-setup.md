# Blueprint outgoing mail

The server at `/opt/someless-mail` sends mail for blueprintsolutions.co.tz. Incoming mail and historical messages remain on cPanel. Keep the current MX records and nameservers.

## Configure each email app

Change only the outgoing SMTP server:

- Server: email.krafton.my.id
- Port: 587
- Encryption: STARTTLS
- Authentication: required
- Username and password: use that address's entry in deployment-blueprint-smtp-credentials.json
- Alternative: port 465 with SSL/TLS

Turn off “use same credentials as incoming server” for outgoing SMTP. Keep the account's existing email address, incoming server, incoming username and incoming password. Do not delete or recreate the account.

Credentials were created for careers, elizabeth, info, jafari, kassim, shamte and winnie at blueprintsolutions.co.tz. Add other addresses as Senders in Someless and generate SMTP keys for them. SMTP keys follow Someless's existing permission model: each valid key may send as any enabled Sender listed in the panel. Store them privately.

## Deployment

Mail data: hard 2 GiB cap. Memory: 768 MiB, CPU: 0.75, Docker logs: 2 x 5 MB. Only submission ports 587 and 465 are published. The HTTPS panel uses existing Traefik routing without restarting Traefik. No incoming mailboxes are hosted here.

This installation includes source overrides for outgoing-only domain verification and MX routing. They are mounted read-only from `/opt/someless-mail/overrides`. Do not remove those overrides or upgrade the image without checking compatibility. The source changes are in this workspace.

The host script `/opt/someless-mail/sync_proxy_certificate.py` reads only this hostname's certificate from the existing Traefik ACME store, then imports it into Stalwart. `/etc/cron.d/someless-mail-tls` checks every 15 minutes. Errors go to syslog under someless-mail-tls.

Domain ownership, SPF, DKIM and DMARC are required in outgoing-only mode; incoming MX and a new mail subdomain are not required. TLS uses email.krafton.my.id. For delivery reputation, set the VPS IP's PTR/reverse DNS at the VPS provider to email.krafton.my.id; it currently uses srv1670294.hstgr.cloud.

Changing SMTP on the server does not update Outlook or phones automatically. Each client must apply the settings above. Successful SMTP submission does not by itself prove inbox placement at Gmail/Outlook; a user-accessible external test inbox is still needed to verify that.

Validation: seven separate SMTP accounts authenticated over publicly verified STARTTLS on 587. TLS on 465 passed. Unauthenticated mail and an unauthorized sender were rejected. A tracked test was delivered to info@blueprintsolutions.co.tz on its existing cPanel MX. An earlier test before the final routing correction bounced locally; the final MX-route test succeeded. External Gmail/Outlook inbox placement has not been tested.
