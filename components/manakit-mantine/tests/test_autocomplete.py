from manakit_mantine.autocomplete import Autocomplete
from manakit_mantine.base import MantineInputComponentBase


def test_autocomplete_inheritance_and_tag():
    assert issubclass(Autocomplete, MantineInputComponentBase)
    assert Autocomplete.tag == "Autocomplete"
