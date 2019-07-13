#!/usr/bin/env python3
import fileinput
import re

filename = 'schema.sql'
data_types = {
    "varchar": "String",
    "integer": "int",
    "blob": "byte[]",
    "datetime": "Date",
    "float": "float"
}
output = ''
package = ''
dto = {}
table = ''

pattern_table = '^CREATE TABLE IF NOT EXISTS "(.*)" \\($'
pattern_type = '^"(.*)" (varchar|integer|blob|datetime|float).*$'


with fileinput.FileInput(filename) as file:
    for line in file:
        sql_table = re.search(pattern_table, line)
        sql_type = re.search(pattern_type, line)

        if sql_type is not None:
            column_name = sql_type.group(1)
            data_type = sql_type.group(2)

            item = {
                column_name: {
                    "data_type": data_type
                }
            }

            dto[table_name].append(item)

        elif sql_table is not None:
            table_name = sql_table.group(1)
            dto[table_name] = []


def upper_repl(match):
    return match.group(1) + match.group(2).upper()


def upper_repl_first_group(match):
    return match.group(1).upper()


def dto_output(table_name, column_name, data_type):
    output = ''
    column_name_static = ''
    if column_name is not None and data_type is not None:
        java_field_name = re.sub(r'([a-z]{1})_([a-z]{1})', upper_repl, column_name.lower())

        additional_parameter = ""
        if data_type == 'blob':
            additional_parameter = ', dataType = DataType.BYTE_ARRAY'
        elif data_type == 'datetime':
            additional_parameter = ', dataType = DataType.DATE_STRING, format = "yyyy-MM-dd\'T\'HH:mm:ss.SSS"'
        elif column_name == 'CTRL_ID':
            additional_parameter = ', canBeNull = false, id = true'

        column_name_static += '\tpublic static final String COLUMN_%s = "%s";\n' % (column_name, column_name)

        output += '\t@DatabaseField(columnName = COLUMN_%s %s)\n' % (column_name, additional_parameter)
        output += '\tprivate %s %s;\n' % (data_types[data_type], java_field_name)
        output += '\n'
    elif table_name is not None:
        java_table_name = re.sub(r'([a-z]{1})_([a-z]{1})', upper_repl, table_name.lower())
        java_table_name = re.sub(r'^([a-z]{1})', upper_repl_first_group, java_table_name)

        output += package + '\n'
        output += '\n'
        output += 'import com.j256.ormlite.field.DataType;\n'
        output += 'import com.j256.ormlite.field.DatabaseField;\n'
        output += 'import com.j256.ormlite.table.DatabaseTable;\n'
        output += 'import lombok.Data;\n'
        output += '\n'
        output += 'import java.util.Date;\n'
        output += '\n'

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
    return output, column_name_static


for table in dto.keys():
    print(table)
    java_dto_output_header = dto_output(table, None, None)
    java_dto_output_fields = []
    for data in dto[table]:
        for data_attr in data.keys():
            data_type = data[data_attr]['data_type']
            print('\t' + data_attr + ' ==> ' + data_type)
            java_dto_output_fields.append(dto_output(None, data_attr, data_type))

    java_file_name = re.sub(r'([a-z]{1})_([a-z]{1})', upper_repl, table.lower())
    java_file_name = re.sub(r'^([a-z]{1})', upper_repl_first_group, java_file_name)
    java_file = open('%sDTO.java' % java_file_name
                     , 'wb')
    java_file.write(java_dto_output_header[0].encode('utf-8'))
    for java_dto_output_field in java_dto_output_fields:
        java_file.write(java_dto_output_field[1].encode('utf-8'))

    java_file.write('\n'.encode('utf-8'))

    for java_dto_output_field in java_dto_output_fields:
        java_file.write(java_dto_output_field[0].encode('utf-8'))
    java_file.write('}'.encode('utf-8'))
    java_file.close()




