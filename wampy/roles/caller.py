# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from wampy.errors import RemoteError, WampProtocolError
from wampy.messages import MESSAGE_TYPE_MAP
from wampy.messages import Message
from wampy.messages.call import Call

logger = logging.getLogger('wampy.rpc')


class CallProxy:
    """ Proxy wrapper of a `wampy` client for WAMP application RPCs.

    Applictions and their endpoints are identified by dot delimented
    strings, e.g. ::

        "com.example.endpoints"

    and a `CallProxy` object will call such and endpoint, passing in
    any `args` or `kwargs` necessary.

    """
    def __init__(self, client):
        self.client = client

    def __call__(self, procedure, *args, **kwargs):
        message = Call(procedure=procedure, args=args, kwargs=kwargs)
        response = self.client.make_rpc(message)
        wamp_code = response.WAMP_CODE

        if wamp_code == Message.ERROR:
            logger.error("call returned an error: %s", response)
            return response
        elif wamp_code == Message.RESULT:
            return response.value

        raise WampProtocolError("unexpected response: %s", response)


class RpcProxy:
    """ Proxy wrapper of a `wampy` client for WAMP application RPCs
    where the endpoint is a non-delimted single string name, such as
    a function name, e.g. ::

        "get_data"

    The typical use case of this proxy class is for microservices
    where endpoints are class methods.

    """
    def __init__(self, client):
        self.client = client

    def __getattr__(self, name):

        def wrapper(*args, **kwargs):
            message = Call(procedure=name, args=args, kwargs=kwargs)
            response = self.client.make_rpc(message)

            wamp_code = response.WAMP_CODE
            if wamp_code == Message.ERROR:
                _, _, request_id, _, error_api, exc_args, exc_kwargs = (
                    response.message)

                raise RemoteError(
                    error_api, request_id, *exc_args, **exc_kwargs
                )

            if wamp_code != Message.RESULT:
                raise WampProtocolError(
                    'unexpected message code: "%s (%s) %s"',
                    wamp_code, MESSAGE_TYPE_MAP[wamp_code],
                    response[5]
                )

            result = response.value
            logger.debug("RpcProxy got result: %s", result)
            return result

        return wrapper
