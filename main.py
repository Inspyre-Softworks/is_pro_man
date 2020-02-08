import PySimpleGUI as gui

config = False
log = None
conf_dir = None
prog_root = None


def gather_config():
    avail_files = list_ini()
    input_file = None

    if not avail_files:
        log.error(f'No files found in {conf_dir}')
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
    conf_dir = str(prog_root + '/conf/')

    if not Path(conf_dir).exists():
        print(f'Did not find conf directory: {conf_dir}')
        print('Creating...')
        makedirs(conf_dir)
        print('Created!')
        return False

    chdir(conf_dir)
    found = glob('*' + '.ini')
    chdir(prog_root)
    return found


def show_config(config):
    import is_conf_man

    config_window = is_conf_man.show(config)
    print(config_window)


def load_config(file):
    global log
    from configparser import ConfigParser

    parser = ConfigParser()

    parser.read(file)

    log.debug(f'Found config file with the following sections: "{", ".join(parser.sections())}"')

    return parser


def run(file=None):
    global log, prog_root, config
    from lib import app

    name = str('ProjectMan.' + __name__)
    print(name)
    pm = app.ProjectMan()
    log = pm.start_logger()
    log.info(f'Log started for "{name}"')

    if file is None:
        file_list = list_ini()
        if not file_list:
            config =gather_config()
        else:
            if len(file_list) == 0:
                return
            else:
                config = load_config(file_list)
    else:
        config = load_config(file)

    show_config(config)


if __name__ == '__main__':
    run()
