"""Encoder for message constructs"""

from construct import Container
from . import common, messages, params

outgoingMessageID = 0

def encodeMessage (name, msgdict={}):
    global outgoingMessageID
    encoder = messages.getEncoderForName(name)
    c = Container(
            Version=1,
            Type=encoder.type,
            Length=10, # XXX
            ID=outgoingMessageID
            )
    c.update(msgdict)
    outgoingMessageID += 1
    return encoder.build(c)
