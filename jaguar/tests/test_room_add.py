from bddrest.authoring import response, when, Update, status

from jaguar.models.membership import Member
from jaguar.models.target import Room
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestAddToRoom(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.user = Member(
            email='user@example.com',
            title='user',
            first_name='user1_first_name',
            last_name='user1_last_name',
            access_token='access token',
            reference_id=1
        )
        session.add(cls.user)
        cls.user1 = Member(
            email='user1@example.com',
            title='user1',
            first_name='user1_first_name',
            last_name='user1_last_name',
            access_token='access token1',
            reference_id=2
        )
        session.add(cls.user1)
        cls.blocked1 = Member(
            email='blocked1@example.com',
            title='blocked1',
            first_name='blocked1_first_name',
            last_name='blocked1_last_name',
            access_token='access token3',
            reference_id=4
        )
        cls.blocked2 = Member(
            email='blocked2@example.com',
            title='blocked2',
            first_name='blocked2_first_name',
            last_name='blocked2_last_name',
            access_token='access token',
            reference_id=6
        )
        cls.room_member = Member(
            email='member@example.com',
            title='member',
            first_name='member_first_name',
            last_name='member_last_name',
            access_token='access token',
            reference_id=3
        )
        cls.never = Member(
            email='never@example.com',
            title='never',
            first_name='first_naver_name',
            last_name='last_naver_name',
            access_token='access token',
            add_to_room=False,
            reference_id=7
        )
        session.add(cls.never)
        cls.blocker = Member(
            email='blocker@example.com',
            title='blocker',
            first_name='blocker_first_name',
            last_name='blocker_last_name',
            access_token='access token4',
            reference_id=5,
            blocked_members=[cls.blocked1, cls.blocked2]
        )
        session.add(cls.blocker)
        room = Room(title='example', type='room', members=[cls.room_member])
        session.add(room)
        session.commit()

    def test_add_user_to_room(self):
        self.login('user@example.com')

        with cas_mockup_server(), self.given(
            'Add to a room',
            '/apiv1/rooms/id:1',
            'ADD',
            form=dict(userId=self.user1.reference_id),
        ):
            assert status == 200
            assert len(response.json['memberIds']) == 2

            when(
                'Already added to the room',
                form=Update(userId=self.room_member.reference_id)
            )
            assert status == '604 Already Added To Target'

            when('Member not exists', form=Update(userId=10))
            assert status == '611 Member Not Found'

            when(
                'Not allowed to add this person to any room',
                 form=Update(userId=self.never.reference_id)
            )
            assert status == '602 Not Allowed To Add This Person To Any Room'

            when('Room not exist', url_parameters=Update(id='2'))
            assert status == '612 Room Not Found'

            self.logout()
            self.login('blocked1@example.com')
            when(
                'Blocked by the target user',
                form=Update(userId=self.blocker.reference_id),
                authorization=self._authentication_token
            )
            assert status == '601 Not Allowed To Add Member To Any Room'

            self.logout()
            self.login('blocker@example.com')
            when(
                'The blocker can not add the user he blocked',
                form=Update(userId=4),
                authorization=self._authentication_token
            )
            assert status == '601 Not Allowed To Add Member To Any Room'

