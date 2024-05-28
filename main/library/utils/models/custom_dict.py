from main.library.utils.core.validations import is_list, is_object


class CustomDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{key}'"
        )

    @staticmethod
    def build_recursivelly(data: dict) -> "CustomDict":
        custom_dict = CustomDict(data)
        for key, value in custom_dict.items():
            if is_object(value):
                custom_dict[key] = CustomDict.build_recursivelly(value)
            elif is_list(value):
                custom_dict[key] = [
                    (CustomDict.build_recursivelly(item) if is_object(item) else item)
                    for item in value
                ]
            else:
                custom_dict[key] = value
        return custom_dict
