from os import path


class CodeCreator:
    def __init__(self):
        self.__base_path = path.dirname(path.dirname(__file__))
        self.__base_dir = "RegionXML"
        self.__old_parent_list = []
        self.__new_parent_list = []

        self.escape_prefix = ''
        self.input_file_name = ''
        self.output_file_name = ''
        self.output_file_code_name = ''
        self.new_list_prefix = ''

    def generate_dictionary(self):
        input_file_path = path.join(self.__base_path, self.__base_dir, self.input_file_name)
        output_file_path = path.join(self.__base_path, self.__base_dir, self.output_file_name)

        if path.exists(input_file_path):
            output_line = '<dictionary>'
            with open(input_file_path, 'r') as input_data:

                for input_line in input_data.readlines():
                    trimmed_input_line = input_line.strip('\n\t\r')
                    output_line_words = trimmed_input_line.split(';')
                    print(output_line_words)

                    item_group = output_line_words[0].strip('\n\t\r').replace(' ', '')
                    item_id = output_line_words[1].strip('\n\t\r').replace(' ', '_')
                    item_name = output_line_words[2].strip('\n\t\r').replace('  ', ' ')

                    output_line += "\n" + "<item id=\"" + item_id + "\"" \
                                   + " name=\"" + item_name + "\"" \
                                   + " group=\"" + item_group + "\"/>"
                output_line += "\n</dictionary>\n"

            if output_line:
                output_data = open(output_file_path, 'w')
                output_data.write(output_line)
                output_data.close()

    def generate_list(self):
        self.__old_parent_list.clear()
        self.__new_parent_list.clear()

        input_file_path = path.join(self.__base_path, self.__base_dir, self.input_file_name)
        output_file_path = path.join(self.__base_path, self.__base_dir, self.output_file_name)

        if path.exists(input_file_path):
            output_line = ''
            with open(input_file_path, 'r') as input_data:
                base_parent_name = ''

                for input_line in input_data.readlines():
                    trimmed_input_line = input_line.strip('\n\t\r')
                    output_line_words = trimmed_input_line.split(';')
                    print(output_line_words)

                    if len(output_line_words) == 4:
                        escape_item = output_line_words[0]
                        if self.escape_prefix == escape_item:
                            continue

                        item_name = output_line_words[2].replace('  ', ' ')
                        parent_name = output_line_words[3].strip('\n\t\r')
                    else:
                        item_name = output_line_words[1].replace('  ', ' ')
                        parent_name = output_line_words[2].strip('\n\t\r')

                    parent_name = parent_name.replace('  ', '')
                    source_parent_name = parent_name.replace(' ', '_')
                    parent_name = self.new_list_prefix + '_' + parent_name ##[parent_name.index('_'):]

                    if base_parent_name != parent_name:
                        base_parent_name = parent_name
                        self.__old_parent_list.append(source_parent_name)
                        self.__new_parent_list.append(parent_name + "_list")

                        if output_line == '':
                            output_line += "\n<string-array name=\""\
                                           + parent_name.replace(" ", "_")\
                                           + "_list" \
                                           + "\">"
                        else:
                            output_line += "\n</string-array>\n"\
                                           + "\n<string-array name=\""\
                                           + parent_name.replace(" ", "_")\
                                           + "_list"\
                                           + "\">"

                    output_line += "\n<item>" + item_name + "</item>"
                output_line += "\n</string-array>\n"\

            if output_line:
                output_data = open(output_file_path, 'w')
                output_data.write(output_line)
                output_data.close()

    def generate_switch_statement(self, statement_argument, variable_name):
        output_file_code_path = path.join(self.__base_path, self.__base_dir, self.output_file_code_name)
        output_code = "switch(" + statement_argument + ") {"

        for code_index, code_line in enumerate(self.__old_parent_list):
            output_code += "\n" + "case \"" + code_line + "\":" \
                           + "\n\t" \
                           + variable_name + " = R.array." + self.__new_parent_list[code_index] \
                           + ";" + "\n\tbreak;\n"

        output_code += '}'
        output_data = open(output_file_code_path, 'w')
        output_data.write(output_code)
        output_data.close()
