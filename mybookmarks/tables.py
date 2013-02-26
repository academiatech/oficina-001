from asyncdynamo.orm.table import Table


class UserTable(Table):

    def __init__(self):
        self.name = 'User'
        self.key = 'id'


class BookmarkTable(Table):

    def __init__(self):
        self.name = 'Bookmark'
        self.key = 'user_id'

    def _get_keyschema(self):
        return {
            "HashKeyElement": {
                "AttributeName": self.key,
                "AttributeType": "S"
            },
            "RangeKeyElement": {
                "AttributeName": 'url',
                "AttributeType": "S"
            }
        }
