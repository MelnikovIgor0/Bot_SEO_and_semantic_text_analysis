from dataclasses import dataclass
import json

@dataclass
class BotConfig:
    bll_api_url: str
    debug: bool
    telegram_api_token: str

def parse_bot_config(path: str) -> BotConfig:
    with open(path) as f:
        json_data = json.load(f)
        return BotConfig(
            bll_api_url=json_data['bll_api_url'],
            debug=json_data['debug'],
            telegram_api_token=json_data['telegram_api_token'],
        )
