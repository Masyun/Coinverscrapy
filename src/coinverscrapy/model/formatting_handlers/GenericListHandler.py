import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class GenericListHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        is_task_match = re.search('Taak: \n', request)

        if is_task_match:
            match = re.search('\\w+\\s*\\no( )*(\\n)*', request)
            if match:
                list_vals = re.sub(' \no ', "", request).splitlines(True)
                list_vals.pop()  # Pop off the pesky final 'o' char

                mutations = []

                for idx in range(len(list_vals)):
                    if idx > 0:
                        mutations.append('- ' + list_vals[idx])
                    else:
                        mutations.append(list_vals[idx])

                mutated = ''.join(mutations)
                # print('Mutated: \n{}'.format(mutated))
                request = mutated

        return super().handle(request)
