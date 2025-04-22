import pytest
from television import Television

def test_initial_state():
    tv = Television()
    assert str(tv) == "Power=False, Channel=0, Volume=0"

def test_power_toggle():
    tv = Television()
    tv.power()
    assert str(tv) == "Power=True, Channel=0, Volume=0"
    tv.power()
    assert str(tv) == "Power=False, Channel=0, Volume=0"

def test_mute_when_on():
    tv = Television()
    tv.power()
    tv.volume_up()
    tv.mute()
    tv.volume_up()
    assert str(tv) == "Power=True, Channel=0, Volume=1"

def test_mute_when_off():
    tv = Television()
    tv.mute()
    assert str(tv) == "Power=False, Channel=0, Volume=0"

def test_channel_up_wraparound():
    tv = Television()
    tv.power()
    tv.channel_up()
    tv.channel_up()
    tv.channel_up()
    tv.channel_up()
    assert str(tv) == "Power=True, Channel=0, Volume=0"

def test_channel_down_wraparound():
    tv = Television()
    tv.power()
    tv.channel_down()
    assert str(tv) == "Power=True, Channel=3, Volume=0"

def test_volume_up_when_muted():
    tv = Television()
    tv.power()
    tv.volume_up()
    tv.mute()
    tv.volume_up()
    assert str(tv) == "Power=True, Channel=0, Volume=2"

def test_volume_up_max():
    tv = Television()
    tv.power()
    tv.volume_up()
    tv.volume_up()
    tv.volume_up()
    assert str(tv) == "Power=True, Channel=0, Volume=2"

def test_volume_down_when_muted():
    tv = Television()
    tv.power()
    tv.volume_up()
    tv.volume_up()
    tv.mute()
    tv.volume_down()
    assert str(tv) == "Power=True, Channel=0, Volume=1"

def test_volume_down_min():
    tv = Television()
    tv.power()
    tv.volume_down()  # should stay at min
    assert str(tv) == "Power=True, Channel=0, Volume=0"
