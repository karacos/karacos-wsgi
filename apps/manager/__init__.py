
import karacos
import os
import core
curdir = os.path.dirname(__file__)

class DomainsList(dict):
    def __init__(self, domains):
        for domain in domains:
            self[domain.value['name']] = domain.value