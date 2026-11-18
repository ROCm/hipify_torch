import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).resolve().parents[1] / "hipify_cli.py"


class TestHipifyCLI(unittest.TestCase):
    def test_extra_extensions(self):
        for use_config in (False, True):
            with self.subTest(use_config=use_config), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = root / "src"
                source.mkdir()
                for name in ("sample.pyx", "header.pxd", "notes.txt"):
                    (source / name).write_text("cdef int cudaGetDeviceCount(int* count)\n")

                if use_config:
                    config = root / "config.json"
                    config.write_text(json.dumps({
                        "project_directory": "src",
                        "output_directory": "out",
                        "extra_extensions": [".pyx", ".pxd"],
                    }))
                    args = ["--config-json", str(config)]
                else:
                    args = [
                        "--project-directory", str(source),
                        "--output-directory", str(root / "out"),
                        "--extra-extensions", ".pyx", ".pxd",
                    ]

                result_file = root / "result.json"
                subprocess.run(
                    [sys.executable, str(CLI), *args, "--dump-dict-file", str(result_file)],
                    check=True,
                    capture_output=True,
                )
                results = json.loads(result_file.read_text())
                self.assertEqual({Path(key).name for key in results}, {"sample.pyx", "header.pxd"})
                for result in results.values():
                    self.assertIn("hipGetDeviceCount", Path(result["hipified_path"]).read_text())
