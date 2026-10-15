import pytest

from wage_check import read_wages


def test_original_encoding_and_leading_zero_id():
    data = ('LEAID\tLEA_NAME\tST_NAME\tLEA_CWIFTEST\tLEA_CWIFTSE\r\n'
            '0100001\tEspañola\tAlabama\t0.868\t0.025\r\n').encode('latin-1')
    frame = read_wages(data)
    assert frame.iloc[0].LEAID == '0100001'
    assert frame.iloc[0].LEA_NAME == 'Española'
    with pytest.raises(ValueError, match='schema'):
        read_wages(data.replace(b'LEAID', b'badid'))
    with pytest.raises(ValueError, match='nonpositive'):
        read_wages(data.replace(b'0.868', b'0'))
