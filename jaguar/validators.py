import re

from nanohttp import validate


TITLE_PATTERN = re.compile(r'^(?!\s).*[^\s]$')


create_room_validator = validate(
    title=dict(
        min_length=(1, '701 Must Be Greater Than 1 Charecters'),
        max_length=(50, '702 Must Be Less Than 50 Charecters'),
        required='703 Room Title Is Required',
    )
)


kick_member_validator = validate(
    memberId=dict(
        type_=(int, '705 Invalid Member Id'),
        required='709 Member Id Is Required',
    )
)


add_contact_validator = validate(
    userId=dict(
        type_=(int, '705 Invalid Member Id'),
        required='709 Member Id Is Required',
    )
)


create_direct_validator = validate(
    userId=dict(
        type_=(int, '705 Invalid Member Id')
    )
)


search_member_validator = validate(
    query=dict(
        max_length=(20, '702 Must Be Less Than 20 Charecters'),
        required='708 Search Query Is Required',
    )
)


send_message_validator = validate(
    body=dict(
        max_length=(1024, '702 Must be less than 1024 charecters'),
        required='400 Bad Request',
    )
)


edit_message_validator = validate(
    body=dict(
        max_length=(1024, '702 Must be less than 1024 charecters'),
        required='400 Bad Request',
    )
)


reply_message_validator = validate(
    body=dict(
        max_length=(1024, '702 Must be less than 1024 charecters'),
        required='712 Message Body Required',
    ),
    mimetype=dict(
        required='713 Message Mimetype Required'
    )
)

