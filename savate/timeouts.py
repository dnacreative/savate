# -*- coding: utf-8 -*-

from savate.looping import BaseIOEventHandler, POLLIN
from savate.lllsfd import TimerFD, CLOCK_REALTIME, TFD_TIMER_ABSTIME


class Timeouts(BaseIOEventHandler):

    def __init__(self, server):
        BaseIOEventHandler.__init__(self)
        self.server = server
        self.timer = self.sock = TimerFD(clockid = CLOCK_REALTIME)
        # A timestamp -> {handlers} dict
        self.timeouts = {}
        # A handler -> timestamp dict
        self.handlers_timeouts = {}

    @property
    def min_expiration(self):
        return min(self.timeouts)

    def update_timeout(self, handler, expiration):
        if (not self.timeouts) or (expiration < self.min_expiration):
            # Specified expiration is earlier that our current one,
            # update our timer
            self.timer.settime(expiration, flags = TFD_TIMER_ABSTIME)

        # Do we need to update an existing timeout ?
        if handler.sock in self.handlers_timeouts:
            old_expiration = self.handlers_timeouts[handler.sock]
            self.timeouts[old_expiration].pop(handler.sock)
        self.handlers_timeouts[handler.sock] = expiration
        self.timeouts.setdefault(expiration, {})[handler.sock] = handler

    def remove_timeout(self, handler):
        if handler.sock in self.handlers_timeouts:
            expiration = self.handlers_timeouts.pop(handler.sock)
            self.timeouts.get(expiration, {}).pop(handler.sock, None)

    def handle_event(self, eventmask):
        if eventmask & POLLIN:
            # Seems we need to "flush" the FD's expiration counter to
            # avoid some strange poll-ability bugs
            self.timer.read()
            # Timer expired
            expiration = self.min_expiration

            # We use this instead of iterating on
            # self.timeouts[expiration] because closing one of the
            # handlers may close other handlers, and thus remove some
            # of timeouts we're processing in this call (i.e. when a
            # source times out any of its clients that was marked as
            # timed out will be dropped, and removed from the timeouts
            # list)
            while self.timeouts[expiration]:
                sock, timed_out_handler = self.timeouts[expiration].popitem()
                self.server.logger.error('Timeout for %s: %d seconds without I/O' %
                                         (timed_out_handler, self.server.INACTIVITY_TIMEOUT))
                self.handlers_timeouts.pop(sock)
                timed_out_handler.close()
            del self.timeouts[expiration]
            if self.timeouts:
                # Reset the timer to the earliest one
                self.timer.settime(self.min_expiration, flags = TFD_TIMER_ABSTIME)
        else:
            self.server.logger.error('%s: unexpected eventmask %d (%s)', self, eventmask, event_mask_str(eventmask))
