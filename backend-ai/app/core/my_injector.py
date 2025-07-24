# core/injector.py
registry = {}

def service(cls):
    """Đánh dấu class là injectable service"""
    instance = cls()
    registry[cls.__name__] = instance
    return cls

def inject(func):
    """Inject các tham số có annotation trùng với service"""
    def wrapper(*args, **kwargs):
        injected_args = {}
        for name, cls in func.__annotations__.items():
            if name not in kwargs and cls.__name__ in registry:
                injected_args[name] = registry[cls.__name__]
        return func(*args, **{**kwargs, **injected_args})
    return wrapper
