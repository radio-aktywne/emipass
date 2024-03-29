from collections.abc import Iterable
from typing import TextIO

from omegaconf import OmegaConf
from pydantic import ValidationError
from yaml import YAMLError

from emipass.config.errors import ConfigParseError
from emipass.config.models import Config


class ConfigBuilder:
    """Builds the config.

    Args:
        file: File-like object to load config from.
        overrides: Config overrides in the form of a dotlist.
    """

    def __init__(
        self,
        file: TextIO | None = None,
        overrides: Iterable[str] | None = None,
    ) -> None:
        self._file = file
        self._overrides = overrides

    def build(self) -> Config:
        try:
            config = OmegaConf.create()
            if self._file is not None:
                config = OmegaConf.merge(config, OmegaConf.load(self._file))
            if self._overrides is not None:
                config = OmegaConf.merge(
                    config, OmegaConf.from_dotlist(list(self._overrides))
                )
            config = OmegaConf.to_container(config, resolve=True)
            return Config.model_validate(config)
        except (YAMLError, ValidationError) as e:
            raise ConfigParseError from e
