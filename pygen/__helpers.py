import contextvars


def get_module():
    ctx = contextvars.copy_context()
    for item in ctx.items():
        if item[0].name == "genesis":
            return item[1]
