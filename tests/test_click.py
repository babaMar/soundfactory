import click
from click.testing import CliRunner
from settings.input_validators import (
    ArbitraryNArgs, WaveComponent, DEFAULT_PHASE, DEFAULT_WAVE_TYPE
)


def test_wavecomponent(bad_wavecomponents):
    @click.command()
    @click.option(
        "--wc", cls=ArbitraryNArgs, type=WaveComponent(), multiple=True)
    def _wavecomponent_option(wc):
        click.echo(wc)

    runner = CliRunner()
    good_result = runner.invoke(
        _wavecomponent_option,
        "--wc 1 1 2 sine --wc 1.34 3. --wc 1 3 square --wc 1 0 3",
    )
    assert good_result.output.strip("\n") == "(" + ", ".join((
        str((1., 1., 2., "sine")),
        str((1.34, 3., DEFAULT_PHASE, DEFAULT_WAVE_TYPE)),
        str((1., 3., DEFAULT_PHASE, "square")),
        str((1., 0., 3., DEFAULT_WAVE_TYPE))
    )) + ")"

    for bad_wc in bad_wavecomponents:
        bad_result = runner.invoke(_wavecomponent_option, ["--wc", bad_wc])
        assert bad_result.exit_code == 2

