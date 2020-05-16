# Initiate an outbound call to 1-888-222-3333 and say
# 'hello world!' when the caller answers.

from pycall import CallFile, Call, Application

call = Call('SIP/380990154149')
action = Application('Playback', 'hello-world')

c = CallFile(call, action, spool_dir='.')
c.spool()
