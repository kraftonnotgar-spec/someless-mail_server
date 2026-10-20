import pytest
from someless import domain_records
from someless.engine import names


def test_outgoing_authentication_requires_ownership_and_signing(monkeypatch):
    monkeypatch.setenv('SOMELESS_OUTBOUND_ONLY', '1')
    found = {key: {'state': 'found'} for key in ('code', 'spf', 'dkim', 'dmarc')}
    assert domain_records.authenticated(found)
    for key in found:
        assert not domain_records.authenticated({k: v for k, v in found.items() if k != key})
    monkeypatch.delenv('SOMELESS_OUTBOUND_ONLY')
    assert not domain_records.authenticated(found)


def test_outgoing_hostname_and_mx_guidance(monkeypatch):
    monkeypatch.setenv('SOMELESS_OUTBOUND_ONLY', '1')
    monkeypatch.setenv('SOMELESS_SMTP_HOSTNAME', 'email.example.com')
    assert names.server_name() == 'email.example.com'
    assert 'keep your existing MX records' in domain_records.receive_note('example.com', {})
