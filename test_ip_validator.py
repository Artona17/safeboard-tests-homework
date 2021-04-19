import ip_validator as val
import pytest
import random


@pytest.fixture
def validate():
    return val.Validate()


def test_empty(validate):
    assert validate.validateIPAddress([]) == 'Provide IPs'


def test_more_than_one_ip_argument(validate):
    ip = '192.168.123.45'
    for i in range(2, 15):
        ips = [ip]*i
        for j in range(i):
            assert validate.validateIPAddress(ips)[j] == [ips[j], 'Valid IPv4']


def test_ipv4_values_positive(validate):
    ip = '.'.join([str(random.randint(2, 253))]*4)
    assert validate.validateIPAddress([ip])[0] == [ip, 'Valid IPv4']


def test_ipv6_values_positive(validate):
    ips = ['2001:0db8:85a3:0:0:8A2E:0370:7334', '5fdd:087b:244d:8b16:84b0:365c:cfe7:fd9d',
           '7296:7272:c150:0fe7:b0d3:6914:f40d:78d6']
    for i in range(len(ips)):
        assert validate.validateIPAddress([ips[i]])[i] == [ips[i], 'Valid IPv6']


@pytest.mark.parametrize("actual,expected", [
    ('::1', ['::1', 'Valid IPv6']),
    ('2000::1234', ['2000::1234', 'Valid IPv6']),
    ('::', ['::', 'Valid IPv6']),
    ('fc00::', ['fc00::', 'Valid IPv6'])])
def test_ipv6_double_colons(actual, expected, validate):
    assert validate.validateIPAddress([actual])[0] == expected


@pytest.mark.parametrize("actual,expected", [
    ('190.b.2.65', ['190.b.2.65', 'Wrong IPv4']),
    ('190.190.190.=', ['190.190.190.=', 'Wrong IPv4']),
    ('190.25.в.6', ['190.25.в.6', 'Wrong IPv4']),
    ('253.900.125.36', ['253.900.125.36', 'Wrong IPv4'])])
def test_ipv4_values_negative(actual, expected, validate):
    assert validate.validateIPAddress([actual])[0] == expected


@pytest.mark.parametrize("actual,expected", [
    ('2:2:2:2:2:2:Q:2', ['2:2:2:2:2:2:Q:2', 'Wrong IPv6']),
    ('2:2:2:2:2:2:q:2', ['2:2:2:2:2:2:q:2', 'Wrong IPv6']),
    ('2:2:2:2:2:=:2:2', ['2:2:2:2:2:=:2:2', 'Wrong IPv6'])
])
def test_ipv6_values_negative(actual, expected, validate):
    assert validate.validateIPAddress([actual])[0] == expected


@pytest.mark.parametrize("actual,expected", [
    ('1921683321', ['1921683321', 'Wrong']),
    ('0'*100, ['0'*100, 'Wrong']),
    (10000000000, [10000000000, 'Wrong']),
    (120.11, [120.11, 'Wrong']),
    (True, [True, 'Wrong'])
])
def test_values_negative(actual, expected, validate):
    assert validate.validateIPAddress([actual])[0] == expected


def test_values_ipv4_positive_in_tuple(validate):
    ips = ('245.21.234.25', '195.28.19.25', '127.239.10.56')
    for i in range(len(ips)):
        assert validate.validateIPAddress([ips[i]])[i] == [ips[i], 'Valid IPv4']


def test_ipv4_equivalence_classes(validate):
    ip_constant_part = str(random.randint(2, 253))
    ip_changing_places_part = str(random.randint(2, 253))
    ip = [ip_constant_part]*3
    for i in range(4):
        ip_checking = ip.copy()
        ip_checking.insert(i, ip_changing_places_part)
        ip_checking = '.'.join(ip_checking)
        assert validate.validateIPAddress([ip_checking])[i][1] == 'Valid IPv4'


@pytest.fixture
def ipv4():
    return '2.2.2.'


def test_ipv4_boundary_values_lower(ipv4, validate):
    for i in range(0, 3):
        ip_checking = ipv4
        ip_checking += str(i - 1)
        if i - 1 == -1:
            assert validate.validateIPAddress([ip_checking])[i] == [ip_checking, 'Wrong IPv4']
        else:
            assert validate.validateIPAddress([ip_checking])[i] == [ip_checking, 'Valid IPv4']


def test_ipv4_boundary_values_upper(ipv4, validate):
    for i in range(0, 3):
        ip_checking = ipv4
        ip_checking += str(i+254)
        if i+254 == 256:
            assert validate.validateIPAddress([ip_checking])[i] == [ip_checking, 'Wrong IPv4']
        else:
            assert validate.validateIPAddress([ip_checking])[i] == [ip_checking, 'Valid IPv4']


def test_ipv6_equivalence_classes(validate):
    ip_constant_part = '5'
    ip_changing_places_part = '3'
    ip = [ip_constant_part] * 7
    for i in range(8):
        ip_checking = ip.copy()
        ip_checking.insert(i, ip_changing_places_part)
        ip_checking = ':'.join(ip_checking)
        assert validate.validateIPAddress([ip_checking])[i][1] == 'Valid IPv6'


@pytest.fixture
def ipv6():
    return '2:2:2:2:2:2:2:'


def test_ipv6_boundary_values_lower(validate, ipv6):
    for i in range(0, 3):
        ip_checking = ipv6
        ip_checking += str(i-1)
        if i-1 == -1:
            assert validate.validateIPAddress([ip_checking])[i] == [ip_checking, 'Wrong IPv6']
        else:
            assert validate.validateIPAddress([ip_checking])[i] == [ip_checking, 'Valid IPv6']


def test_ipv6_boundary_values_upper_lowercase(validate, ipv6):
    for i in range(ord('e'), ord('g')+1):
        ip_checking = ipv6
        ip_checking += chr(i)
        if chr(i) == 'g':
            assert validate.validateIPAddress([ip_checking])[i-ord('e')] == [ip_checking, 'Wrong IPv6']
        else:
            assert validate.validateIPAddress([ip_checking])[i-ord('e')] == [ip_checking, 'Valid IPv6']


def test_ipv6_boundary_values_upper_uppercase(validate, ipv6):
    for i in range(ord('E'), ord('G')+1):
        ip_checking = ipv6
        ip_checking += chr(i)
        if chr(i) == 'G':
            assert validate.validateIPAddress([ip_checking])[i-ord('E')] == [ip_checking, 'Wrong IPv6']
        else:
            assert validate.validateIPAddress([ip_checking])[i-ord('E')] == [ip_checking, 'Valid IPv6']


def test_ipv6_length_of_parts(validate):
    ip_particle = 'a'
    for i in range(0, 6):
        ip_part = ip_particle * i
        ip_list = [ip_part] * 8
        ip = ':'.join(ip_list)
        if i == 5 or i == 0:
            assert validate.validateIPAddress([ip])[i] == [ip, 'Wrong IPv6']
        else:
            assert validate.validateIPAddress([ip])[i] == [ip, 'Valid IPv6']


def test_ipv6_upper_and_lower_letters(validate):
    ip = 'aa:aa:aa:aa:aa:aa:aa:'
    ips = [ip + 'aa', ip + 'aA', ip + 'Aa', ip + 'AA']
    for i in range(len(ips)):
        assert validate.validateIPAddress([ips[i]])[i] == [ips[i], 'Valid IPv6']


@pytest.mark.parametrize("actual,expected", [
    ('127.0.0.1', ['127.0.0.1', 'Valid IPv4']),
    ('0:0:0:0:0:0:0:1', ['0:0:0:0:0:0:0:1', 'Valid IPv6'])
])
def test_localhosts(actual, expected, validate):
    assert validate.validateIPAddress([actual])[0] == expected


def test_other_delimiters(validate):
    ip_part = '2'
    delimiter_ids = list(range(32, 46)) + list([48]) + list(range(59, 65))
    for i in range(len(delimiter_ids)):
        ip = chr(delimiter_ids[i]).join([ip_part] * 4)
        assert validate.validateIPAddress([ip])[i] == [ip, 'Wrong']


def test_ipv4_wrong_points(validate):
    ip = '10.'
    for i in range(1, 10):
        ip_checking = ip*i
        if i == 3:
            assert validate.validateIPAddress([ip_checking])[i-1] == [ip_checking, 'Wrong IPv4']
        else:
            assert validate.validateIPAddress([ip_checking])[i-1] == [ip_checking, 'Wrong']


def test_ipv6_wrong_colons(validate):
    ip = '10:'
    for i in range(1, 10):
        ip_checking = ip*i
        if i == 7:
            assert validate.validateIPAddress([ip_checking])[i-1] == [ip_checking, 'Wrong IPv6']
        else:
            assert validate.validateIPAddress([ip_checking])[i-1] == [ip_checking, 'Wrong']
