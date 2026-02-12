"""
Solend instruction packing/unpacking and creation utilities.

This file implements instruction builders corresponding to the Solend token-lending program
source at https://github.com/solendprotocol/solana-program-library/tree/mainnet/token-lending.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, List, Optional, Sequence, Union

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey


# ================================================================================
# Lending Instructions Enum (matches Solana token-lending program src/instruction.rs)
# ================================================================================


class LendingInstruction(IntEnum):
    """Instructions supported by the Solend lending program."""

    InitLendingMarket = 0
    SetLendingMarketOwner = 1
    InitReserve = 2
    RefreshReserve = 3
    DepositReserveLiquidity = 4
    RedeemReserveCollateral = 5
    InitObligation = 6
    RefreshObligation = 7
    DepositObligationCollateral = 8
    WithdrawObligationCollateral = 9
    BorrowObligationLiquidity = 10
    RepayObligationLiquidity = 11
    LiquidateObligation = 12
    FlashLoan = 13
    ModifyReserveConfig = 14


# ================================================================================
# Data Classes for Instruction Parameters
# ================================================================================


@dataclass
class ReserveConfig:
    """Reserve configuration values (packed into instruction data)."""

    optimal_utilization_rate: int
    loan_to_value_ratio: int
    liquidation_bonus: int
    liquidation_threshold: int
    min_borrow_rate: int
    optimal_borrow_rate: int
    max_borrow_rate: int
    borrow_fee_wad: int
    flash_loan_fee_wad: int
    host_fee_percentage: int

    @classmethod
    def default(cls) -> "ReserveConfig":
        """Default reserve configuration for testing."""
        return cls(
            optimal_utilization_rate=50,
            loan_to_value_ratio=1,
            liquidation_bonus=10,
            liquidation_threshold=5,
            min_borrow_rate=2,
            optimal_borrow_rate=4,
            max_borrow_rate=10,
            borrow_fee_wad=1,
            flash_loan_fee_wad=3,
            host_fee_percentage=1,
        )


# ================================================================================
# Instruction Packing and Unpacking
# ================================================================================


def pack_u64(value: int) -> bytes:
    """Pack u64 into little-endian bytes."""
    return value.to_bytes(8, "little")


def pack_u8(value: int) -> bytes:
    """Pack u8 into little-endian bytes."""
    return value.to_bytes(1, "little")


def pack_pubkey(pk: Pubkey) -> bytes:
    """Pack PublicKey into bytes."""
    return bytes(pk)


def pack_bytes32(data: Union[bytes, List[int]]) -> bytes:
    """Pack exactly 32 bytes into fixed-length buffer."""
    if isinstance(data, list):
        data = bytes(data)
    if len(data) > 32:
        raise ValueError("Expected exactly 32 bytes")
    return data.ljust(32, b"\x00")[:32]


def pack_reserve_config(config: ReserveConfig) -> bytes:
    """Pack ReserveConfig into instruction data buffer."""
    buf = bytearray()
    buf.extend(pack_u8(config.optimal_utilization_rate))
    buf.extend(pack_u8(config.loan_to_value_ratio))
    buf.extend(pack_u8(config.liquidation_bonus))
    buf.extend(pack_u8(config.liquidation_threshold))
    buf.extend(pack_u8(config.min_borrow_rate))
    buf.extend(pack_u8(config.optimal_borrow_rate))
    buf.extend(pack_u8(config.max_borrow_rate))
    buf.extend(pack_u64(config.borrow_fee_wad))
    buf.extend(pack_u64(config.flash_loan_fee_wad))
    buf.extend(pack_u8(config.host_fee_percentage))
    return bytes(buf)


def pack_instruction_data(ix: LendingInstruction, params: Any) -> bytes:
    """
    Pack instruction tag and parameters into a byte buffer.

    Parameters:
        ix: Instruction type tag (LendingInstruction)
        params: Instruction-specific parameters

    Returns:
        Packed instruction data as bytes

    Raises:
        ValueError: Invalid or missing parameters for the instruction
    """
    buf = bytearray()
    buf.append(int(ix))

    if ix == LendingInstruction.InitLendingMarket:
        owner = params["owner"]
        quote_currency = params.get("quote_currency", b"USD" + b"\x00" * 29)  # 32 bytes
        buf.extend(pack_pubkey(owner))
        buf.extend(pack_bytes32(quote_currency))

    elif ix == LendingInstruction.SetLendingMarketOwner:
        new_owner = params["new_owner"]
        buf.extend(pack_pubkey(new_owner))

    elif ix == LendingInstruction.InitReserve:
        liquidity_amount = params["liquidity_amount"]
        config = params["config"] or ReserveConfig.default()
        buf.extend(pack_u64(liquidity_amount))
        buf.extend(pack_reserve_config(config))

    elif ix == LendingInstruction.DepositReserveLiquidity:
        liquidity_amount = params["liquidity_amount"]
        buf.extend(pack_u64(liquidity_amount))

    elif ix == LendingInstruction.RedeemReserveCollateral:
        collateral_amount = params["collateral_amount"]
        buf.extend(pack_u64(collateral_amount))

    elif ix == LendingInstruction.InitObligation:
        pass  # No params

    elif ix == LendingInstruction.RefreshObligation:
        pass  # No params

    elif ix == LendingInstruction.DepositObligationCollateral:
        collateral_amount = params["collateral_amount"]
        buf.extend(pack_u64(collateral_amount))

    elif ix == LendingInstruction.WithdrawObligationCollateral:
        collateral_amount = params["collateral_amount"]
        buf.extend(pack_u64(collateral_amount))

    elif ix == LendingInstruction.BorrowObligationLiquidity:
        liquidity_amount = params["liquidity_amount"]
        slippage_limit = params.get("slippage_limit", 0)
        buf.extend(pack_u64(liquidity_amount))
        buf.extend(pack_u64(slippage_limit))

    elif ix == LendingInstruction.RepayObligationLiquidity:
        liquidity_amount = params["liquidity_amount"]
        buf.extend(pack_u64(liquidity_amount))

    elif ix == LendingInstruction.LiquidateObligation:
        liquidity_amount = params["liquidity_amount"]
        buf.extend(pack_u64(liquidity_amount))

    elif ix == LendingInstruction.FlashLoan:
        amount = params["amount"]
        buf.extend(pack_u64(amount))

    elif ix == LendingInstruction.ModifyReserveConfig:
        new_config = params["new_config"]
        buf.extend(pack_reserve_config(new_config))

    else:
        raise ValueError(f"Unknown instruction type: {ix}")

    return bytes(buf)


# ================================================================================
# Instruction Builders (directly correspond to Solend's Rust functions)
# ================================================================================

# Common program ids and sysvars
import base58

SOLEND_PROGRAM_ID = Pubkey.from_bytes(
    base58.b58decode("9xQeWvL9zG9h3gF5hV9S1aYcKX9QeR7jVvZL2b5Z9cM")
)
SPL_TOKEN_PROGRAM_ID = Pubkey.from_bytes(
    base58.b58decode("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
)
CLOCK_SYSVAR_ID = Pubkey.from_bytes(
    base58.b58decode("SysvarC1ock11111111111111111111111111111111")
)
RENT_SYSVAR_ID = Pubkey.from_bytes(
    base58.b58decode("SysvarRent111111111111111111111111111111111")
)


def refresh_reserve(
    reserve_pubkey: Pubkey,
    reserve_liquidity_oracle_pubkey: Pubkey,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Refresh an obligation's accrued interest and collateral/liquidity prices.

    Args:
        reserve_pubkey: Reserve account to refresh
        reserve_liquidity_oracle_pubkey: Pyth price oracle account
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    accounts = [
        AccountMeta(pubkey=reserve_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=reserve_liquidity_oracle_pubkey,
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
    ]
    data = pack_instruction_data(LendingInstruction.RefreshReserve, {})
    return Instruction(program_id, data, accounts)


def deposit_reserve_liquidity(
    liquidity_amount: int,
    source_liquidity_pubkey: Pubkey,
    destination_collateral_pubkey: Pubkey,
    reserve_pubkey: Pubkey,
    reserve_liquidity_supply_pubkey: Pubkey,
    reserve_collateral_mint_pubkey: Pubkey,
    lending_market_pubkey: Pubkey,
    user_transfer_authority_pubkey: Pubkey,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Deposit liquidity into a reserve in exchange for collateral tokens.

    Args:
        liquidity_amount: Amount to deposit in lamports
        source_liquidity_pubkey: Source token account of the depositor
        destination_collateral_pubkey: Destination collateral token account
        reserve_pubkey: Reserve account
        reserve_liquidity_supply_pubkey: Reserve liquidity supply
        reserve_collateral_mint_pubkey: Collateral token mint
        lending_market_pubkey: Lending market account
        user_transfer_authority_pubkey: User transfer authority
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    # Derive lending market authority via program address
    (lending_market_authority_pubkey, _bump_seed) = Pubkey.find_program_address(
        [bytes(lending_market_pubkey)], program_id
    )

    accounts = [
        AccountMeta(pubkey=source_liquidity_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=destination_collateral_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=reserve_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=reserve_liquidity_supply_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=reserve_collateral_mint_pubkey, is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=lending_market_pubkey, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=lending_market_authority_pubkey, is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=user_transfer_authority_pubkey, is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SPL_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    data = pack_instruction_data(
        LendingInstruction.DepositReserveLiquidity,
        {"liquidity_amount": liquidity_amount},
    )
    return Instruction(program_id, data, accounts)


def redeem_reserve_collateral(
    collateral_amount: int,
    source_collateral_pubkey: Pubkey,
    destination_liquidity_pubkey: Pubkey,
    reserve_pubkey: Pubkey,
    reserve_collateral_mint_pubkey: Pubkey,
    reserve_liquidity_supply_pubkey: Pubkey,
    lending_market_pubkey: Pubkey,
    user_transfer_authority_pubkey: Pubkey,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Redeem collateral from a reserve for liquidity.

    Args:
        collateral_amount: Amount of collateral to redeem
        source_collateral_pubkey: Source collateral account
        destination_liquidity_pubkey: Destination liquidity token account
        reserve_pubkey: Reserve account
        reserve_collateral_mint_pubkey: Collateral mint
        reserve_liquidity_supply_pubkey: Reserve liquidity supply
        lending_market_pubkey: Lending market
        user_transfer_authority_pubkey: User transfer authority
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    (lending_market_authority_pubkey, _bump_seed) = Pubkey.find_program_address(
        [bytes(lending_market_pubkey)], program_id
    )

    accounts = [
        AccountMeta(pubkey=source_collateral_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=destination_liquidity_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=reserve_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=reserve_collateral_mint_pubkey, is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=reserve_liquidity_supply_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=lending_market_pubkey, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=lending_market_authority_pubkey, is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=user_transfer_authority_pubkey, is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SPL_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    data = pack_instruction_data(
        LendingInstruction.RedeemReserveCollateral,
        {"collateral_amount": collateral_amount},
    )
    return Instruction(program_id, data, accounts)


def init_obligation(
    obligation_pubkey: Pubkey,
    lending_market_pubkey: Pubkey,
    obligation_owner_pubkey: Pubkey,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Initialize a new lending market obligation.

    Args:
        obligation_pubkey: Obligation account (uninitialized)
        lending_market_pubkey: Lending market account
        obligation_owner_pubkey: Owner of the new obligation
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    accounts = [
        AccountMeta(pubkey=obligation_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=lending_market_pubkey, is_signer=False, is_writable=False),
        AccountMeta(pubkey=obligation_owner_pubkey, is_signer=True, is_writable=False),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SPL_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    data = pack_instruction_data(LendingInstruction.InitObligation, {})
    return Instruction(program_id, data, accounts)


def refresh_obligation(
    obligation_pubkey: Pubkey,
    reserve_pubkeys: Sequence[Pubkey],
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Refresh an obligation's accrued interest and collateral/liquidity prices.

    Args:
        obligation_pubkey: Obligation to refresh
        reserve_pubkeys: List of collateral and liquidity reserve pubkeys
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    accounts = [
        AccountMeta(pubkey=obligation_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
    ]

    for reserve_pubkey in reserve_pubkeys:
        accounts.append(
            AccountMeta(pubkey=reserve_pubkey, is_signer=False, is_writable=False)
        )

    data = pack_instruction_data(LendingInstruction.RefreshObligation, {})
    return Instruction(program_id, data, accounts)


def deposit_obligation_collateral(
    collateral_amount: int,
    source_collateral_pubkey: Pubkey,
    destination_collateral_pubkey: Pubkey,
    deposit_reserve_pubkey: Pubkey,
    obligation_pubkey: Pubkey,
    lending_market_pubkey: Pubkey,
    obligation_owner_pubkey: Pubkey,
    user_transfer_authority_pubkey: Pubkey,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Deposit collateral into an obligation.

    Args:
        collateral_amount: Amount to deposit in lamports
        source_collateral_pubkey: Source collateral token account
        destination_collateral_pubkey: Destination collateral token account
        deposit_reserve_pubkey: Reserve account for the collateral
        obligation_pubkey: Obligation to deposit into
        lending_market_pubkey: Lending market
        obligation_owner_pubkey: Obligation owner
        user_transfer_authority_pubkey: User transfer authority
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    accounts = [
        AccountMeta(pubkey=source_collateral_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=destination_collateral_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=deposit_reserve_pubkey, is_signer=False, is_writable=False),
        AccountMeta(pubkey=obligation_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=lending_market_pubkey, is_signer=False, is_writable=False),
        AccountMeta(pubkey=obligation_owner_pubkey, is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=user_transfer_authority_pubkey, is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SPL_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    data = pack_instruction_data(
        LendingInstruction.DepositObligationCollateral,
        {"collateral_amount": collateral_amount},
    )
    return Instruction(program_id, data, accounts)


def withdraw_obligation_collateral(
    collateral_amount: int,
    source_collateral_pubkey: Pubkey,
    destination_collateral_pubkey: Pubkey,
    withdraw_reserve_pubkey: Pubkey,
    obligation_pubkey: Pubkey,
    lending_market_pubkey: Pubkey,
    obligation_owner_pubkey: Pubkey,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Withdraw collateral from an obligation.

    Args:
        collateral_amount: Amount to withdraw in lamports
        source_collateral_pubkey: Source collateral account
        destination_collateral_pubkey: Destination collateral account
        withdraw_reserve_pubkey: Reserve account
        obligation_pubkey: Obligation to withdraw from
        lending_market_pubkey: Lending market
        obligation_owner_pubkey: Obligation owner
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    (lending_market_authority_pubkey, _bump_seed) = Pubkey.find_program_address(
        [bytes(lending_market_pubkey)], program_id
    )

    accounts = [
        AccountMeta(pubkey=source_collateral_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=destination_collateral_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=withdraw_reserve_pubkey, is_signer=False, is_writable=False),
        AccountMeta(pubkey=obligation_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=lending_market_pubkey, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=lending_market_authority_pubkey, is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=obligation_owner_pubkey, is_signer=True, is_writable=False),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SPL_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    data = pack_instruction_data(
        LendingInstruction.WithdrawObligationCollateral,
        {"collateral_amount": collateral_amount},
    )
    return Instruction(program_id, data, accounts)


def borrow_obligation_liquidity(
    liquidity_amount: int,
    source_liquidity_pubkey: Pubkey,
    destination_liquidity_pubkey: Pubkey,
    borrow_reserve_pubkey: Pubkey,
    borrow_reserve_liquidity_fee_receiver_pubkey: Pubkey,
    obligation_pubkey: Pubkey,
    lending_market_pubkey: Pubkey,
    obligation_owner_pubkey: Pubkey,
    host_fee_receiver_pubkey: Optional[Pubkey] = None,
    slippage_limit: int = 0,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Borrow liquidity from a reserve.

    Args:
        liquidity_amount: Amount to borrow in lamports
        source_liquidity_pubkey: Source liquidity token account
        destination_liquidity_pubkey: Destination liquidity token account
        borrow_reserve_pubkey: Reserve to borrow from
        borrow_reserve_liquidity_fee_receiver_pubkey: Fee receiver
        obligation_pubkey: Obligation to collateralize
        lending_market_pubkey: Lending market
        obligation_owner_pubkey: Obligation owner
        host_fee_receiver_pubkey: Host fee receiver (optional)
        slippage_limit: Slippage limit for borrow
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    (lending_market_authority_pubkey, _bump_seed) = Pubkey.find_program_address(
        [bytes(lending_market_pubkey)], program_id
    )

    accounts = [
        AccountMeta(pubkey=source_liquidity_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=destination_liquidity_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=borrow_reserve_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=borrow_reserve_liquidity_fee_receiver_pubkey,
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=obligation_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=lending_market_pubkey, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=lending_market_authority_pubkey, is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=obligation_owner_pubkey, is_signer=True, is_writable=False),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SPL_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    if host_fee_receiver_pubkey is not None:
        accounts.append(
            AccountMeta(
                pubkey=host_fee_receiver_pubkey, is_signer=False, is_writable=True
            )
        )

    data = pack_instruction_data(
        LendingInstruction.BorrowObligationLiquidity,
        {
            "liquidity_amount": liquidity_amount,
            "slippage_limit": slippage_limit,
        },
    )
    return Instruction(program_id, data, accounts)


def repay_obligation_liquidity(
    liquidity_amount: int,
    source_liquidity_pubkey: Pubkey,
    destination_liquidity_pubkey: Pubkey,
    repay_reserve_pubkey: Pubkey,
    obligation_pubkey: Pubkey,
    lending_market_pubkey: Pubkey,
    user_transfer_authority_pubkey: Pubkey,
    program_id: Pubkey = SOLEND_PROGRAM_ID,
) -> Instruction:
    """
    Repay borrowed liquidity to a reserve.

    Args:
        liquidity_amount: Amount to repay in lamports
        source_liquidity_pubkey: Source liquidity token account
        destination_liquidity_pubkey: Destination liquidity token account
        repay_reserve_pubkey: Reserve being repaid
        obligation_pubkey: Obligation being repaid
        lending_market_pubkey: Lending market
        user_transfer_authority_pubkey: User transfer authority
        program_id: Solend program id

    Returns:
        Solders Instruction
    """
    accounts = [
        AccountMeta(pubkey=source_liquidity_pubkey, is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=destination_liquidity_pubkey, is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=repay_reserve_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=obligation_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=lending_market_pubkey, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=user_transfer_authority_pubkey, is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=CLOCK_SYSVAR_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SPL_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    data = pack_instruction_data(
        LendingInstruction.RepayObligationLiquidity,
        {"liquidity_amount": liquidity_amount},
    )
    return Instruction(program_id, data, accounts)


# ================================================================================
# Test Helpers
# ================================================================================


def test_instruction_packing() -> None:
    """Quick validation test for instruction packing/unpacking."""
    from random import randint
    from solders.pubkey import Pubkey

    # Test DepositReserveLiquidity (tag 4)
    amount = randint(1, 1000000)
    data = pack_instruction_data(
        LendingInstruction.DepositReserveLiquidity, {"liquidity_amount": amount}
    )
    assert len(data) > 1
    assert data[0] == LendingInstruction.DepositReserveLiquidity

    # Test BorrowObligationLiquidity (tag 10)
    data = pack_instruction_data(
        LendingInstruction.BorrowObligationLiquidity,
        {
            "liquidity_amount": 100000,
            "slippage_limit": 100,
        },
    )
    assert data[0] == LendingInstruction.BorrowObligationLiquidity
    assert int.from_bytes(data[1:9], "little") == 100000
    assert int.from_bytes(data[9:17], "little") == 100

    print("All packing tests passed")


if __name__ == "__main__":
    test_instruction_packing()
