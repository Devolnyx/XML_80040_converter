import zlib
import base64
from urllib.parse import unquote, quote

a = '7ZhLc7JIFIZ/yyzcTnFRwSXIZwQENYKiG4pLg61AI5eILPjtHxoVYzSTqTgzyShldXXRp7tPv748nKLWYGsUWyMIaJdNjWTKtg5cWYejBo8xUfO5HVqG3+K2o0S7bCOwSmEElAi6Loji4yzD844xydvBwx4W8kOjnLoJwXFajeT2v8PkMsoHQVJFHAY84CQDIzqM7JaMURpZb1cstzB8kES8dJz5GjU2vLQKMyNgLEH0pxuhNLD1MEIJsBKIgm0Exe0PC935Z/aMEyOB1of7YafrnqhtzQSKbosMUcQNwdY6sU/YdhX7nwg3Ko+Txt9KPvyKfII/c/1+L8SISaunP+cjceq197GNfbixS+ydG+dG4J7nsfHAdT05rMZyu7ZR4/AaXcZhu05zd5N4M7TtY8e1dtrGpzIswea4sgM9r408FJ1J8HdFSiIjiLdOec36glxaFzJpr0k2jBznc+TDvly8c9t7YRKQJX/ts48PiULDgsnmi0fc6tqi9u2RSVsPwsB9jXIMLwYnAwp6vX9RENIuVpGAmqV2nDNnfcFuFwevlf45keVkEsX32e7aQM+9ROyNpJgW6DqqsnkQ8qaP+CgIwEpXstVKc100xHOBGJ7Q9EHIj+XD2SybFn66TGiVs3mlyeSbonL4TQn57+KuRpCdDlZeV05O6WKszQaamsEB6uS5258A4dw49wQ7duLoOjahEp+Mw2nfUF5ai3Flhcuwy2hqQRjMJh3N4DAWOMmkTLbK5gG7m5aDoYRZddhrzNYSYzGe5/NBVz337AN29SvyZdRSx9ZA6XFLvF4MXzKhGNKVw38w7M5qu6+iAHKpA3NvXcCGt+43e5Y+4PvnPrsnNioTtZ3NOJtduACZXcl2uPTkNXmZjREwZzhgtLxv8q1kIWfDGeVX2TzYeNNKZkI6ISHhL/xCkNsSz7Rwn0rPPftg4zU2ksoEqkHCpio9jpYhIBdgACqH/2A2loWg4xwKwa+CYB75mxbF0Zo3spqLWTLgFnl47rJ7IuNkPZ7L8tI11XgcmasO6q9lpvLNZTJiUylfEWCMYjAWxdjz4C8prbK5LRn/uA8uXqsZmZU2mIvlv2c0l1OxO2xZG/QZLt6JbNdeJ6qb1h1sOngSB5YFKFGd081DCfRPfDrED98Hy5bdfSVkd/3WJ+lwU1pur1vAQX3JbDGAut1e2FOz4F2wfvl17r1vTcsbiLA2rcxoSBwhaeGkMVGABwd85aTLhNRyS4BB0lx2SdYJO7iEGEyvsvkphPyGBdC1B17usmTU4ELRF7xu8fQUsCPDPPfqvYt3rXq08nxIFnAWiDEaz92YtQ05qjz+oOVnQMHItBZMJFkeseSmTcQtT+nOzx34f6dl+qS0aFGbKcMV4tUnXOvnmFM5adf+Bg=='

def decode_inflate(string):
    data = base64.b64decode(string)
    xml = zlib.decompress(data, wbits=-15)
    xml = unquote(xml)
    return xml

def deflate_encode(string, raw=True):
    zlibbed_str = zlib.compress(quote(string).encode('utf8'))
    #To handle the raw deflate and inflate, without header and checksum, the following things needed to happen:
    # On deflate/compress: strip the first two bytes (header) and the last four bytes (checksum).
    if raw:
        zlibbed_str = zlibbed_str[2:-4]

    encoded = base64.b64encode(zlibbed_str)
    return encoded.decode('utf8')

b = decode_inflate(a)
c = deflate_encode(b)