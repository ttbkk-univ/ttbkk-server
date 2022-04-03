import sys
import traceback
from logging import Handler, raiseExceptions

import env
from src.utils.slack import post_slack_message


class SlackHandler(Handler):
    def emit(self, record):
        if raiseExceptions and sys.stderr:  # see issue 13807
            t, v, tb = sys.exc_info()
            try:
                err_msg = self.get_exception_message(t, v, tb, None, sys.stderr)
                text = f'*{env.ENV}* 에서 에러가 발생했어요!'
                if record.request is not None:
                    text += f'\n`{record.request.method} {record.request.path}`'
                    body = record.request.body.decode("utf-8")
                    if body:
                        text += f'\n*Body*\n```{body}```'
                    text += f'\n*Header*\n```{record.request.headers}```'
                text += '\n*Traceback*\n```%s```' % err_msg
                post_slack_message(env.SLACK_ERROR_CHANNEL, text)
            except OSError:  # pragma: no cover
                pass  # see issue 5971
            finally:
                del t, v, tb

    def get_exception_message(self, etype, value, tb, limit=None, file=None, chain=True):
        """Print exception up to 'limit' stack trace entries from 'tb' to 'file'.

        This differs from print_tb() in the following ways: (1) if
        traceback is not None, it prints a header "Traceback (most recent
        call last):"; (2) it prints the exception type and value after the
        stack trace; (3) if type is SyntaxError and value has the
        appropriate format, it prints the line where the syntax error
        occurred with a caret on the next line indicating the approximate
        position of the error.
        """
        # format_exception has ignored etype for some time, and code such as cgitb
        # passes in bogus values as a result. For compatibility with such code we
        # ignore it here (rather than in the new TracebackException API).
        if file is None:
            file = sys.stderr
        return ''.join([
            message for message in
            traceback.TracebackException(type(value), value, tb, limit=limit).format(chain=chain)])
