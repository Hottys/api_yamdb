from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    '''Вьюсет создаёт экземпляр объекта,

    удаляет экземпляр объекта и возвращает список объектов
    '''
    pass


class NoPutViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    '''Вьюсет создаёт экземпляр объекта,

    удаляет экземпляр объекта, возвращает список объектов или объект,
    частично обновляет объект. Не обрабатывает PUT-запрос!
    '''
    http_method_names = ['get', 'post', 'patch', 'delete']
