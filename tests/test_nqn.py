import pytest
import itertools
from infi.dtypes.nqn import NQN, iSCSIName, InvalidNQN, make_iscsi_name  # pylint: disable=no-name-in-module


def test_basic():
    a = NQN('nqn.2001-04.com.example:storage:diskarrays-sn-a8675309')
    assert hash(a) == hash('nqn.2001-04.com.example:storage:diskarrays-sn-a8675309')
    assert a == a
    assert a == 'nqn.2001-04.com.example:storage:diskarrays-sn-a8675309'
    assert a == 'NQN.2001-04.com.EXAMPLE:storage:diskarrays-sn-a8675309'
    assert a != 'lol'
    assert a.get_date() == '2001-04'
    assert a.get_naming_authority() == 'com.example'
    assert a.get_extra() == 'storage:diskarrays-sn-a8675309'
    assert a.get_extra_fields() == ('storage', 'diskarrays-sn-a8675309')


def test_rfc_examples():
    a = NQN('nqn.2001-04.com.example')
    assert a.get_date() == '2001-04'
    assert a.get_naming_authority() == 'com.example'
    assert a.get_extra() == ''
    assert a.get_extra_fields() == ()


@pytest.mark.parametrize('copy_types', itertools.product([NQN, iSCSIName], repeat=2))
@pytest.mark.parametrize('is_upper', [False, True])
def test_copy_ctor(copy_types, is_upper):
    source_type, target_type = copy_types
    identifier = 'nqn.2001-04.com.example'
    obj = source_type(identifier.upper() if is_upper else identifier)
    assert target_type(obj) == obj


def test_invalid_nqn():
    iscsi_identifier = '1'
    with pytest.raises(InvalidNQN):
        NQN(iscsi_identifier)
    iSCSIName(iscsi_identifier)
    assert isinstance(make_iscsi_name(iscsi_identifier), iSCSIName)


def test_equality():
    iscsi_identifier = 'nqn.2001-04.com.example'
    nqn = NQN(iscsi_identifier)
    iscsi_name = iSCSIName(iscsi_identifier)
    assert nqn == iscsi_name
    assert nqn == iscsi_identifier
    assert nqn == iscsi_identifier.upper()
    assert iscsi_name == nqn
    assert iscsi_name == iscsi_identifier
    assert iscsi_name == iscsi_identifier.upper()
