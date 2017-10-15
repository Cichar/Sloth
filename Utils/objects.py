# -*- coding:utf-8 -*-

from http import HTTPStatus

normal_response = {v: v.phrase for v in HTTPStatus.__members__.values()}
