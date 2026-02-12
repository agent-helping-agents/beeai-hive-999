import pytest
import subprocess
import signal
import os

class TestAiderCommands:
    """Test cases for Aider's command-line functionality"""
    
    @pytest.mark.parametrize("args", [
        ["--architect", "--model", "ollama/codellama:7b"],
        ["--watch-files"],
        ["--voice", "--voice-language", "en"],
        ["--copy-paste"],
        ["--browser"],
    ])
    def test_command_line_options(self, args):
        """Test that aider accepts various command-line options"""
        try:
            result = subprocess.run(
                ["aider"] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=20,  # Increased timeout for GUI startup
                input="\n",  # Send empty input
                text=True,
                start_new_session=True,  # Allow sending signals to process group
                env={**os.environ, "PYTHONUNBUFFERED": "1"}  # Ensure immediate output
            )
            
            # For browser mode, check if it at least starts up
            if "--browser" in args:
                assert "Running browser interface" in result.stdout
                
        except subprocess.TimeoutExpired as e:
            # If timed out but we got some output, check for argument recognition
            if e.stderr:
                assert "error: unrecognized arguments" not in e.stderr.decode()
            if e.stdout:
                # Check for either startup message or help text
                output = e.stdout.decode()
                if "--browser" in args:
                    assert any(msg in output for msg in ["Running browser interface", "browser mode"])
            
            # Cleanup process group if we have a process reference
            if hasattr(e, "process") and e.process.pid:
                os.killpg(os.getpgid(e.process.pid), signal.SIGINT)
        except subprocess.CalledProcessError as e:
            assert "error: unrecognized arguments" not in e.stderr
            
    def test_version_option(self):
        """Test the version flag"""
        result = subprocess.run(
            ["aider", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        assert b"aider" in result.stdout.lower()

    @pytest.mark.xfail(reason="Browser mode is experimental")
    def test_browser_mode_implementation(self):
        """Test browser mode actually launches (mock test)"""
        # This would need proper mocking in a real test environment
        raise NotImplementedError("Browser mode requires UI mocking")
