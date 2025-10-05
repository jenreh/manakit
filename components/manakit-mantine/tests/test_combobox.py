from manakit_mantine.base import MantineComponentBase
from manakit_mantine.combobox import Combobox


def test_combobox_inheritance_and_tag():
    assert issubclass(Combobox, MantineComponentBase)
    assert Combobox.tag == "Combobox"
