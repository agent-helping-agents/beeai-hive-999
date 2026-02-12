#!/usr/bin/env python3
"""
Energetic Lexicon Database - Encryption Wrapper
🔒 PRIVATE - PROPRIETARY
© 2025 Bakery Street Project

GPG-based encryption/decryption utilities for secure data storage.
Uses AES256 symmetric encryption with vault password file.
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Union
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EncryptionConfig:
    """Configuration for encryption operations"""
    vault_password_file: Path = Path.home() / '.primax_vault_password'
    cipher_algo: str = 'AES256'
    compression_algo: str = 'ZLIB'
    armor: bool = False  # Binary output by default

    def __post_init__(self):
        """Validate configuration"""
        if not self.vault_password_file.exists():
            raise FileNotFoundError(
                f"Vault password file not found: {self.vault_password_file}\n"
                "Create it with: echo 'your-secure-password' > ~/.primax_vault_password && chmod 600 ~/.primax_vault_password"
            )

        # Verify file permissions (should be 600)
        stat_info = self.vault_password_file.stat()
        if stat_info.st_mode & 0o777 != 0o600:
            logger.warning(
                f"Vault password file has insecure permissions: {oct(stat_info.st_mode)}\n"
                f"Run: chmod 600 {self.vault_password_file}"
            )


class EncryptionWrapper:
    """GPG encryption wrapper for database files"""

    def __init__(self, config: Optional[EncryptionConfig] = None):
        """
        Initialize encryption wrapper

        Args:
            config: Encryption configuration (uses defaults if None)
        """
        self.config = config or EncryptionConfig()
        logger.info(f"Initialized encryption wrapper with {self.config.cipher_algo}")

    def encrypt_file(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        delete_original: bool = False
    ) -> Path:
        """
        Encrypt a file using GPG symmetric encryption

        Args:
            input_path: Path to file to encrypt
            output_path: Path for encrypted output (default: input_path + '.gpg')
            delete_original: Whether to delete the original file after encryption

        Returns:
            Path to encrypted file

        Raises:
            FileNotFoundError: If input file doesn't exist
            subprocess.CalledProcessError: If encryption fails
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Default output path
        if output_path is None:
            output_path = input_path.with_suffix(input_path.suffix + '.gpg')
        else:
            output_path = Path(output_path)

        logger.info(f"Encrypting {input_path} → {output_path}")

        # Build GPG command
        cmd = [
            'gpg',
            '--symmetric',
            '--cipher-algo', self.config.cipher_algo,
            '--compress-algo', self.config.compression_algo,
            '--batch',
            '--yes',
            '--quiet',
            '--passphrase-file', str(self.config.vault_password_file),
            '--output', str(output_path),
            str(input_path)
        ]

        if self.config.armor:
            cmd.insert(1, '--armor')

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"Successfully encrypted {input_path}")

            # Delete original if requested
            if delete_original:
                input_path.unlink()
                logger.info(f"Deleted original file: {input_path}")

            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Encryption failed: {e.stderr}")
            raise

    def decrypt_file(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        delete_encrypted: bool = False
    ) -> Path:
        """
        Decrypt a GPG-encrypted file

        Args:
            input_path: Path to encrypted file
            output_path: Path for decrypted output (default: strip .gpg extension)
            delete_encrypted: Whether to delete encrypted file after decryption

        Returns:
            Path to decrypted file

        Raises:
            FileNotFoundError: If input file doesn't exist
            subprocess.CalledProcessError: If decryption fails
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Encrypted file not found: {input_path}")

        # Default output path (strip .gpg extension)
        if output_path is None:
            if input_path.suffix == '.gpg':
                output_path = input_path.with_suffix('')
            else:
                output_path = input_path.with_suffix('.decrypted')
        else:
            output_path = Path(output_path)

        logger.info(f"Decrypting {input_path} → {output_path}")

        # Build GPG command
        cmd = [
            'gpg',
            '--decrypt',
            '--batch',
            '--yes',
            '--quiet',
            '--passphrase-file', str(self.config.vault_password_file),
            '--output', str(output_path),
            str(input_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"Successfully decrypted {input_path}")

            # Delete encrypted if requested
            if delete_encrypted:
                input_path.unlink()
                logger.info(f"Deleted encrypted file: {input_path}")

            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Decryption failed: {e.stderr}")
            raise

    def encrypt_data(self, data: bytes) -> bytes:
        """
        Encrypt raw bytes data

        Args:
            data: Raw bytes to encrypt

        Returns:
            Encrypted bytes
        """
        cmd = [
            'gpg',
            '--symmetric',
            '--cipher-algo', self.config.cipher_algo,
            '--compress-algo', self.config.compression_algo,
            '--batch',
            '--yes',
            '--quiet',
            '--passphrase-file', str(self.config.vault_password_file)
        ]

        if self.config.armor:
            cmd.insert(1, '--armor')

        try:
            result = subprocess.run(
                cmd,
                input=data,
                check=True,
                capture_output=True
            )
            return result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Data encryption failed: {e.stderr}")
            raise

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt raw bytes data

        Args:
            encrypted_data: Encrypted bytes

        Returns:
            Decrypted bytes
        """
        cmd = [
            'gpg',
            '--decrypt',
            '--batch',
            '--yes',
            '--quiet',
            '--passphrase-file', str(self.config.vault_password_file)
        ]

        try:
            result = subprocess.run(
                cmd,
                input=encrypted_data,
                check=True,
                capture_output=True
            )
            return result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Data decryption failed: {e.stderr}")
            raise

    def encrypt_directory(
        self,
        dir_path: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
        extensions: Optional[list[str]] = None,
        recursive: bool = True
    ) -> list[Path]:
        """
        Encrypt all files in a directory

        Args:
            dir_path: Directory to encrypt
            output_dir: Output directory for encrypted files (default: same as input)
            extensions: File extensions to encrypt (default: all files)
            recursive: Whether to recurse into subdirectories

        Returns:
            List of encrypted file paths
        """
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")

        output_dir = Path(output_dir) if output_dir else dir_path
        output_dir.mkdir(parents=True, exist_ok=True)

        encrypted_files = []

        # Get files to encrypt
        pattern = '**/*' if recursive else '*'
        for file_path in dir_path.glob(pattern):
            if not file_path.is_file():
                continue

            # Filter by extension if specified
            if extensions and file_path.suffix not in extensions:
                continue

            # Skip already encrypted files
            if file_path.suffix == '.gpg':
                continue

            # Calculate output path (preserve directory structure)
            rel_path = file_path.relative_to(dir_path)
            output_path = output_dir / f"{rel_path}.gpg"
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Encrypt file
            try:
                encrypted_path = self.encrypt_file(file_path, output_path)
                encrypted_files.append(encrypted_path)
            except Exception as e:
                logger.error(f"Failed to encrypt {file_path}: {e}")

        logger.info(f"Encrypted {len(encrypted_files)} files from {dir_path}")
        return encrypted_files


# Convenience functions
def encrypt(input_path: Union[str, Path], **kwargs) -> Path:
    """Convenience function for encrypting a file"""
    wrapper = EncryptionWrapper()
    return wrapper.encrypt_file(input_path, **kwargs)


def decrypt(input_path: Union[str, Path], **kwargs) -> Path:
    """Convenience function for decrypting a file"""
    wrapper = EncryptionWrapper()
    return wrapper.decrypt_file(input_path, **kwargs)


# CLI interface
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Energetic Lexicon Database - Encryption Utility'
    )
    parser.add_argument(
        'action',
        choices=['encrypt', 'decrypt', 'encrypt-dir'],
        help='Action to perform'
    )
    parser.add_argument(
        'input',
        type=Path,
        help='Input file or directory'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file or directory (optional)'
    )
    parser.add_argument(
        '-d', '--delete',
        action='store_true',
        help='Delete original file after encryption/decryption'
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recurse into subdirectories (for encrypt-dir)'
    )
    parser.add_argument(
        '-e', '--extensions',
        nargs='+',
        help='File extensions to encrypt (e.g., .db .sql)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        wrapper = EncryptionWrapper()

        if args.action == 'encrypt':
            result = wrapper.encrypt_file(
                args.input,
                args.output,
                delete_original=args.delete
            )
            print(f"✅ Encrypted: {result}")

        elif args.action == 'decrypt':
            result = wrapper.decrypt_file(
                args.input,
                args.output,
                delete_encrypted=args.delete
            )
            print(f"✅ Decrypted: {result}")

        elif args.action == 'encrypt-dir':
            results = wrapper.encrypt_directory(
                args.input,
                args.output,
                extensions=args.extensions,
                recursive=args.recursive
            )
            print(f"✅ Encrypted {len(results)} files")

    except Exception as e:
        logger.error(f"Error: {e}")
        exit(1)
