import json

def main():
    dict1 = json.loads('''{"backends":{"backend-ghost-ghost":{"servers":{"server-ghost-ghost-1-99770bddaba48339278f05e1f45d7d9c":{"url":"http://10.0.1.6:2368","weight":1}},"loadBalancer":{"method":"wrr"}},"backend-ghost-talk":{"servers":{"server-ghost-talk-1-2e31ab03ae2be608fe90ecaa19db7917":{"url":"http://10.0.1.3:3000","weight":1}},"loadBalancer":{"method":"wrr"}}},"frontends":{"frontend-Host-fluffycloudsandlines-blog-0":{"entryPoints":["http","https"],"backend":"backend-ghost-ghost","routes":{"route-frontend-Host-fluffycloudsandlines-blog-0":{"rule":"Host:fluffycloudsandlines.blog"}},"passHostHeader":true,"priority":0,"basicAuth":[]},"frontend-Host-talk-fluffycloudsandlines-blog-1":{"entryPoints":["http","https"],"backend":"backend-ghost-talk","routes":{"route-frontend-Host-talk-fluffycloudsandlines-blog-1":{"rule":"Host:talk.fluffycloudsandlines.blog"}},"passHostHeader":true,"priority":0,"basicAuth":[]}}}''')
    dict2 = json.loads('''{
    "frontends": {
      "frontend2": {
        "routes": {
          "test_2": {
            "rule": "Path:/test"
          }
        },
        "backend": "backend1"
      },
      "frontend1": {
        "routes": {
          "test_1": {
            "rule": "Host:test.localhost"
          }
        },
        "backend": "backend2"
      }
    },
    "backends": {
      "backend2": {
        "loadBalancer": {
          "method": "drr"
        },
        "servers": {
          "server2": {
            "weight": 2,
            "URL": "http://172.17.0.5:80"
          },
          "server1": {
            "weight": 1,
            "url": "http://172.17.0.4:80"
          }
        }
      },
      "backend1": {
        "loadBalancer": {
          "method": "wrr"
        },
        "circuitBreaker": {
          "expression": "NetworkErrorRatio() > 0.5"
        },
        "servers": {
          "server2": {
            "weight": 1,
            "url": "http://172.17.0.3:80"
          },
          "server1": {
            "weight": 10,
            "url": "http://172.17.0.2:80"
          }
        }
      }
    }
}''')
    print (dict1)


if __name__ == "__main__":
    main()
