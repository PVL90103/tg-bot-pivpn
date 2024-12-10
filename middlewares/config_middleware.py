from aiogram import BaseMiddleware

class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config_dir: str):
        super().__init__()
        self.config_dir = config_dir

    async def __call__(self, handler, event, data):
        data['config_dir'] = self.config_dir
        return await handler(event, data)
