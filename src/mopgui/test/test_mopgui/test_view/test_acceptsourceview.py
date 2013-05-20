__author__ = "David Rusk <drusk@uvic.ca>"

import unittest

import wx

from mock import Mock, call
from hamcrest import assert_that, equal_to, has_length, contains

from test.base_tests import WxWidgetTestCase
from mopgui.view.acceptsourceview import AcceptSourceDialog

# Constants used for test data
TEST_MINOR_PLANET_NUMBER = "mpn01"
TEST_PROVISIONAL_NAME = "provisional-name-1"
TEST_DISCOVERY_AST = "*"
TEST_NOTE1 = "A"
TEST_NOTE2 = "B"
TEST_DATE = "2012 01 01"
TEST_DEC = 31.2123
TEST_RA = 27.213
TEST_MAG = "123.5"
TEST_BAND = "A"
TEST_OBS_CODE = "523"


class AcceptSourceDialogTest(WxWidgetTestCase):
    def setUp(self):
        self.app = wx.App()
        self.rootframe = wx.Frame(None)
        self.controller = Mock()

    def tearDown(self):
        self.rootframe.Destroy()

    def create_undertest(self, note1_choices=None, note2_choices=None):
        return AcceptSourceDialog(self.rootframe, self.controller,
                                  TEST_PROVISIONAL_NAME,
                                  TEST_DATE, TEST_RA, TEST_DEC,
                                  note1_choices=note1_choices,
                                  note2_choices=note2_choices)

    def test_create_components(self):
        undertest = self.create_undertest()

        component_labels = [AcceptSourceDialog.MINOR_PLANET_NUMBER, AcceptSourceDialog.PROVISIONAL_NAME,
                            AcceptSourceDialog.DISCOVERY_ASTERISK, AcceptSourceDialog.NOTE1,
                            AcceptSourceDialog.NOTE2, AcceptSourceDialog.DATE_OF_OBS,
                            AcceptSourceDialog.RA, AcceptSourceDialog.DEC, AcceptSourceDialog.OBS_MAG,
                            AcceptSourceDialog.BAND, AcceptSourceDialog.OBSERVATORY_CODE,
                            AcceptSourceDialog.OK_BTN, AcceptSourceDialog.CANCEL_BTN]

        for label in component_labels:
            self.assert_has_child_with_label(undertest, label)

    def test_required_preset_values(self):
        undertest = self.create_undertest()

        assert_that(undertest.GetTitle(), equal_to(AcceptSourceDialog.TITLE))
        self.assert_has_child_with_label(undertest, TEST_PROVISIONAL_NAME)

        self.assert_has_child_with_label(undertest, str(TEST_RA))
        self.assert_has_child_with_label(undertest, str(TEST_DEC))
        self.assert_has_child_with_label(undertest, TEST_DATE)

    def test_note_comboboxes_populated(self):
        note1_choices = ["n1a", "n1b"]
        note2_choices = ["n2a", "n2b", "n2c"]
        undertest = self.create_undertest(note1_choices, note2_choices)

        note1_combobox = self.get_child_by_name(undertest, AcceptSourceDialog.NOTE1)
        assert_that(note1_combobox.GetValue(), equal_to(""))
        assert_that(not note1_combobox.IsEditable())
        assert_that(note1_combobox.GetCount(), equal_to(len(note1_choices)))

        note2_combobox = self.get_child_by_name(undertest, AcceptSourceDialog.NOTE2)
        assert_that(note2_combobox.GetValue(), equal_to(""))
        assert_that(not note2_combobox.IsEditable())
        assert_that(note2_combobox.GetCount(), equal_to(len(note2_choices)))

    def test_cancel_event(self):
        undertest = self.create_undertest()

        cancel_button = self.get_child_by_name(undertest, AcceptSourceDialog.CANCEL_BTN)
        self.fire_button_click_event(cancel_button)

        assert_that(self.controller.on_do_accept.call_args_list, has_length(0))
        assert_that(self.controller.on_cancel_accept.call_args_list, contains(call()))

    def test_submit_data(self):
        note1_choices = ["C", TEST_NOTE1]
        note2_choices = [TEST_NOTE2, "D", "E"]
        undertest = self.create_undertest(note1_choices, note2_choices)

        def get(name):
            """Convenience method"""
            return self.get_child_by_name(undertest, name)

        # Enter data
        get(AcceptSourceDialog.MINOR_PLANET_NUMBER).SetValue(TEST_MINOR_PLANET_NUMBER)
        get(AcceptSourceDialog.DISCOVERY_ASTERISK).SetValue(wx.CHK_CHECKED)
        get(AcceptSourceDialog.NOTE1).SetStringSelection(TEST_NOTE1)
        get(AcceptSourceDialog.NOTE2).SetStringSelection(TEST_NOTE2)
        get(AcceptSourceDialog.OBS_MAG).SetValue(TEST_MAG)
        get(AcceptSourceDialog.BAND).SetValue(TEST_BAND)
        get(AcceptSourceDialog.OBSERVATORY_CODE).SetValue(TEST_OBS_CODE)

        # Submit data
        ok_button = self.get_child_by_name(undertest, AcceptSourceDialog.OK_BTN)
        self.fire_button_click_event(ok_button)

        # Check data
        assert_that(not self.controller.on_cancel_accept.called)
        self.controller.on_do_accept.assert_called_once_with(
            TEST_MINOR_PLANET_NUMBER, TEST_PROVISIONAL_NAME, TEST_DISCOVERY_AST,
            TEST_NOTE1, TEST_NOTE2, TEST_DATE, str(TEST_RA), str(TEST_DEC), TEST_MAG,
            TEST_BAND, TEST_OBS_CODE)


if __name__ == '__main__':
    unittest.main()
