__author__ = "David Rusk <drusk@uvic.ca>"

import unittest

from hamcrest import assert_that, close_to, has_length

from test.base_tests import FileReadingTestCase
from pymop.tools import daophot

DELTA = 0.0001


class DaophotTest(FileReadingTestCase):
    def test_phot(self):
        """
        Test data to compare with generated by running make testphot
        which runs the equivalent Perl script with the same data.
        """
        fits_filename = self.get_abs_path("data/1616681p22.fits")
        x_in = 560.06
        y_in = 406.51
        ap = 4
        insky = 11
        outsky = 15
        maxcount = 30000.0
        exptime = 1.0

        swidth = outsky - insky
        apcor = 0.0

        hdu = daophot.phot(fits_filename, x_in, y_in, aperture=ap, sky=insky,
                           swidth=swidth, apcor=apcor, maxcount=maxcount,
                           exptime=exptime)

        def get_first(param):
            value_list = hdu["data"][param]
            assert_that(value_list, has_length(1))
            return value_list[0]

        xcen = get_first("X")
        ycen = get_first("Y")
        mag = get_first("MAG")
        magerr = get_first("MERR")

        assert_that(xcen, close_to(560.000, DELTA))
        assert_that(ycen, close_to(406.600, DELTA))
        assert_that(mag, close_to(24.769, DELTA))
        # NOTE: minor difference in magnitude error: 0.290 vs 0.291
        assert_that(magerr, close_to(0.290, 0.0011))

    def test_phot_mag(self):
        fits_filename = self.get_abs_path("data/1616681p22.fits")
        x_in = 560.06
        y_in = 406.51
        ap = 4
        insky = 11
        outsky = 15
        maxcount = 30000.0
        exptime = 1.0

        swidth = outsky - insky
        apcor = 0.0

        mag = daophot.phot_mag(fits_filename, x_in, y_in, aperture=ap, sky=insky,
                               swidth=swidth, apcor=apcor, maxcount=maxcount,
                               exptime=exptime)

        assert_that(mag, close_to(24.769, DELTA))


if __name__ == '__main__':
    unittest.main()