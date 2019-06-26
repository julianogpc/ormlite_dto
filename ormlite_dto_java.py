#!/usr/bin/env python3
import fileinput
import re

filename = 'insert.sql'
data_types = {
    "varchar": "String",
    "integer": "int",
    "blob": "byte[]",
    "datetime": "Date",
    "float": "float"
}
output = ""


def upper_repl(match):
    return match.group(1) + match.group(2).upper()


def upper_repl_first_group(match):
    return match.group(1).upper()


with fileinput.FileInput(filename) as file:
    for line in file:
        sql_table = re.search('^CREATE TABLE "(.*)".*$', line)
        sql_type = re.search('^"(.*)" (varchar|integer|blob|datetime|float).*$', line)

        if sql_type is not None:
            column_name = sql_type.group(1)
            data_type = sql_type.group(2)
            java_field_name = re.sub(r'([a-z]{1})_([a-z]{1})', upper_repl, column_name.lower())

            additional_parameter = ""
            if data_type == 'blob':
                additional_parameter = ', dataType = DataType.BYTE_ARRAY'
            elif data_type == 'datetime':
                additional_parameter = ', dataType = DataType.DATE_STRING, format = "yyyy-MM-dd\'T\'HH:mm:ss.SSS"'
            elif column_name == 'CTRL_ID':
                additional_parameter = ', canBeNull = false, id = true'

            output += '\t@DatabaseField(columnName = "%s"%s)\n' % (column_name, additional_parameter)
            output += '\tprivate %s %s;\n' % (data_types[data_type], java_field_name)
            output += '\n'
        elif sql_table is not None:
            table_name = sql_table.group(1)
            java_table_name = re.sub(r'([a-z]{1})_([a-z]{1})', upper_repl, table_name.lower())
            java_table_name = re.sub(r'^([a-z]{1})', upper_repl_first_group, java_table_name)
            output += '/**\n'
            output += ' * %s DTO\n' % (java_table_name)
            output += ' *\n'
            output += ' * @author Juliano Costa\n'
            output += ' * @version $Id: $Id\n'
            output += ' * @since 1.0.0\n'
            output += ' */\n'
            output += '@Data\n'
            output += '@DatabaseTable(tableName = "%s")\n' % (table_name)
            output += 'public class %sDTO\n' % (java_table_name)
            output += '{\n'
        else:
            raise Exception('Invalid data: {}'.format(line))

output += '}'

print(output)

