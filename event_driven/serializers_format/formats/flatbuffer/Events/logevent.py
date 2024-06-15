# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Events

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class logevent(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = logevent()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAslogevent(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # logevent

    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # logevent
    def Name(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # logevent
    def Timestamp(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # logevent
    def Source(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # logevent
    def SerializerFormat(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(
            self._tab.Offset(10))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # logevent
    def Level(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(
            self._tab.Offset(12))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # logevent
    def Message(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(
            self._tab.Offset(14))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None


def Start(builder): builder.StartObject(6)


def logeventStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)


def AddName(builder, name): builder.PrependUOffsetTRelativeSlot(
    0, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)


def logeventAddName(builder, name):
    """This method is deprecated. Please switch to AddName."""
    return AddName(builder, name)


def AddTimestamp(builder, timestamp): builder.PrependUOffsetTRelativeSlot(
    1, flatbuffers.number_types.UOffsetTFlags.py_type(timestamp), 0)


def logeventAddTimestamp(builder, timestamp):
    """This method is deprecated. Please switch to AddTimestamp."""
    return AddTimestamp(builder, timestamp)


def AddSource(builder, source): builder.PrependUOffsetTRelativeSlot(
    2, flatbuffers.number_types.UOffsetTFlags.py_type(source), 0)


def logeventAddSource(builder, source):
    """This method is deprecated. Please switch to AddSource."""
    return AddSource(builder, source)


def AddSerializerFormat(builder, serializerFormat): builder.PrependUOffsetTRelativeSlot(
    3, flatbuffers.number_types.UOffsetTFlags.py_type(serializerFormat), 0)


def logeventAddSerializerFormat(builder, serializerFormat):
    """This method is deprecated. Please switch to AddSerializerFormat."""
    return AddSerializerFormat(builder, serializerFormat)


def AddLevel(builder, level): builder.PrependUOffsetTRelativeSlot(
    4, flatbuffers.number_types.UOffsetTFlags.py_type(level), 0)


def logeventAddLevel(builder, level):
    """This method is deprecated. Please switch to AddLevel."""
    return AddLevel(builder, level)


def AddMessage(builder, message): builder.PrependUOffsetTRelativeSlot(
    5, flatbuffers.number_types.UOffsetTFlags.py_type(message), 0)


def logeventAddMessage(builder, message):
    """This method is deprecated. Please switch to AddMessage."""
    return AddMessage(builder, message)


def End(builder): return builder.EndObject()


def logeventEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)
