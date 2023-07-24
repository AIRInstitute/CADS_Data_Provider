import jwt
import uuid
import time
import requests

from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.hazmat.primitives import serialization
from cryptography import x509

filepath = 'rlopez.p12'
password = 'CdxXF9wB'

filepath = 'proint.p12'
password = '4VYAAvdy'

def p12_read(filepath, password):
    # Leer el archivo PKCS12
    with open(filepath, 'rb') as f:
        p12_data = f.read()

    # Cargar clave privada, certificado y CA certs
    private_key, certificate, ca_certs = load_key_and_certificates(p12_data, password.encode())

    # Convertir la clave privada a formato PEM
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # Convertir el certificado a formato PEM
    certificate_pem = certificate.public_bytes(encoding=serialization.Encoding.PEM).decode()

    # Convertir los certificados de CA a formato PEM
    ca_certs_pem = [ca_cert.public_bytes(encoding=serialization.Encoding.PEM).decode() for ca_cert in ca_certs]

    return certificate_pem, private_key_pem, ca_certs_pem


def x5c_read(filepath, password):
    # Obtener el certificado del archivo PKCS12 en formato PEM
    certificate_pem, _, _ = p12_read(filepath, password)

    # Convertir PEM a base64 (eliminar encabezado y pie de página y juntar líneas)
    b64_cert = certificate_pem.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")

    # El campo x5c contiene el certificado en base64
    x5c = [b64_cert]
    
    return x5c

certificate, private_key, ca_certs = p12_read(filepath, password)
#print("Certificate:", certificate)
#print("Private Key:", private_key)
#print("CA Certificates:", ca_certs)

x5c = x5c_read(filepath, password)
#print("x5c:", x5c)


# Datos para la generación del client_assertion

clientID = "EU.EORI.ES64973164978542"
#clientID =  "EU.EORI.ESG37571627"
satelliteID = "EU.EORI.NLi4TRUSTSAT"
satelliteURL = "https://mw.i4trustsat.ishareworks.nl"
'''
pub_key = b"-----BEGIN CERTIFICATE-----MIIFYDCCBEigAwIBAgIIV/6fc2q5A7UwDQYJKoZIhvcNAQELBQAwPDE6MDgGA1UEAwwxVEVTVCBpU0hBUkUgRVUgSXNzdWluZyBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eSBHNTAeFw0yMzA1MDMxMzMwMjJaFw0yNjA1MDIxMzMwMjFaMIHFMSowKAYDVQQDDCFQUk9JTlQgUHJvamVjdGVuIEludGVybmF0aW9uYWwgU0wxITAfBgNVBAUTGEVVLkVPUkkuRVM2NDk3MzE2NDk3ODU0MjEqMCgGA1UECwwhUFJPSU5UIFByb2plY3RlbiBJbnRlcm5hdGlvbmFsIFNMMSowKAYDVQQKDCFQUk9JTlQgUHJvamVjdGVuIEludGVybmF0aW9uYWwgU0wxDzANBgNVBAcMBk1hZHJpZDELMAkGA1UEBhMCRVMwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQCdqIA2R8CWl+LGJ1eS2LFpDfUWb9YhC9Sy1369cStSKQZHs6k1XueoROHbWWar4CqqjBln1EkIRgG6rS5ixJ3UfJq24tP3eFi4K/FOgM8DEntCIFsn9k/D9EdBZUtjTkf5Kj5Sai5uPvVN/F79mS1m2/bEVn1IJ4zWSlO6pgkuwtK/00tyMnoOZm7Nbstv06LOJrhl7vViBMnzAd2qoZx+dXNpcHRHgq77Vltvza0Ic9D4mtZlj1pf3KiK5l+RVsWW7w9dBhED8nS+1HdjS2mZedoeOtKEWhc+EbdVEtdC5gzQbE2IAcP1JYZLJLs9PzjEyvA286lJVx9YQ4L69wtXjVUtxhC8iq/3gSAF28pcARFVWIKtuHMckZQAR6SUHozyIWSn3sh+qJaAtpjBO7VZKvSd1CahH7XDb3lNeO+Z+IDDuCO2klxVEQ52ZRO2mlCSUfqzF8GyJxRYrPRcTaknzzXYXy7iNDEnIZdaC31NFLT2Pwi3o5OAlHmCLUMgK9PXx7DYMEr574CiZ5mTcRvZLipGw3yPZtBn+sgLv3CaX4dx6xJP2fwu8dx9GmKpZiwyOOJXtmUhO2bpoNcQOO1RyzHT2rAgvRf94F5uAQRAURtcb2pesuLMsfCm8pavCJuCPWV80xThyeLNMi5zXUlO3BLAYNpRNjI8aoFiYmRyNwIDAQABo4HbMIHYMB8GA1UdIwQYMBaAFG3FZYnL35FU0Ws8twKlLs2KaJAdMCQGA1UdEQQdMBuBGXJhbG9uc29AYWlyLWluc3RpdHV0ZS5jb20wJwYDVR0lBCAwHgYIKwYBBQUHAwIGCCsGAQUFBwMEBggrBgEFBQcDATA3BggrBgEFBQcBAwQrMCkwCAYGBACORgEBMAgGBgQAjkYBBDATBgYEAI5GAQYwCQYHBACORgEGAjAdBgNVHQ4EFgQUJWMkGNW1uc3/9ddejsPQsTwFnHowDgYDVR0PAQH/BAQDAgbAMA0GCSqGSIb3DQEBCwUAA4IBAQBFNQXeFACFaNM7PdLtmRiX4cACtA8nJreCikfirf/hGRx07q+NKqoolaVRBVPTguGzoI+hm7SBD98deILcH/7cHn4+tRzgyHTawOopvCneiCaUBw740FscHm30U3RKzHpidLeNP8M+9VD3kW8i41uCjjzuI6mwypN7LEZ7hypzeR2doVlEjhsIhBe8DetH5i+5+ikMKxfgpe8iqWQ40PXIDXdJG76F8LQAOOEv9PdAKk2oRmbssTLrP1Oh8pWUkKKy73OXFMtxxT2Q4HXAJqzmerzOnYeE0lrEjLsjcyDA/P9TAYPxLKR1S2i9ba5jg5gGS6tKl+L4U/05FIsVYjl/-----END CERTIFICATE-----"

priv_key = """
-----BEGIN PRIVATE KEY-----
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
mE8Aoce2lQVaffQDKQ/uMTQEnC8vKw==
-----END PRIVATE KEY-----
"""

x5c = ["MIIFYDCCBEigAwIBAgIIV/6fc2q5A7UwDQYJKoZIhvcNAQELBQAwPDE6MDgGA1UEAwwxVEVTVCBpU0hBUkUgRVUgSXNzdWluZyBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eSBHNTAeFw0yMzA1MDMxMzMwMjJaFw0yNjA1MDIxMzMwMjFaMIHFMSowKAYDVQQDDCFQUk9JTlQgUHJvamVjdGVuIEludGVybmF0aW9uYWwgU0wxITAfBgNVBAUTGEVVLkVPUkkuRVM2NDk3MzE2NDk3ODU0MjEqMCgGA1UECwwhUFJPSU5UIFByb2plY3RlbiBJbnRlcm5hdGlvbmFsIFNMMSowKAYDVQQKDCFQUk9JTlQgUHJvamVjdGVuIEludGVybmF0aW9uYWwgU0wxDzANBgNVBAcMBk1hZHJpZDELMAkGA1UEBhMCRVMwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQCdqIA2R8CWl+LGJ1eS2LFpDfUWb9YhC9Sy1369cStSKQZHs6k1XueoROHbWWar4CqqjBln1EkIRgG6rS5ixJ3UfJq24tP3eFi4K/FOgM8DEntCIFsn9k/D9EdBZUtjTkf5Kj5Sai5uPvVN/F79mS1m2/bEVn1IJ4zWSlO6pgkuwtK/00tyMnoOZm7Nbstv06LOJrhl7vViBMnzAd2qoZx+dXNpcHRHgq77Vltvza0Ic9D4mtZlj1pf3KiK5l+RVsWW7w9dBhED8nS+1HdjS2mZedoeOtKEWhc+EbdVEtdC5gzQbE2IAcP1JYZLJLs9PzjEyvA286lJVx9YQ4L69wtXjVUtxhC8iq/3gSAF28pcARFVWIKtuHMckZQAR6SUHozyIWSn3sh+qJaAtpjBO7VZKvSd1CahH7XDb3lNeO+Z+IDDuCO2klxVEQ52ZRO2mlCSUfqzF8GyJxRYrPRcTaknzzXYXy7iNDEnIZdaC31NFLT2Pwi3o5OAlHmCLUMgK9PXx7DYMEr574CiZ5mTcRvZLipGw3yPZtBn+sgLv3CaX4dx6xJP2fwu8dx9GmKpZiwyOOJXtmUhO2bpoNcQOO1RyzHT2rAgvRf94F5uAQRAURtcb2pesuLMsfCm8pavCJuCPWV80xThyeLNMi5zXUlO3BLAYNpRNjI8aoFiYmRyNwIDAQABo4HbMIHYMB8GA1UdIwQYMBaAFG3FZYnL35FU0Ws8twKlLs2KaJAdMCQGA1UdEQQdMBuBGXJhbG9uc29AYWlyLWluc3RpdHV0ZS5jb20wJwYDVR0lBCAwHgYIKwYBBQUHAwIGCCsGAQUFBwMEBggrBgEFBQcDATA3BggrBgEFBQcBAwQrMCkwCAYGBACORgEBMAgGBgQAjkYBBDATBgYEAI5GAQYwCQYHBACORgEGAjAdBgNVHQ4EFgQUJWMkGNW1uc3/9ddejsPQsTwFnHowDgYDVR0PAQH/BAQDAgbAMA0GCSqGSIb3DQEBCwUAA4IBAQBFNQXeFACFaNM7PdLtmRiX4cACtA8nJreCikfirf/hGRx07q+NKqoolaVRBVPTguGzoI+hm7SBD98deILcH/7cHn4+tRzgyHTawOopvCneiCaUBw740FscHm30U3RKzHpidLeNP8M+9VD3kW8i41uCjjzuI6mwypN7LEZ7hypzeR2doVlEjhsIhBe8DetH5i+5+ikMKxfgpe8iqWQ40PXIDXdJG76F8LQAOOEv9PdAKk2oRmbssTLrP1Oh8pWUkKKy73OXFMtxxT2Q4HXAJqzmerzOnYeE0lrEjLsjcyDA/P9TAYPxLKR1S2i9ba5jg5gGS6tKl+L4U/05FIsVYjl/"]
#       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"]
'''
priv_key = private_key


# Creación del header para el JWT
header = {}
header["typ"] = "JWT"
header["x5c"] = x5c

# Creación del payload para el JWT
iss = clientID
sub = clientID
#aud = satelliteID
aud = clientID
jti = str(uuid.uuid1())
iat = int(time.time())
exp = iat + 30

payload = {
    "iss": iss,
    "sub": sub,
    "aud": aud,
    "jti": jti,
    "iat": iat,
    "exp": exp
}

# Generación del client_assertion
client_assertion = jwt.encode(payload, priv_key, headers=header, algorithm="RS256")
print("client_assertion:" + client_assertion)

# URL de Keyrock
keyrock_url = "https://keyrock-ds5.dev.cads.co.ua/oauth2/token"  # Reemplaza <KEYROCK_URL> con la URL de tu instancia de Keyrock
#keyrock_url = "https://ar.isharetest.net/connect/token"
#keyrock_url = "https://mw.i4trustsat.ishareworks.nl/connect/token"
#keyrock_url = "https://scheme.isharetest.net/connect/token"

# Headers para la solicitud HTTP POST
http_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Datos para la solicitud HTTP POST
post_data = {
    'grant_type': 'client_credentials',
    'scope': 'iSHARE',
    'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
    'client_assertion': client_assertion,
    'client_id': clientID
}

'''post_data = {
    "grant_type": "urn-ietf:params:oauth:grant-type:jwt-bearer",
    "scope": "iSHARE",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": client_assertion,
    "client_id": clientID
}'''

print("POST")
# Realizar la solicitud HTTP POST
response = requests.post(keyrock_url, headers=http_headers, data=post_data)

# Imprimir la respuesta
print(f"POST request to {keyrock_url}")
print(f"POST payload to {post_data}")
print(f"Status code {response.status_code}")
print(f"Response: {response.text}")
