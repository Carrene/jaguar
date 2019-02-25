from nanohttp import HTTPKnownStatus


class CASServerNotFound(HTTPKnownStatus):
    status = '617 CAS Server Not Found'


class CASServerNotAvailable(HTTPKnownStatus):
    status = '800 CAS Server Not Available'


class CASInternallError(HTTPKnownStatus):
    status = '801 CAS Server Internal Error'


class HTTPUnsupportedMediaType(HTTPKnownStatus):
    status = '415 Unsupported Media Type'


class DolhinIssueNotFound(HTTPKnownStatus):
    status = '802 Issue Not Found'


class DolhinIssueNotSubscribed(HTTPKnownStatus):
    status = '803 Issue Not Subscribed'