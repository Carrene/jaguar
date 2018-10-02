from nanohttp import HTTPKnownStatus


class CASServerNotFound(HTTPKnownStatus):
    status = '617 CAS Server Not Found'


class CASServerNotAvailable(HTTPKnownStatus):
    status = '800 CAS Server Not Available'


class CASInternallError(HTTPKnownStatus):
    status = '801 CAS Server Internal Error'

