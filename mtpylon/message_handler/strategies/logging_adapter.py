# -*- coding: utf-8 -*-
import logging
from typing import Any, MutableMapping, Tuple


class MessageLoggerAdapter(logging.LoggerAdapter):

    def process(
        self,
        msg: Any,
        kwargs: MutableMapping[str, Any]
    ) -> Tuple[Any, MutableMapping[str, Any]]:
        message_id = self.extra['message_id']
        return f'[message {message_id}] {msg}', kwargs
