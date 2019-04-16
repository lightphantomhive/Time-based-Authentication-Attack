# -*- coding: utf-8 -*-

import time
from pwn import log
from .config import (DEFAULT_CHARSET,
                     DEFAULT_TOKEN_LENGTH,
                     DEFAULT_HIDDEN_CHAR
                     )


class TimeAuthChecker(object):

    def __init__(self,
                 charset=DEFAULT_CHARSET,
                 token_length=DEFAULT_TOKEN_LENGTH,
                 base_token="",
                 hidden_char=DEFAULT_HIDDEN_CHAR,
                 break_on_time=0):

        self._charset = charset
        self._token_length = token_length
        self._hidden_char = hidden_char
        self._break_on_time = break_on_time
        self._token = [c for c in base_token] + [self._hidden_char for _ in range(self._token_length - len(base_token))]

    
    def _avg(self, l):

        return sum(l) / float(len(l))

    def request(self):

    	raise NotImplementedError('You should implement this one')

    def get_token(self):

        return ''.join(self._token)

    def _get_token_offsets(self):

        return range(len(''.join(self._token).rstrip(self._hidden_char)), self._token_length)

    def _get_timing(self):

        return time.time()

    def _log(self, progress, offset, char, t1, t2, timings, i, best_candidate):
    	
    	progress.status("""
                        Testing character '%c' 
                        Current Flag: [%s]
                        Took: %s
                        Max: %s:%c
                        Avg: %s
                        """ % (
                            char,
                            ''.join(self._token),
                            (t2 - t1),
                            max(timings),
                            best_candidate,
                            self._avg(timings)
                        ))

    def process(self):

        log.info("Start guessing token :")
        progress = log.progress('Progress')
        for offset in self._get_token_offsets():
            timings = []
            for i, char in enumerate(self._charset):
                self._token[offset] = char
                t1 = self._get_timing()
                self.request()
                t2 = self._get_timing()
                timings.append(t2 - t1)
                best_candidate = self._charset[timings.index(max(timings))]
                self._log(progress, offset, char, t1, t2, timings, i, best_candidate)
                if self._break_on_time != 0:
                    if (max(timings) > min(timings) + self._break_on_time):
                        break
            found_char = self._charset[timings.index(max(timings))]
            self._token[offset] = found_char
            log.success("Found Character : %c - Best : %s - Average : %s"
            			%(found_char,
        		        max(timings),
                		self._avg(timings)))
        progress.success("DONE! %s" % (self.get_token()))

    def print_token(self):

        log.success("Your token : [%s]" % self.get_token())
