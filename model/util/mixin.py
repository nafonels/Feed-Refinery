#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.exc import NoForeignKeysError

__version__ = "$"


class ArgumentedTableMixin(object):
    @classmethod
    # noinspection PyUnresolvedReferences
    def return_item(cls, target_id: object) -> object:
        result = cls.query.filter(cls.id == target_id).first()  # type: cls
        return result

    @classmethod
    def return_list_of_every_item(cls):
        try:
            ret = cls.query.all()
        except NoForeignKeysError:
            ret = []
        return ret
