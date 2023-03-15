class WarehouseMixin:
    def get_queryset(self):
        queryset = self.filter_queryset(super().get_queryset())

        if self.request.user.is_superuser:
            return queryset

        warehouses = self.request.user.warehouses.all().values("warehouse")
        return queryset.filter(warehouse__in=warehouses)
