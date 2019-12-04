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
        print('Failed:\n')
        for fail in self.parser.get_failures():
            print(fail.replace('pdfs\\', ''))

    def finalize(self):
        try:
            print('\n')
            write_json(self.parser.get_data(), self.output)
        except IOError as ioe:
            print("error! -> \n{}".format(ioe))
            print("\n\n")


def write_json(json_objs, output_folder):
    i = 0

    for json_obj in json_objs:
        json_obj = json.loads(json_obj)
        title = json.dumps(json_obj['titel']) \
            .replace('/', '') \
            .strip("\"")
        title = title.encode('utf-8', 'ignore') \
            .decode('unicode_escape')

        file_path = (output_folder + '\\' + title + '.json')
        try:
            with open(file_path, 'w+', encoding="utf-8") as outfile:
                # print('json_obj: \n{}'.format(json_obj))
                # json_str = json.dumps(json_obj, sort_keys=True, indent=4, ensure_ascii=False)
                json.dump(json_obj, outfile, indent=4)
                # outfile.write(json_str)
        except OSError as ose:
            print(ose)
        i += 1
        # time.sleep(0.1)


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
