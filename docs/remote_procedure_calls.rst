Remote Procedure Calls
======================

Classic
-------

Conventional remote procedure calling over Crossbar.io.

::

    from wampy.peers import Client
    from wampy.peers.routers import Crossbar

    with Client(router=Crossbar()) as client:
        result = client.call("example.app.com.endpoint", *args, **kwargs)


Microservices
-------------

Inspired by the `nameko`_ project.

::

    from wampy.peers import Client
    from wampy.peers.routers import Crossbar

    with Client(router=Crossbar()) as client:
        result = client.rpc.endpoint(**kwargs)

See `nameko_wamp`_ for usage.

.. _nameko: https://github.com/nameko/nameko
.. _nameko_wamp: https://github.com/noisyboiler/nameko-wamp

Register / provide RPC
----------------------

::

    from wampy.peers import Client
    from wampy.messages.error import Error

    def rpc_handler(*args, **kwargs):
        print("rpc_handler called : ", args, kwargs)
        return 42

    client = Client()
    client.start()
    result = client.register(rpc_handler, "myservice.rpc")
    if isinstance(result, Error):
        print (result)
    else:
        assert result == True
