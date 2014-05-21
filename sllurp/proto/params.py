"""Implementations of LLRP parameters from Section 17.2 of the LLRP 1.1 protocol
specification."""

from construct import *
from .common import TLVParameterHeader, TVParameterHeader, IntRange

# 17.2.2.1
UTCTimestamp = Struct("UTCTimestamp",
        TLVParameterHeader(128),
        UBInt64("Microseconds"))

# 17.2.2.2
Uptime = Struct("Uptime",
        TLVParameterHeader(129),
        UBInt64("Microseconds"))

# 17.2.3.1
GeneralDeviceCapabilities = Struct("GeneralDeviceCapabilities",
        TLVParameterHeader(137),
        UBInt16("MaxNumberOfAntennaSupported"),
        EmbeddedBitStruct(
            Flag("CanSetAntennaProperties"),
            Flag("HasUTCClockCapability"),
            Padding(14)),
        UBInt32("DeviceManufacturerName"),
        UBInt32("ModelName"),
        UBInt16("FirmwareVersionByteCount"),
        String("ReaderFirmwareVersion",
            lambda ctx: ctx["FirmwareVersionByteCount"]),

        # 17.2.3.1.2
        GreedyRange(Struct("ReceiveSensitivityTableEntry",
                TLVParameterHeader(139),
                UBInt16("Index"),
                IntRange(UBInt16("ReceiveSensitivityValue"), 0, 128))),

        # 17.2.3.1.3
        OptionalGreedyRange(Struct("PerAntennaReceiveSensitivityRange",
                TLVParameterHeader(149),
                UBInt16("AntennaID"),
                UBInt16("ReceiveSensitivityIndexMin"),
                UBInt16("ReceiveSensitivityIndexMax"))),

        # 17.2.3.1.5
        Struct("GPIOCapabilities",
                TLVParameterHeader(141),
                UBInt16("NumGPIs"),
                UBInt16("NumGPOs")),

        # 17.2.3.1.4
        GreedyRange(Struct("PerAntennaAirProtocol",
                    TLVParameterHeader(140),
                    UBInt16("AntennaID"),
                    UBInt16("NumProtocols"),
                    Array(lambda ctx: ctx.NumProtocols, UBInt8("ProtocolID")))),

        # 17.2.3.1.1
        Optional(Struct("MaximumReceiveSensitivity",
                    TLVParameterHeader(363),
                    UBInt16("MaximumSensitivity")))
        )

# 17.2.3.2
LLRPCapabilities = Struct("LLRPCapabilities",
        TLVParameterHeader(142),
        EmbeddedBitStruct(
            Flag("CanDoRFSurvey"),
            Flag("CanReportBufferFillWarning"),
            Flag("SupportsClientRequestOpSpec"),
            Flag("CanDoTagInventoryStateAwareSingulation"),
            Flag("SupportsEventAndReportHolding"),
            Padding(3)),
        IntRange(UBInt8("MaxPriorityLevelSupported"), 0, 7),
        UBInt16("ClientRequestOpSpecTimeout"),
        UBInt32("MaxNumROSpecs"),
        UBInt32("MaxNumSpecsPerROSpec"),
        UBInt32("MaxNumInventoryParameterSpecsPerAISpec"),
        UBInt32("MaxNumAccessSpecs"),
        UBInt32("MaxNumOpSpecsPerAccessSpec"))

# 17.2.3.4.1
UHFBandCapabilities = Struct("UHFBandCapabilities",
        TLVParameterHeader(144),

        # 17.2.3.4.1.1
        GreedyRange(Struct("TransmitPowerLevelTableEntry",
                TLVParameterHeader(145),
                IntRange(UBInt16("Index"), 0, 255),
                UBInt16("TransmitPowerValue"))),

        # 17.2.3.4.1.2
        Struct("FrequencyInformation",
            TLVParameterHeader(146),
            EmbeddedBitStruct(
                Flag("Hopping"),
                Padding(7)),

            # 17.2.3.4.1.2.1
            OptionalGreedyRange(Struct("FrequencyHopTable",
                    TLVParameterHeader(147),
                    UBInt8("HopTableID"),
                    Padding(1),
                    UBInt16("NumHops"),
                    Array(lambda ctx: ctx.NumHops, UBInt32("Frequency")))),

            # 17.2.3.4.1.2.2
            Optional(Struct("FixedFrequencyTable",
                    TLVParameterHeader(148),
                    UBInt16("NumFrequencies"),
                    Array(lambda ctx: ctx.NumFrequencies,
                        UBInt32("Frequency"))))),

        # 17.3.1.1.2
        GreedyRange(Struct("UHFC1G2RFModeTable",
                    TLVParameterHeader(328),

                    # 17.3.1.1.2.1
                    GreedyRange(Struct("UHFC1G2RFModeTableEntry",
                            TLVParameterHeader(329),
                            UBInt32("ModeIdentifier"),
                            EmbeddedBitStruct(
                                Flag("DivideRatio"),
                                Alias("DR", "DivideRatio"),
                                Flag("EPCHAGT&CConformance"),
                                Padding(6)),

                            Enum(UBInt8("Modulation"),
                                FM0 = 0,
                                Miller2 = 1,
                                Miller4 = 2,
                                Miller8 = 3),
                            Alias("Mod", "Modulation"),

                            Enum(UBInt8("ForwardLinkModulation"),
                                PR_ASK = 0,
                                SSB_ASK = 1,
                                DSB_ASK = 2),
                            Alias("FLM", "ForwardLinkModulation"),

                            Enum(UBInt8("SpectralMaskIndicator"),
                                    Unknown = 0,
                                    SingleInterrogator = 1,
                                    MultiInterrogator = 2,
                                    DenseInterrogator = 3),
                            Alias("M", "SpectralMaskIndicator"),

                            IntRange(UBInt32("BackscatterDataRate"),
                                40e3, 640e3),
                            Alias("BDR", "BackscatterDataRate"),

                            IntRange(UBInt32("PIE"), 1500, 2000),
                            IntRange(UBInt32("MinTari"), 6250, 25000),
                            IntRange(UBInt32("MaxTari"), 6250, 25000),
                            IntRange(UBInt32("StepTari"), 0, 18750)
                            )))),

        # 17.2.3.4.1.3
        Optional(Struct("RFSurveyFrequencyCapabilities",
                    TLVParameterHeader(365),
                    UBInt32("MinimumFrequency"),
                    UBInt32("MaximumFrequency"))))


# 17.2.3.4
RegulatoryCapabilities = Struct("RegulatoryCapabilities",
        TLVParameterHeader(143),
        UBInt16("CountryCode"),
        UBInt16("CommunicationsStandard"),
        Optional(UHFBandCapabilities),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.8.1
LLRPStatus = Struct("LLRPStatus",
        TLVParameterHeader(287),
        UBInt16("StatusCode"),
        UBInt16("ErrorDescriptionByteCount"),
        If(lambda ctx: ctx.ErrorDescriptionByteCount,
            String("ErrorDescription",
                lambda ctx: ctx.ErrorDescriptionByteCount)),
        Optional(Struct("FieldError",
            TLVParameterHeader(288),
            UBInt16("FieldNum"),
            UBInt16("ErrorCode"), # XXX Enum?
            )),
        Optional(Struct("ParameterError",
            TLVParameterHeader(289),
            UBInt16("ParameterType"),
            UBInt16("ErrorCode"), # XXX Enum?
            ))
        )

# 17.3
C1G2LLRPCapabilities = Struct("C1G2LLRPCapabilities",
        TLVParameterHeader(327),
        EmbeddedBitStruct(
            Flag("CanSupportBlockErase"),
            Flag("CanSupportBlockWrite"),
            Flag("CanSupportBlockPermalock"),
            Flag("CanSupportTagRecommissioning"),
            Flag("CanSupportUMIMethod2"),
            Flag("CanSupportXPC"),
            Padding(2)),
        UBInt16("MaxNumSelectFiltersPerQuery"))
