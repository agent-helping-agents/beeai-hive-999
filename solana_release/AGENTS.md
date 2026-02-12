# Solana Release (v1.18.26)

This is a **Solana blockchain software release package** (version 1.18.26), containing pre-built binaries for running a Solana validator, CLI tools, and SBF (Solana Binary Format) program development SDK.

## Project Overview

This is a binary distribution of the Solana Labs client software, built from commit `d9f20e951a06b61e4505da0955228020b96a8915` for the `x86_64-unknown-linux-gnu` target.

**⚠️ Important Notice**: The `solana-install` tool is deprecated and will be discontinued when v1.18 is no longer supported. Users should migrate to [Agave](https://github.com/anza-xyz/agave/wiki/Agave-Transition).

## Technology Stack

- **Language**: Rust (built with rustc 1.75.0)
- **Target Platform**: x86_64-unknown-linux-gnu
- **SBF Target**: sbf-solana-solana (for on-chain programs)
- **LLVM Version**: 17.0.6 (for SBF compilation)

## Directory Structure

```
/home/boozelee/solana-release/
├── bin/                          # All executable binaries
│   ├── solana                    # Main CLI tool
│   ├── solana-validator          # Validator node
│   ├── solana-test-validator     # Local test validator
│   ├── solana-genesis            # Genesis block creation
│   ├── solana-ledger-tool        # Ledger manipulation
│   ├── solana-keygen             # Keypair generation
│   ├── solana-faucet             # Test faucet
│   ├── solana-gossip             # Gossip protocol tool
│   ├── solana-install            # Software installer (DEPRECATED)
│   ├── solana-stake-accounts     # Stake account management
│   ├── solana-tokens             # Token distribution
│   ├── solana-watchtower         # Validator monitoring
│   ├── solana-bench-tps          # TPS benchmarking
│   ├── solana-dos                # DoS testing tool
│   ├── solana-log-analyzer       # Log analysis
│   ├── solana-net-shaper         # Network simulation
│   ├── spl-token                 # SPL token CLI (v3.4.1)
│   ├── solang                    # Solidity compiler for Solana
│   ├── cargo-build-bpf           # Legacy BPF build tool
│   ├── cargo-build-sbf           # SBF build tool for Rust programs
│   ├── cargo-test-bpf            # Legacy BPF test tool
│   ├── cargo-test-sbf            # SBF test tool
│   ├── rbpf-cli                  # SBF program debugger (deprecated, use solana-ledger-tool)
│   ├── deps/                     # Runtime dependencies
│   │   ├── libsolana_program.rlib
│   │   └── libsolana_program.so
│   ├── perf-libs/                # Performance libraries
│   │   ├── libpoh-simd.so        # PoH SIMD optimizations
│   │   ├── libsigning.so         # Signing library
│   │   ├── signing.signed.so     # Signed version
│   │   ├── cuda-10.0/            # CUDA 10.0 libraries
│   │   ├── cuda-10.1/            # CUDA 10.1 libraries
│   │   ├── cuda-10.2/            # CUDA 10.2 libraries
│   │   └── solana-perf.tgz       # Performance package
│   └── sdk/                      # Software Development Kit
│       └── sbf/                  # SBF (Solana Binary Format) SDK
│           ├── env.sh            # Environment setup script
│           ├── syscalls.txt      # Syscall definitions
│           ├── scripts/          # Build scripts
│           │   ├── install.sh    # SDK installer
│           │   ├── dump.sh       # ELF dumper
│           │   ├── objcopy.sh    # Object copy
│           │   ├── package.sh    # Packaging script
│           │   └── strip.sh      # Binary stripper
│           └── c/                # C/C++ SBF SDK
│               ├── README.md     # C SDK documentation
│               ├── sbf.mk        # Main Makefile
│               ├── sbf.ld        # Linker script
│               └── inc/          # Header files
│                   ├── solana_sdk.h
│                   └── sol/      # Solana-specific headers
├── version.yml                   # Version information
├── .crates.toml                  # Installed crates info
└── .crates2.json                 # Extended crates metadata
```

## Key Binaries

### Core CLI
- `solana` - Main command-line interface for interacting with Solana clusters
- `solana-validator` - Full validator node for mainnet/testnet/devnet
- `solana-test-validator` - Single-node test validator for local development

### Development Tools
- `cargo-build-sbf` - Build Rust programs for SBF target
- `cargo-test-sbf` - Test SBF programs
- `solang` - Compile Solidity to SBF
- `rbpf-cli` - SBF program runner (deprecated, use `solana-ledger-tool program run`)

### Utility Tools
- `solana-keygen` - Generate and manage keypairs
- `solana-genesis` - Create genesis configurations
- `solana-ledger-tool` - Inspect and manipulate ledgers
- `solana-faucet` - Local SOL faucet for testing
- `spl-token` - SPL token management

## SBF (Solana Binary Format) SDK

The SBF SDK allows writing on-chain programs in C/C++:

### Quick Start for C Programs

1. Create a `makefile`:
```make
include /path/to/sbf.mk
```

2. Create `src/program.c`:
```c
#include <solana_sdk.h>

extern uint64_t entrypoint(const uint8_t *input) {
  SolAccountInfo ka[1];
  SolParameters params = (SolParameters) { .ka = ka };

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(ka))) {
    return ERROR_INVALID_ARGUMENT;
  }
  return SUCCESS;
}
```

3. Build: `make`
4. Output: `out/program.so`

### Build Commands

```bash
# Build all programs
make all

# Build specific program
make <program_name>

# Build and run tests
make tests

# Dump ELF contents
make dump_<program_name>

# Display ELF info
make readelf_<program_name>

# Clean build artifacts
make clean
```

### C SDK Limitations
- Programs must be fully contained within a single .c file
- No libc available; use `solana_sdk.h` for primitives

### Unit Testing (C)

Uses [Criterion](https://criterion.readthedocs.io/) framework:

1. Create `test/example.c`:
```c
#include <criterion/criterion.h>
#include "../src/program.c"

Test(test_suite_name, test_case_name) {
  cr_assert(true);
}
```

2. Run: `make test`

## Common CLI Commands

### Cluster Interaction
```bash
# Set cluster
solana config set --url localhost  # or mainnet-beta, testnet, devnet

# Check balance
solana balance

# Request airdrop (test clusters only)
solana airdrop 1

# Transfer SOL
solana transfer <RECIPIENT> <AMOUNT>

# Deploy program
solana program deploy <PROGRAM.so>
```

### Validator Operations
```bash
# Start test validator
solana-test-validator

# Start with specific ledger
solana-test-validator --ledger <DIR>

# Reset ledger
solana-test-validator --reset
```

### Key Management
```bash
# Generate new keypair
solana-keygen new --outfile <KEYPAIR_FILE>

# Display public key
solana-keygen pubkey <KEYPAIR_FILE>

# Recover from seed phrase
solana-keygen recover
```

## Configuration

Default config locations:
- CLI config: `~/.config/solana/cli/config.yml`
- Install config: `~/.config/solana/install/config.yml`

## Build Configuration

### SBF C/C++ Build Flags
- Target: `sbf` (Solana Binary Format)
- Standard: C17 / C++17
- Optimization: `-O2`
- Warnings: `-Werror`

### Environment Variables
- `SBF_OUT_PATH` - Output directory for SBF builds
- `SOL_SBFV2=1` - Enable SBFv2 features

## Testing

### Local Testing
```bash
# Start local validator
solana-test-validator

# In another terminal, run tests
solana program deploy <your_program.so>
```

### Program Testing
```bash
# Test SBF programs
cargo-test-sbf

# With specific features
cargo-test-sbf --features <FEATURE_NAME>
```

## Security Considerations

1. **Key Management**: Keep keypair files secure and never commit them to version control
2. **Program Deployment**: Always verify program addresses before deployment
3. **Validator Keys**: Use dedicated hardware for validator identity keys
4. **Deprecated Tools**: `solana-install` is deprecated; plan migration to Agave
5. **Signing Library**: The `signing.so` library in `perf-libs/` is signed for integrity verification

## Version Information

- **Channel**: v1.18.26
- **Commit**: d9f20e951a06b61e4505da0955228020b96a8915
- **Target**: x86_64-unknown-linux-gnu
- **Rustc**: 1.75.0
- **SPL Token CLI**: 3.4.1
- **Solang**: v0.3.3

## Additional Resources

- [Solana Documentation](https://docs.solana.com/)
- [Agave Transition Guide](https://github.com/anza-xyz/agave/wiki/Agave-Transition)
- [SBF SDK C Examples](bin/sdk/sbf/c/README.md)
