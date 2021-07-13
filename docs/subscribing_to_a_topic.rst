Subscribing to a Topic
======================

You need a long running wampy application process for this.

::

    from wampy.peers.clients import Client
    from wampy.roles.subscriber import subscribe


    class WampyApp(Client):

        @subscribe(topic="topic-name")
        def weather_events(self, topic_data):
            # do something with the ``topic_data`` here
            pass


See `runnning a wampy application`_ for executing the process.


.. _runnning a wampy application: a_wampy_application.html#running-the-application


Or you can use the ``client.subscribe()`` method:

::

    from wampy.peers.clients import Client
    from wampy.messages.error import Error

    client = Client()

    def subscr_handler(*args, **kwargs):
        print("subscr_handler called : ", args, kwargs)

    client.start()
    result = client.subscribe(subscr_handler, "myservice.topic")
    if isinstance(result, Error):
        print (result)
    else:
        assert result == True
