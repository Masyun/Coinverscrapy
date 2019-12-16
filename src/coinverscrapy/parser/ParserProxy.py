import json
import os

from src.coinverscrapy.model.template.IModuleTemplate import IModuleTemplate


class ParserProxy(IModuleTemplate):
    def __init__(self, real_parser, output):
        self.parser = real_parser
        self.output = output

    def initialize(self):
        handle_fs(self.output)

    def run(self):
        print("Parsing pdfs to json...")
        self.parser.execute()

    def finalize(self):

        try:
            write_json(self.parser.get_data(), self.output)
        except IOError as ioe:
            print("error! -> \n{}".format(ioe))
            print("\n\n")

        if len(self.parser.get_failures()) > 0:
            print('Failed:\n')
            for idx, fail in enumerate(self.parser.get_failures()):
                print(str(idx + 1) + '. ' + fail.replace('pdfs\\', ''))


def write_json(json_objs, output_folder):
    i = 0
    for json_obj in json_objs:
        json_obj = json.loads(json_obj)
        title = json.dumps(json_obj['titel']).replace('/', '').strip("\"")\
            .encode('utf-8', 'ignore').decode('unicode_escape')

        file_path = os.path.join(output_folder, '{}.json'.format(title))

        try:
            with open(file_path, 'w+', encoding="utf-8") as outfile:
                json_str = json.dumps(json_obj, ensure_ascii=False).encode('utf-8').decode()
                json.dump(json_str, outfile, indent=4)
        except OSError as e:
            print(e)
        except TypeError as te:
            print(te)
        i += 1


def handle_fs(folder_name):
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
