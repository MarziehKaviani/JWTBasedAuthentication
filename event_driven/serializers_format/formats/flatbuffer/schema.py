class Schema:
    def __init__(
            self,
            events_data,
            table_pattern=["\ntable {event_name} {{\n",
                           "  {field_name}: {field_type};\n"],
            files_start_pattern='namespace Events;\n',
            files_end_pattern='',
            file_name='event.fbs',
            output_directory='serializers/flatbuffer',
    ) -> None:

        self.format_name = 'flatbuffer'
        self.flatbuffers_type = {
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'str': 'string',
            'bytes': 'string',
            'datetime.datetime': 'string'
        }
        self.events_data = events_data
        self.table_pattern = table_pattern
        self.files_start_pattern = files_start_pattern
        self.files_end_pattern = files_end_pattern
        self.file_name = file_name
        self.output_directory = output_directory
        self.setup()

    def setup(self):
        events_list = [self.create_event(event) for event in self.events_data]
        self.create_file(events_list)

    def create_event(self, event):
        table_start_pattern, field_pattern = self.table_pattern
        event_text = table_start_pattern.format(event_name=event['name'])
        for field in event['fields']:
            event_text += field_pattern.format(
                field_type=self.flatbuffers_type[field['type']], field_name=field['name'])
        event_text += '}\n'
        return event_text

    def create_file(self, events_list):
        file_path = f'{self.output_directory}/{self.file_name}'
        with open(file_path, 'r+') as file:
            content = [self.files_start_pattern] if not file.read(
            ) else file.read().splitlines()
            content.extend(events_list)
            content.append(self.files_end_pattern)
            file.writelines(content)
