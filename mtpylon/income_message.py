# -*- coding: utf-8 -*-
from typing import Union

from .messages.types import MtprotoMessage
from .service_schema.constructors.message import Message


IncomeMessage = Union[MtprotoMessage, Message]
