
class Published(object):
    """ If the _Broker_ is able to fulfill and allow the publication, it
    answers by sending a "PUBLISHED" message to the _Publisher_

       [PUBLISHED, SUBSCRIBE.Request|id, publication|id]

    """
    WAMP_CODE = 17
    name = "published"

    def __init__(self, request_id, publication_id):
        super(Published, self).__init__()

        self.request_id = request_id
        self.publication_id = publication_id

    @property
    def message(self):
        return [
            self.WAMP_CODE, self.request_id, self.publication_id,
        ]
