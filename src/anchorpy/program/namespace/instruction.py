import itertools
from typing import Callable, List, Any, Sequence, cast, Tuple

from solana.transaction import TransactionInstruction, AccountMeta

from anchorpy.program.common import (
    to_instruction,
    validate_accounts,
    translate_address,
    InstructionToSerialize,
)
from anchorpy.program.context import split_args_and_context, Accounts
from solana.publickey import PublicKey
from anchorpy.idl import IdlInstruction, IdlAccountItem, IdlAccounts, IdlAccount

InstructionEncodeFn = Callable[[str, str], List[bytes]]

InstructionFn = Callable[[Any], Any]


def build_instruction_fn(  # ts: InstructionNamespaceFactory.build
    idl_ix: IdlInstruction,
    encode_fn: Callable[[InstructionToSerialize], bytes],
    program_id: PublicKey,
) -> InstructionFn:
    if idl_ix.name == "_inner":
        raise ValueError("_inner name is reserved")

    def instruction_method(*args) -> TransactionInstruction:
        def accounts(accs: Accounts) -> List[AccountMeta]:
            return accounts_array(accs, idl_ix.accounts)

        split_args, ctx = split_args_and_context(idl_ix, args)
        validate_accounts(idl_ix.accounts, ctx.accounts)
        validate_instruction(idl_ix, split_args)

        keys = accounts(ctx.accounts)
        if ctx.remaining_accounts:
            keys.extend(ctx.remaining_accounts)
        return TransactionInstruction(
            keys=keys,
            program_id=program_id,
            data=encode_fn(to_instruction(idl_ix, split_args)),
        )

    return instruction_method


def accounts_array(
    ctx: Accounts, accounts: Sequence[IdlAccountItem]
) -> List[AccountMeta]:
    accounts_ret: List[AccountMeta] = []
    for acc in accounts:
        if isinstance(acc, IdlAccounts):
            rpc_accs = cast(Accounts, ctx[acc.name])
            acc_arr = accounts_array(rpc_accs, acc.accounts)
            to_add: List[AccountMeta] = list(
                itertools.chain.from_iterable(acc_arr),  # type: ignore
            )
            accounts_ret.extend(to_add)
        else:
            account: IdlAccount = acc
            accounts_ret.append(
                AccountMeta(
                    pubkey=translate_address(ctx[account.name]),
                    is_writable=account.is_mut,
                    is_signer=account.is_signer,
                )
            )
    return accounts_ret


def validate_instruction(ix: IdlInstruction, args: Tuple):
    # TODO
    pass