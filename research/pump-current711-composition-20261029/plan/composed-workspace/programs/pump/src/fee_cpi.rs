use anchor_lang::prelude::*;

use crate::trade_types::{BondingCurve, Fees};
use anchor_spl::token_interface::Mint;

// buy_quote lives in lib.rs (the original's bonding-curve math region); re-exported for the legacy callers.
pub use crate::buy_quote;

/// Shared fee query and accounting. Account clones are created here before
/// the fallible market-cap calculation, as in the original outer helper.
pub fn trade_fees<'info>(
    global: &Account<'info, crate::Global>,
    curve: &Account<'info, BondingCurve>,
    mint: &InterfaceAccount<'info, Mint>,
    fee_config: &Account<'info, super::LegacyFeeConfig>,
    fee_program: &Program<'info, super::LegacyFeesProgram>,
    program: &AccountInfo<'info>,
    quote_amount: u64,
) -> Result<(u64, u64, u64, u64)> {
    let fees = get_fees_with_quote_mint(CpiContext::new(
        fee_program.to_account_info(),
        GetFeesWithQuoteMint {
            fee_config: fee_config.to_account_info(),
            config_program_id: program.clone(),
        },
    ),
    true, crate::buy_fee_market_cap(curve, mint)?, curve.quote_mint)?.get();

    let (protocol_fee_bps, creator_fee_bps) = (fees.protocol_fee_bps, fees.creator_fee_bps);
    let creator_fee_bps = if global.creator_fee_configurable && curve.creator_fee_bps != 0 { curve.creator_fee_bps } else { creator_fee_bps };
    let protocol_fee = fee(quote_amount, protocol_fee_bps)?;
    let creator_fee = if curve.creator != Pubkey::default() { fee(quote_amount, creator_fee_bps)? } else { 0 };







    return Ok((protocol_fee, creator_fee, protocol_fee_bps, creator_fee_bps));
}

pub use super::fee_math::{checked_ceil_div, fee};













// Keep existing caller paths while using the root external-interface API.
pub(crate) use crate::pump_fees::cpi::accounts::GetFeesWithQuoteMint;
pub use crate::pump_fees::cpi::{get_fees_with_quote_mint, Return};
