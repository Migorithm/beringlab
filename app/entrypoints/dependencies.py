from app.service_layer.unit_of_work import SqlAlchemyUnitOfWork


def get_unit_of_work():
    return SqlAlchemyUnitOfWork()
