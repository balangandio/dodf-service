import nltk
import pathlib
import mimetypes


def setup_nltk_data_packages():
    nltk_data_reqs_file = pathlib.Path(__file__).parent.parent.joinpath('requirements-nltk.txt')
    packages = []

    if nltk_data_reqs_file.exists():
        with nltk_data_reqs_file.open() as f:
            content = f.readlines()

        packages = [line.strip() for line in content]
        packages = list(filter(lambda line : not line.startswith('#') and len(line) > 0, packages))
 
    for package in packages:
        if not nltk.downloader.Downloader().is_installed(package):
            nltk.download(package, None, True)


def setup_environment_mimetypes():
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')


setup_nltk_data_packages()
setup_environment_mimetypes()