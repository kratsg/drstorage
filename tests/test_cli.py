import shlex
import drstorage
import time
import subprocess
import pytest


@pytest.fixture(
    scope="function",
    params=[
        (
            "F1_600",
            "abab00471200c5120901000000000000000a10025810000000000000140d0a",
            "humidity = 7.1    temperature = 19.7",
        )
    ],
    ids=["F1_600"],
)
def data(tmp_path, request):
    model, input_data, stdout = request.param
    temp = tmp_path / "data"
    temp.write_bytes(bytearray.fromhex(input_data) * 3)
    return temp, model, stdout


def test_version(script_runner):
    command = "drstorage --version"
    start = time.time()
    ret = script_runner.run(*shlex.split(command))
    end = time.time()
    elapsed = end - start
    assert ret.success
    assert drstorage.__version__ in ret.stdout
    assert ret.stderr == ""
    # make sure it took less than a second
    assert elapsed < 1.0


def test_delayed_pipe_parse(data):
    fpath, model, stdout = data
    command_in = f"""perl -pe "system 'sleep 1'" {fpath}"""
    command = f"drstorage parse --model {model}"
    ps = subprocess.Popen(shlex.split(command_in), stdout=subprocess.PIPE)
    output = subprocess.check_output(shlex.split(command), stdin=ps.stdout)
    assert ps.stdout.read() == b"", "All of the piped input was not read in"
    assert len(output) > 100, "More output was expected"
    assert stdout in output.decode("utf-8")


def test_parse(script_runner, data):
    fpath, model, stdout = data
    command = f"drstorage parse --model {model} {fpath}"
    ret = script_runner.run(*shlex.split(command))
    assert ret.success
    assert len(ret.stdout) > 100
    assert stdout in ret.stdout
    assert ret.stderr == ""
