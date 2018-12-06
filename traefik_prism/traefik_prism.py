# -*- coding: utf-8 -*-
import requests
import time
import functools
import os
import json
from urllib.parse import urljoin
import logging
import sys

def merge_config(config, providers):
    frontends = {}
    backends = {}

    for provider in providers.split(','):
        backends.update(config[provider]['backends'])
        frontends.update(config[provider]['frontends'])
        
    merged_config = {}
    merged_config['frontends'] = frontends
    merged_config['backends'] = backends
    # TODO consider namespacing each provider's config to avoid conflicts when merging to web
    logging.debug("Merged config")
    logging.debug(merged_config)
    logging.debug("================================")
    return merged_config

def pull_dynamic_config(src, src_auth):
    r = requests.get(src)
    config = r.json()
    logging.debug("Retrieved config")
    logging.debug(config)
    logging.debug("================================")
    return config

def push_dynamic_config(dest, dest_auth, config):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.put(dest, data=json.dumps(config), headers=headers)
    if r.status_code != 200:
        logging.critical("Update code [%s]" % r.status_code)
        logging.critical("Update response [%s]" % r.text)
    else:
        logging.info("Update code [%s]", r.status_code)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    providers = os.getenv('PROVIDERS')
    src_traefik_endpoint = os.getenv('SRC_TRAEFIK')
    dest_traefik_endpoint = os.getenv('DEST_TRAEFIK')

    if providers and src_traefik_endpoint and dest_traefik_endpoint:
        src_traefik_endpoint_clean = urljoin(src_traefik_endpoint, '/api')
        dest_traefik_endpoint_clean = urljoin(dest_traefik_endpoint, '/api/providers/rest')
        logging.debug("Environment Set")
    else:
        logging.critical("env not set - need PROVIDERS, SRC_TRAEFIK and DEST_TRAEFIK")
        exit(-1)

    src_traefik_endpoint_auth = os.getenv('SRC_TRAEFIK_AUTH', None)
    src_traefik_endpoint_auth_file = os.getenv('SRC_TRAEFIK_AUTH_FILE', None)
    dest_traefik_endpoint_auth = os.getenv('DEST_TRAEFIK_AUTH', None)
    dest_traefik_endpoint_auth_file = os.getenv('DEST_TRAEFIK_AUTH_FILE', None)

    while True:
        logging.info("Pulling config from [%s]" % src_traefik_endpoint_clean)
        config = pull_dynamic_config(src_traefik_endpoint_clean,'')
        logging.info("Pushing config to [%s]" % dest_traefik_endpoint_clean)
        push_dynamic_config(dest_traefik_endpoint_clean, '', merge_config(config, providers))
        logging.info("Sleeping for 15s")
        time.sleep(15)

if __name__ == "__main__":
    main()
