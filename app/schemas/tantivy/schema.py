import tantivy


schema_builder = tantivy.SchemaBuilder()
schema_builder.add_text_field("id", stored=True)
schema_builder.add_text_field("first_name", stored=True)
schema_builder.add_text_field("middle_name",stored=True)
schema_builder.add_text_field("last_name",stored=True)
schema_builder.add_text_field("email",stored=True)
schema_builder.add_text_field("phone", stored=True)
schema = schema_builder.build()