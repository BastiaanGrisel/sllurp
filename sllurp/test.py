import unittest
import random
import sllurp
import sllurp.llrp
import sllurp.llrp_proto
import sllurp.llrp_errors
import binascii
import logging

from sllurp.proto import messages, params, common, decode, encode
from construct import Struct, Embed

logLevel = logging.WARNING
logging.basicConfig(level=logLevel,
        format='%(asctime)s %(name)s: %(levelname)s: %(message)s')
logger = logging.getLogger('sllurp')
logger.setLevel(logLevel)

def randhex (numdigits):
    """Return a string with numdigits hexadecimal digits."""
    assert type(numdigits) is int
    return '{{:0{}x}}'.format(numdigits).format(random.randrange(16**numdigits))

def hex_to_bytes (hexdata):
    binrep = binascii.unhexlify(hexdata)
    assert len(binrep) == (len(hexdata) / 2)
    return binrep

def bytes_to_hex (bindata):
    ascrep = binascii.hexlify(bindata)
    assert len(ascrep) == (len(bindata) * 2)
    return ascrep

class mock_stream (object):
    _bytes = None
    def __init__ (self, mybytes):
        self._bytes = mybytes
    def recv (self, length):
        if length > len(self._bytes):
            length = len(self._bytes)
        data = self._bytes[:length]
        self._bytes = self._bytes[length:]
        return data
    def waiting (self):
        return len(self._bytes)

class mock_conn (object):
    stream = None
    def __init__ (self, mybytes):
        self.stream = mock_stream(mybytes)
    def write (self, mybytes):
        pass

class TestROSpec (unittest.TestCase):
    def setUp (self):
        pass
    def test_start (self):
        rospec = sllurp.llrp.LLRPROSpec(1)
        rospec_str = repr(rospec)
        self.assertNotEqual(rospec_str, '')
    def tearDown (self):
        pass

class TestReaderEventNotification (unittest.TestCase):
    def test_decode (self):
        data = binascii.unhexlify('043f000000200ab288c900f600160080000c0004f8' \
                '535baadaff010000060000')
        client = sllurp.llrp.LLRPClient(self, start_inventory=False)
        client.transport = mock_conn('')
        client.dataReceived(data)

class TestDecodeROAccessReport (unittest.TestCase):
    _r = """
    043d0000002c4095892f00f000228d3005fb63ac1f3841ec88046781000186ce820004ec2ea8
    354c09880001043d0000002c4095893000f000228d300833b2ddd906c00000000081000186c6
    820004ec2ea8355af2880001043d0000002c4095893100f000228d3005fb63ac1f3841ec8804
    6781000186cf820004ec2ea8359791880001043d0000002c4095893200f000228d300833b2dd
    d906c00000000081000186c6820004ec2ea835a71c880001043d0000002c4095893300f00022
    8d3005fb63ac1f3841ec88046781000186ce820004ec2ea835e0ff880001043d0000002c4095
    893400f000228d300833b2ddd906c00000000081000186c6820004ec2ea835f3e0880001043d
    0000002c4095893500f000228d3005fb63ac1f3841ec88046781000186ce820004ec2ea83630
    49880001043d0000002c4095893600f000228d300833b2ddd906c00000000081000186c68200
    04ec2ea836400f880001043d0000002c4095893700f000228d3005fb63ac1f3841ec88046781
    000186ce820004ec2ea83679c8880001043d0000002c4095893800f000228d300833b2ddd906
    c00000000081000186c6820004ec2ea8368c76880001043d0000002c4095893900f000228d30
    0833b2ddd906c00000000081000186c6820004ec2ea836c617880001043d0000002c4095893a
    00f000228d3005fb63ac1f3841ec88046781000186ce820004ec2ea836d516880001043d0000
    002c4095893b00f000228d3005fb63ac1f3841ec88046781000186ce820004ec2ea8370ebf88
    0001043d0000002c4095893c00f000228d300833b2ddd906c00000000081000186c6820004ec
    2ea8372189880001043d0000002c4095893d00f000228d3005fb63ac1f3841ec880467810001
    86cf820004ec2ea8375b09880001043d0000002c4095893e00f000228d300833b2ddd906c000
    00000081000186c6820004ec2ea8376a40880001043d0000002c4095893f00f000228d3005fb
    63ac1f3841ec88046781000186cf820004ec2ea837a430880001043d0000002c4095894000f0
    00228d300833b2ddd906c00000000081000186c6820004ec2ea837b699880001043d00000037
    4095894100f0002d00f1001800901fb41f712ac9c37ab79d618173188324001a81000186ef82
    0004ec2ea8381f57880001043d0000002c4095894200f000228d3005fb63ac1f3841ec880467
    81000186cf820004ec2ea8383238880001043d0000002c4095894300f000228d300833b2ddd9
    06c00000000081000186c4820004ec2ea8384211880001043d0000002c4095894400f000228d
    300833b2ddd906c00000000081000186c4820004ec2ea8387c55880001043d0000002c409589
    4500f000228d3005fb63ac1f3841ec88046781000186cf820004ec2ea83892cf880001043d00
    00002c4095894600f000228d300833b2ddd906c00000000081000186c3820004ec2ea838cc76
    880001043d0000002c4095894700f000228d3005fb63ac1f3841ec88046781000186cf820004
    ec2ea838dbb3880001043d0000002c4095894800f000228d3005fb63ac1f3841ec8804678100
    0186cf820004ec2ea8395e67880001043d0000002c4095894900f000228d300833b2ddd906c0
    0000000081000186c3820004ec2ea8396d13880001043d0000002c4095894a00f000228d3005
    fb63ac1f3841ec88046781000186cf820004ec2ea83a3119880001043d0000002c4095894b00
    f000228d300833b2ddd906c00000000081000186c3820004ec2ea83a4389880001043d000000
    2c4095894c00f000228d300833b2ddd906c00000000081000186c3820004ec2ea83a7d2b8800
    01043d0000002c4095894d00f000228d3005fb63ac1f3841ec88046781000186cf820004ec2e
    a83a8c28880001043d0000002c4095894e00f000228d300833b2ddd906c00000000081000186
    c3820004ec2ea83ac551880001043d0000002c4095894f00f000228d3005fb63ac1f3841ec88
    046781000186cf820004ec2ea83ad450880001043d0000002c4095895000f000228d300833b2
    ddd906c00000000081000186c7820004ec2ea83b26ad880001043d0000002c4095895100f000
    228d3005fb63ac1f3841ec88046781000186cf820004ec2ea83b35eb880001043d0000002c40
    95895200f000228d3005fb63ac1f3841ec88046781000186cf820004ec2ea83b701d88000104
    3d0000002c4095895300f000228d300833b2ddd906c00000000081000186c7820004ec2ea83b
    7f2c880001043d0000002c4095895400f000228d3005fb63ac1f3841ec88046781000186cf82
    0004ec2ea83bb8d8880001043d0000002c4095895500f000228d300833b2ddd906c000000000
    81000186c7820004ec2ea83bcbc5880001043d0000002c4095895600f000228d300833b2ddd9
    06c00000000081000186c7820004ec2ea83c0566880001043d0000002c4095895700f000228d
    3005fb63ac1f3841ec88046781000186cf820004ec2ea83c1479880001043d0000002c409589
    5800f000228d3005fb63ac1f3841ec88046781000186cf820004ec2ea83c4e47880001043d00
    00002c4095895900f000228d300833b2ddd906c00000000081000186c7820004ec2ea83c5d92
    880001043d0000002c4095895a00f000228d3005fb63ac1f3841ec88046781000186cf820004
    ec2ea83c9699880001043d0000002c4095895b00f000228d300833b2ddd906c0000000008100
    0186c7820004ec2ea83ca950880001"""
    _binr = None
    _client = None
    _tags_seen = 0
    def tagcb (self, llrpmsg):
        self._tags_seen += 1
    def setUp (self):
        self._r = self._r.rstrip().lstrip().replace('\n', '').replace(' ', '')
        self._binr = hex_to_bytes(self._r)
        self.assertEqual(len(self._r), 3982)
        self.assertEqual(len(self._binr), 1991)
        self._mock_conn = mock_conn(self._binr)
        logger.debug('{} bytes waiting'.format(self._mock_conn.stream.waiting()))
        self._client = sllurp.llrp.LLRPClient(self, start_inventory=False)
        self._client.transport = mock_conn('')
        self._client.addMessageCallback('RO_ACCESS_REPORT', self.tagcb)
    def test_start(self):
        """Parse the above pile of bytes into a series of LLRP messages."""
        self._client.state = sllurp.llrp.LLRPClient.STATE_INVENTORYING
        self._client.dataReceived(self._binr)
        self.assertEqual(self._tags_seen, 45)
    def tearDown (self):
        pass

class TestEncodings (unittest.TestCase):
    tagReportContentSelector = {
        'EnableROSpecID': False,
        'EnableSpecIndex': False,
        'EnableInventoryParameterSpecID': False,
        'EnableAntennaID': True,
        'EnableChannelIndex': False,
        'EnablePeakRRSI': True,
        'EnableFirstSeenTimestamp': True,
        'EnableLastSeenTimestamp': True,
        'EnableTagSeenCount': True,
        'EnableAccessSpecID': False}
    def test_roreportspec (self):
        par = {'ROReportTrigger': 'Upon_N_Tags_Or_End_Of_ROSpec',
            'N': 1}
        par['TagReportContentSelector'] = self.tagReportContentSelector
        data = sllurp.llrp_proto.encode_ROReportSpec(par)

    def test_tagreportcontentselector (self):
        par = self.tagReportContentSelector
        data = sllurp.llrp_proto.encode_TagReportContentSelector(par)
        self.assertEqual(len(data), 48 / 8)
        ty = int(binascii.hexlify(data[0:2]), 16) & (2**10 - 1)
        self.assertEqual(ty, 238)
        length = int(binascii.hexlify(data[2:4]), 16)
        self.assertEqual(length, len(data))
        flags = int(binascii.hexlify(data[4:]), 16) >> 6
        self.assertEqual(flags, 0b0001011110)

class TestDecodeGetReaderCapabilitiesResponse (unittest.TestCase):
    getCapsResponse = \
    '040b000005d700000000011f00080000000000890185000240000000651a001e88690009' \
    '342e382e332e323430008b000800010000008b00080002000a008b00080003000b008b00' \
    '080004000c008b00080005000d008b00080006000e008b00080007000f008b0008000800' \
    '10008b000800090011008b0008000a0012008b0008000b0013008b0008000c0014008b00' \
    '08000d0015008b0008000e0016008b0008000f0017008b000800100018008b0008001100' \
    '19008b00080012001a008b00080013001b008b00080014001c008b00080015001d008b00' \
    '080016001e008b00080017001f008b000800180020008b000800190021008b0008001a00' \
    '22008b0008001b0023008b0008001c0024008b0008001d0025008b0008001e0026008b00' \
    '08001f0027008b000800200028008b000800210029008b00080022002a008b0008002300' \
    '2b008b00080024002c008b00080025002d008b00080026002e008b00080027002f008b00' \
    '0800280030008b000800290031008b0008002a0032008d000800040004008c0009000100' \
    '0101008c00090002000101008e001c48010000000000010000001000000001000005e400' \
    '000010008f041d034800010090041500910008000103e800910008000204010091000800' \
    '03041a0091000800040433009100080005044c0091000800060465009100080007047e00' \
    '9100080008049700910008000904b000910008000a04c900910008000b04e20091000800' \
    '0c04fb00910008000d051400910008000e052d00910008000f0546009100080010055f00' \
    '91000800110578009100080012059100910008001305aa00910008001405c30091000800' \
    '1505dc00910008001605f5009100080017060e0091000800180627009100080019064000' \
    '910008001a065900910008001b067200910008001c068b00910008001d06a40091000800' \
    '1e06bd00910008001f06d600910008002006ef0091000800210708009100080022072100' \
    '9100080023073a0091000800240753009100080025076c00910008002607850091000800' \
    '27079e00910008002807b700910008002907d000910008002a07e900910008002b080200' \
    '910008002c081b00910008002d083400910008002e084d00910008002f08660091000800' \
    '30087f009100080031089800910008003208b100910008003308ca00910008003408e300' \
    '910008003508fc0091000800360915009100080037092e00910008003809470091000800' \
    '39096000910008003a097900910008003b099200910008003c09ab00910008003d09c400' \
    '910008003e09dd00910008003f09f60091000800400a0f0091000800410a280091000800' \
    '420a410091000800430a5a0091000800440a730091000800450a8c0091000800460aa500' \
    '91000800470abe0091000800480ad70091000800490af000910008004a0b090091000800' \
    '4b0b2200910008004c0b3b00910008004d0b5400910008004e0b6d00910008004f0b8600' \
    '91000800500b9f0091000800510bb80091000800520bd10091000800530bea0091000800' \
    '540c030091000800550c1c0091000800560c350091000800570c4e0091000800580c6700' \
    '91000800590c8000910008005a0c9900910008005b0cb2009200d580009300d001000032' \
    '000e2036000e1c4e000de3aa000dca46000ddbda000e06d2000de986000dddce000e04de' \
    '000dc852000ded6e000e2612000dce2e000e00f6000dfb1a000ddfc2000e0aba000e1672' \
    '000e0cae000e1a5a000de59e000de792000e0ea2000dd5fe000dcc3a000e1e42000dc65e' \
    '000dd40a000dfd0e000dff02000df156000e08c6000dd9e6000df34a000def62000e241e' \
    '000dd216000df732000e147e000e02ea000e222a000e128a000dd7f2000df53e000dd022' \
    '000e1866000e1096000deb7a000de1b6000df92601480064014900200000000280020003' \
    '00042e50000007d000004e2000004e200000000001490020000000038003000300029a68' \
    '000007d000004e2000004e200000000001490020000003e80000000000009c40000005dc' \
    '0000186a0000186a0000000001470007400002'.decode('hex')

    def test_parse_message_header (self):
        s = Struct("a",
                Embed(common.MessageHeader(11))).parse(self.getCapsResponse[:10])
        self.assertTrue(s)

    def test_parse_llrp_status (self):
        s = Struct("b", params.LLRPStatus).parse(self.getCapsResponse[10:18])
        self.assertTrue(s)

    def test_parse_capabilities_response (self):
        "Parse and spot-test GET_READER_CAPABILITIES_RESPONSE"
        msg, msgname = decode.decodeMessage(self.getCapsResponse)
        self.assertEqual(msgname, 'GET_READER_CAPABILITIES_RESPONSE')
        self.assertEqual(msg.Type, 11)
        uhf = msg.RegulatoryCapabilities.UHFBandCapabilities
        self.assertIn(908750,
                uhf.FrequencyInformation.FrequencyHopTable[0].Frequency)
        self.assertEqual(msg.C1G2LLRPCapabilities.CanSupportBlockWrite, True)

class TestEncoding (unittest.TestCase):
    def test_encoder (self):
        msg = encode.encodeMessage('GET_SUPPORTED_VERSION')
        self.assertEqual(msg.encode('hex'), '042e0000000a00000000')

class TestMessageTypes (unittest.TestCase):
    def isMsg (self, fn):
        return isinstance(getattr(messages, fn), messages.LLRPMessageStruct)
    def allMessages (self):
        return [getattr(messages, m) for m in filter(self.isMsg, dir(messages))]
    def test_all_have_types (self):
        for m in self.allMessages():
            self.assertIsNotNone(m.type)
    def test_all_types_unique (self):
        types = [m.type for m in self.allMessages()]
        self.assertEqual(len(set(types)), len(types))

if __name__ == '__main__':
    unittest.main()
