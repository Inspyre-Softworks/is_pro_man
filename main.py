config = False
log = None
conf_dir = None
prog_root = None

def gather_config():
    import PySimpleGUI as gui
    input_file = None
    ask = gui.PopupYesNo('Unable to find existing config file.\n\nCould be a new install.\n\n'
                         'Do you have another config file you\'d like to import?',
                         keep_on_top=True
                         )

    if ask.lower() == 'yes':
        input_file = gui.PopupGetFile('Please select a config file.',
                                      keep_on_top=True,
                                      title='Please pick a file.')

    elif ask.lower() == 'no' or ask is None:
        log.warning('User did not provide config file. Loading default config.')
        input_file = str(prog_root + '/docs/example_conf/example_config.ini')

    config = load_config(input_file)
    conf_sections = config.sections()
    f_conf_sections = ", ".join(conf_sections)
    log.debug(f'Received a config with the following sections "{f_conf_sections}"')
    return config


def list_ini():
    from glob import glob
    from os import getcwd, chdir, makedirs
    from pathlib import Path
    global conf_dir, prog_root

    prog_root = getcwd()
    log.debug(f'Determined the program root directory as: "{prog_root}"')
    conf_dir = str(prog_root + '/conf')
    log.debug(f'Determined the conf directory should be: "{conf_dir}"')

    if not Path(conf_dir).exists():
        print(f'Did not find conf directory: {conf_dir}')
        print('Creating...')
        makedirs(conf_dir)
        print('Created!')
        return None

    chdir(conf_dir)
    found = glob('*.ini')
    chdir(prog_root)
    print(found)
    print(len(found))
    return found


def show_config(alt_config=None, dest=None):
    import is_conf_man
    global config

    if alt_config is None:
        my_conf = config
    else:
        my_conf = alt_config

    config_window = is_conf_man.show(my_conf, dest=dest)



def load_config(file):
    global log, config, prog_root
    from configparser import ConfigParser

    parser = ConfigParser()
    print(file)

    if isinstance(file, list):
        new_list = []
        print('got a list')
        for candidate in file:
            candidate = str(prog_root + '/conf/' + candidate)
            new_list.append(candidate)
            print(candidate)
            print(new_list)
        file = new_list

    parser.read(file)

    log.debug(f'Found config file with the following sections: "{", ".join(parser.sections())}"')

    config = parser

    return parser


def run(file=None):
    global log, prog_root, config
    from lib import app
    import os

    name = str('ProjectMan.' + __name__)
    print(name)
    pm = app.ProjectMan()
    log = pm.start_logger()
    log.info(f'Log started for "{name}"')

    if file is None:
        file_list = list_ini()
        print(f'File list is {file_list}')
        if len(file_list) == 0:
            config = gather_config()
        else:
            print(f'File list is greater than 0')
            conf_dir = os.getcwd() + '/conf/'
            config = load_config(file_list)
    else:
        config = load_config(file)

    show_config(config, dest=conf_dir)


if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser(description='Short sample app', add_help=True)

    arg_parser.add_argument('-v', '--verbose',
                            action="store_true",
                            default=False,
                            help='Logs to STDOUT verbosely.')

    arg_parser.add_argument('-c', '--config',
                            type=open,
                            default=None,
                            help='Import a config file to edit')

    args = arg_parser.parse_args()
    if args.config:
        run(file=args.config.name)
    else:
        run()
