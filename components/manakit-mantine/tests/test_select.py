from manakit_mantine.base import MantineInputComponentBase
from manakit_mantine.select import Select


def test_select_inheritance_and_tag():
    assert issubclass(Select, MantineInputComponentBase)
    assert Select.tag == "Select"
