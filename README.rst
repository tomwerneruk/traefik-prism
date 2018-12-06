==============================
Docker Traefik Event Forwarder
==============================


.. image:: https://img.shields.io/pypi/v/traefik_prism.svg
        :target: https://pypi.python.org/pypi/traefik_prism

.. image:: https://img.shields.io/travis/tomwerneruk/traefik_prism.svg
        :target: https://travis-ci.org/tomwerneruk/traefik_prism

.. image:: https://readthedocs.org/projects/docker-traefik-prism/badge/?version=latest
        :target: https://docker-traefik-prism.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Docker Traefik Event Forwarder


* Free software: BSD license
* Documentation: https://docker-traefik-prism.readthedocs.io.


Features
--------

* Pulls config from one Traefik instance to another to avoid exposing orchestrators (mainly Docker socket) in internet facing containers

Usage
--------

Configured via env variables;

* Pulls config from /api on endpoint defined in SRC_TRAEFIK
* Extracts backend config from a comma-separated list of providers in PROVIDERS
* Pushes config based on DEST_TRAEFIK TO /api/providers/rest

To integrate, extend the 'config generator' pattern seen in https://docs.traefik.io/user-guide/cluster-docker-consul/;

* create a treafik container with the REST provider enabled (--rest), but not bound to docker socket (this will become your frontend)
* another which is (which the only purpose is to generate config based on orchestrator events).

Example Compose;

.. code::

    version: "3.6"
    services:
      traefik_dockerinit:
        image: traefik:1.6
        command:
          - "storeconfig"
          - "--loglevel=debug"
          - "--api"
          - "--entrypoints=Name:http Address::80 Redirect.EntryPoint:https"
          - "--entrypoints=Name:https Address::443 TLS TLS.SniStrict:true TLS.MinVersion:VersionTLS12"
          - "--defaultentrypoints=http,https"
          - "--acme"
          - "--acme.storage=traefik/acme/account"
          - "--acme.entryPoint=https"
          - "--acme.httpChallenge.entryPoint=http"
          - "--acme.onHostRule=true"
          - "--acme.onDemand=false"
          - "--acme.email=hello@example.com"
          - "--docker"
          - "--docker.swarmMode"
          - "--docker.domain=test.example.com"
          - "--docker.watch"
          - "--consul"
          - "--consul.endpoint=consul:8500"
          - "--consul.prefix=traefikdocker"
          - "--rest"
        networks:
          - traefik
        deploy:
          restart_policy:
            condition: on-failure
        depends_on:
          - consul
    
      traefik_init:
        image: traefik:1.6
        command:
          - "storeconfig"
          - "--loglevel=debug"
          - "--api"
          - "--entrypoints=Name:http Address::80 Redirect.EntryPoint:https"
          - "--entrypoints=Name:https Address::443 TLS TLS.SniStrict:true TLS.MinVersion:VersionTLS12"
          - "--defaultentrypoints=http,https"
          - "--acme"
          - "--acme.storage=traefik/acme/account"
          - "--acme.entryPoint=https"
          - "--acme.httpChallenge.entryPoint=http"
          - "--acme.onHostRule=true"
          - "--acme.onDemand=false"
          - "--acme.email=test@example.com
          - "--consul"
          - "--consul.endpoint=consul:8500"
          - "--consul.prefix=traefik"
          - "--rest"
        networks:
          - traefik
        deploy:
          restart_policy:
            condition: on-failure
        depends_on:
          - consul
    
      traefikgen:
        image: traefik:1.6
        depends_on:
          - traefik_dockerinit
          - consul
        command:
          - "--consul"
          - "--consul.endpoint=consul:8500"
          - "--consul.prefix=traefikdocker"
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
        networks:
          - traefik
        deploy:
          restart_policy:
            condition: on-failure
    
      traefik:
        image: traefik:1.6
        depends_on:
          - traefik_init
          - consul
        command:
          - "--consul"
          - "--consul.endpoint=consul:8500"
          - "--consul.prefix=traefik"
        networks:
          - traefik
        ports:
          - target: 80
            published: 80
            mode: host
          - target: 443
            published: 443
            mode: host
          - target: 8080
            published: 8080
            mode: host
        deploy:
          mode: global
          placement:
            constraints:
              - node.role == manager
          update_config:
            parallelism: 1
            delay: 10s
          restart_policy:
            condition: on-failure
     
      consul:
        image: consul
        command: agent -server -bootstrap-expect=1 -ui
        volumes:
          - consul-data:/consul/data
        environment:
          - CONSUL_LOCAL_CONFIG={"datacenter":"us_east2","server":true}
          - CONSUL_BIND_INTERFACE=eth0
          - CONSUL_CLIENT_INTERFACE=eth0
        ports:
          - target: 8500
            published: 8539
            mode: host
        deploy:
          replicas: 1
          placement:
            constraints:
              - node.role == manager
          restart_policy:
            condition: on-failure
        networks:
          - traefik
    
      traefik_config_prism:
        image: tomwerneruk/traefik-prism:latest
        environment:
          - PYTHONUNBUFFERED=1
          - BACKENDS=docker
          - SRC_TRAEFIK=http://traefikgen:8080/
          - DEST_TRAEFIK=http://traefik:8080/
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
        networks:
          - traefik
    
    networks:
      traefik:
        driver: overlay
    
    volumes:
      consul-data:
          driver: local


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage 