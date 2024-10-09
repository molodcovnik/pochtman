from services.models import Field, FormTypeEnum


def create_fields():
    Field.objects.create(
        field_name='Email',
        field_type=FormTypeEnum.EMAIL
    )

    Field.objects.create(
        field_name='Name',
        field_type=FormTypeEnum.TEXT
    )

    Field.objects.create(
        field_name='Date',
        field_type=FormTypeEnum.DATE
    )

    Field.objects.create(
        field_name='Phone',
        field_type=FormTypeEnum.PHONE
    )

    Field.objects.create(
        field_name='Text',
        field_type=FormTypeEnum.TEXT
    )


def run():
    create_fields()
