import os

from src.coinverscrapy.model.proxy.IModuleProxy import IModuleProxy
from src.coinverscrapy.model.template.IModuleTemplate import IModuleTemplate


class ParserProxy(IModuleProxy, IModuleTemplate):
    def __init__(self, real_parser, output):
        self.parser = real_parser
        self.output = output

    def initialize(self):
        handle_fs(self.output)

    def run(self):
        self.parser.execute()

    def finalize(self):
        '''
        TODO
        try:
            print_progress(0, len(self.output), prefix='Progress:', suffix='Complete', bar_length=50)
            write_json(self.parser.get_data(), self.output)
        except:
            print("\n\n")
            print("Faulty URL supplied! -> quitting execution")
            exit(0)
        '''


def handle_fs(folder_name):
    print("Checking output directory(creating if it doesn't exist)...")
    try:
        os.mkdir(folder_name)
        print('Created directory {}'.format(folder_name))
    except FileExistsError:
        for file in os.listdir(folder_name):
            file_path = os.path.join(folder_name, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


def print_progress(iteration, total, prefix='', suffix='', decimals=0, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    import sys
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def write_json(urls, output_folder):
    #TODO
    pass