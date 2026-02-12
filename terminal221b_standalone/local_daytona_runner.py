import os
import asyncio
import json
import logging
from daytona import AsyncDaytona
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_daytona_staking_agent():
    """
    Orchestrates the execution of the StakingAgent within a Daytona sandbox.
    """
    sandbox = None # Initialize sandbox to None for the outer finally block
    try:
        logger.info("Initializing Daytona client asynchronously...")
        async with AsyncDaytona() as daytona:
            logger.info("Creating Daytona sandbox...")
            sandbox = await daytona.create() # Create a new sandbox

            # Define the user-accessible base path within the sandbox
            sandbox_base_path = "/home/user/app"

            # Explicitly create the base directory in the sandbox
            logger.info(f"Creating {sandbox_base_path} directory in sandbox...")
            await sandbox.fs.create_folder(sandbox_base_path, "755") # Use common permissions
            logger.info(f"{sandbox_base_path} directory created successfully.")

            # Define paths
            project_root = Path(__file__).resolve().parent # This script is in terminal221b/
            agent_dir = project_root / "monetization" / "daytona_functions" / "staking_agent"
            monetization_root = project_root / "monetization"

            # --- Bypass fs.upload_file and create file directly via exec ---
            logger.info("Bypassing fs.upload_file and creating a test file directly in sandbox via exec...")
            direct_write_command = f"echo 'Hello Daytona! Direct Sandbox Write.' > {sandbox_base_path}/direct_write.txt"
            direct_write_result = await sandbox.process.exec(direct_write_command, timeout=30)
            if direct_write_result.exit_code == 0:
                logger.info(f"File 'direct_write.txt' created successfully via exec. Stdout: {direct_write_result.stdout}")
            else:
                logger.error(f"Failed to create file via exec. Stderr: {direct_write_result.stderr}")
                raise Exception(f"Direct file creation via exec failed: {direct_write_result.stderr}")

            logger.info(f"Verifying content of {sandbox_base_path}/direct_write.txt...")
            cat_result = await sandbox.process.exec(f"cat {sandbox_base_path}/direct_write.txt", timeout=30)
            if cat_result.exit_code == 0:
                logger.info(f"Content of direct_write.txt: {cat_result.stdout.strip()}")
            else:
                logger.error(f"Failed to read file via exec. Stderr: {cat_result.stderr}")
                raise Exception(f"Direct file read via exec failed: {cat_result.stderr}")
            
            # Commented out original uploads for debugging
            # logger.info(f"Uploading terminal221b/test_file.txt content directly as bytes to {sandbox_base_path}/test_file.txt...")
            # test_file_path = project_root / "test_file.txt"
            # # Read content as bytes
            # try:
            #     with open(test_file_path, "rb") as f:
            #         file_content_bytes = f.read()
            # except FileNotFoundError:
            #     logger.error(f"Test file not found at {test_file_path}. Please create it.")
            #     raise
            # await sandbox.fs.upload_file(file_content_bytes, f"{sandbox_base_path}/test_file.txt")
            # logger.info("Test file uploaded successfully (via bytes overload).")

            # Commented out original uploads for debugging
            # # --- Upload Agent Code and Dependencies ---
            # # logger.info(f"Uploading {agent_dir}/daytona_staking_agent.py to sandbox...")
            # # await sandbox.fs.upload_file(str(agent_dir / "daytona_staking_agent.py"), "/app/daytona_staking_agent.py")
            
            # # logger.info(f"Uploading {agent_dir}/requirements.txt to sandbox...")
            # # await sandbox.fs.upload_file(str(agent_dir / "requirements.txt"), "/app/requirements.txt")

            # # # Upload the entire monetization directory for proper imports
            # # logger.info(f"Uploading monetization directory ({monetization_root}) to sandbox...")
            # # await sandbox.fs.upload_directory(str(monetization_root), "/app/monetization")

            # --- Install Dependencies within Sandbox ---
            # This part will likely fail now as the actual requirements.txt for the agent is not uploaded
            logger.info("Installing dependencies in Daytona sandbox...")
            install_result = await sandbox.process.exec("pip install -r /app/requirements.txt", timeout=300)
            if install_result.exit_code != 0:
                logger.error(f"Dependency installation failed. Stdout: {install_result.stdout}, Stderr: {install_result.stderr}")
                raise Exception("Sandbox dependency installation failed.")
            logger.info("Dependencies installed successfully in sandbox.")
            logger.debug(f"Install Stdout: {install_result.stdout}")

            # --- Execute the Agent Script ---
            # This part will also fail as daytona_staking_agent.py is not uploaded
            logger.info("Executing StakingAgent in Daytona sandbox...")
            command = "PYTHONPATH=/app:/app/monetization /usr/bin/python3 /app/daytona_staking_agent.py"
            
            env_vars = {"SOLANA_RPC_URL": os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")}
            
            execution_result = await sandbox.process.exec(command, timeout=300, env=env_vars) # 5 minutes timeout

            if execution_result.exit_code == 0:
                logger.info("StakingAgent execution successful in Daytona sandbox.")
                logger.info("Sandbox Output:")
                print(execution_result.stdout)
                try:
                    parsed_output = json.loads(execution_result.stdout)
                    logger.info(f"Parsed StakingAgent result: {parsed_output}")
                    return parsed_output
                except json.JSONDecodeError:
                    logger.warning("StakingAgent output was not valid JSON.")
                    return {"status": "success", "raw_output": execution_result.stdout}
            else:
                logger.error(f"StakingAgent execution failed in Daytona sandbox. Exit Code: {execution_result.exit_code}")
                logger.error(f"Sandbox Stdout: {execution_result.stdout}")
                logger.error(f"Sandbox Stderr: {execution_result.stderr}")
                raise Exception(f"Sandbox execution failed: {execution_result.stderr}")
    except Exception as e:
        logger.exception("An error occurred during Daytona sandbox operation.")
        raise
    finally: # This finally is for the outer try block, ensuring sandbox closure
        # The AsyncDaytona context manager should handle closing resources created within its context.
        # Explicit sandbox.close() is not needed and causes AttributeError.
        pass

if __name__ == "__main__":
    asyncio.run(run_daytona_staking_agent())
