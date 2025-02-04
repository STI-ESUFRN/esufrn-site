class WarehouseMixin:
    def get_queryset(self):
        queryset = self.filter_queryset(super().get_queryset())

        if self.request.user.is_superuser:
            return queryset

        warehouses = self.request.user.warehouses.all().values("warehouse")
        return queryset.filter(warehouse__in=warehouses)

class WarehouseMixinTI:
    def get_queryset(self):
        queryset = self.filter_queryset(super().get_queryset())

        if self.request.user.is_superuser:
            return queryset

        warehouses_ti = self.request.user.warehouses_ti.all().values("warehouse_ti")
        return queryset.filter(warehouse_ti__in=warehouses_ti)