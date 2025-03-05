import pytest

from app.config.database import DBSettings

from . import database_data as data


class TestDatabaseConfig:

    @pytest.mark.parametrize("data", data.test_config)
    def test_db_config(self, data):
        engine_data = {
            data["engine"]: data[data["engine"]],
        }
        conf = DBSettings(
            engine=data["engine"],
            **engine_data,
        )

        assert conf.engine == data["engine"]
        engine_config = getattr(conf, conf.engine)

        # Check engine config values are set
        for key, value in engine_data[data["engine"]].items():
            assert getattr(engine_config, key) == value

        assert conf.url == engine_config.url

    @pytest.mark.parametrize("engine", [1, None, "", "invalid"])
    def test_invalid_engine(self, engine):
        with pytest.raises(ValueError, match="Input should be"):
            DBSettings(
                engine=engine,
            )

    def test_missing_engine(self):
        with pytest.raises(ValueError, match="Field required"):
            DBSettings()

    @pytest.mark.parametrize("engine", ["sqlite", "postgres"])
    def test_missing_engine_config(self, engine):
        with pytest.raises(
            ValueError,
            match=f"Database engine is set to '{engine}' but no config provided",
        ):
            DBSettings(engine=engine)
