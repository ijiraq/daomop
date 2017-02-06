__author__ = 'bannisterm'

import argparse
import os
from ossos import storage, mpc, ssos
from ossos.gui import context, tasks
from ossos import parameters, parsers
from astropy.time import Time
from ossos import util 


if __name__ == '__main__':
    description = 'Given a block ID (e.g. o5d), report which objects in that block have unmeasured lines of astrometry,' \
                  'as found by SSOIS from the present arc of each object in the block.'
    epilog = '''
    For all objects in the database, check if they have images taken by OSSOS on which they are predicted to fall
    but on which their astrometry/photometry have not yet been measured to generate a recorded MPC line.
    Output a list of objects to work on, and a list of images that have failed processing for any reason.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('block',
                        help="The three-digit OSSOS designation for the set of TNOs of interest.",
                        )
    parser.add_argument('-a', '--ast-dir',
                        help="Name of the directory holding the astrometric files (.ast files)",
                        default=parameters.REAL_KBO_AST_DIR,
                        )
    parser.add_argument('-x', '--check-mkpsf',
                        help="Check in mkpsf has run.",
                        action="store_true",
                        default=False,
                        )
    args = parser.parse_args()

    outfile = 'need_to_measure_{}.txt'.format(args.block)

    working_context = context.get_context(args.ast_dir)
    files = working_context.get_listing('ast')
    files = [f for f in files if f.startswith(args.block)]

    with open(outfile, 'w') as ofile:
      ofile.write('Examining {} object files.\n'.format(len(files)))
      for fn in files:
        print(fn)
        ofile.write('{}\n'.format(fn))
        obj = parsers.TNO(mpc.MPCReader(os.path.join(os.path.join(args.ast_dir, fn))))
        discovery_frame = obj.discovery.comment.frame.split('p')[0].strip(' ')
        parser = ssos.TracksParser(skip_previous=True)
        tracks_data = parser.parse(os.path.join(args.ast_dir, fn), print_summary=False)
        if len(tracks_data.observations) > 1:  # it is set to always return the discovery image
            print('{} unmeasured observations!\n'.format(len(tracks_data.observations) - 1))
            ofile.write('{} unmeasured observations!\n'.format(len(tracks_data.observations) - 1))
            for obs in tracks_data.observations:
                if obs.expnum != discovery_frame:  # are these new?
                    ofile.write('{} {}\n'.format(obs.rawname, Time(obs.mjd, format='mjd', scale='utc').mpc))
                    # Any processing-related reason why this image hasn't been measured yet? If so we need to process.
                    # assert storage.get_status('update_header', '', obs.expnum, "p", 36)

                    if args.check_mkpsf and not (storage.get_status('mkpsf', '', obs.expnum, "p", obs.ccdnum) or \
                            storage.get_status('mk_mopheader', '', obs.expnum, "p", obs.ccdnum)):
                        ofile.write('{}\n'.format(obs.expnum))
        ofile.flush()

