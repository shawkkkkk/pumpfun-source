use anchor_lang::prelude::*;
use crate::{AdminGlobal, AdminReadonly, PumpError, ReservedFeeRecipientsEvent};
use anchor_lang::error::ErrorCode;



































pub fn set_reserved_fee_recipients(ctx: Context<AdminReadonly>, whitelist_pda: Pubkey) -> Result<()> {
    require_gte!(ctx.remaining_accounts.len(), 8, PumpError::NotEnoughRemainingAccounts);
    let global = &mut ctx.accounts.global;













    let recipients: [Pubkey; 8] = ctx.remaining_accounts[..8].iter().map(|account| account.key()).collect::<Vec<Pubkey>>().try_into().unwrap();
    let reserved_fee_recipient = recipients[0];
    let reserved_fee_recipients: [Pubkey; 7] = recipients[1..].try_into().unwrap();
    let rent = Rent::get()?;
    for (index, account) in ctx.remaining_accounts[..8].iter().enumerate() {
        require_keys_neq!(account.key(), Pubkey::default(), PumpError::AllFeeRecipientsShouldBeNonZero);
        if account.executable {
            return Err(Error::from(ErrorCode::ConstraintExecutable).with_account_name(format!("reserved_fee_recipients[{}]", index)));
        }
        if !rent.is_exempt(account.lamports(), account.try_data_len()?) {
            return Err(crate::account_name::with_owned_name(Error::from(ErrorCode::ConstraintRentExempt), &format!("reserved_fee_recipients[{}]", index)));
        }
    }
    // global was bound before key collection so its account pointer is live across the allocator
    global.whitelist_pda = whitelist_pda;
    global.reserved_fee_recipient = reserved_fee_recipient;
    global.reserved_fee_recipients = reserved_fee_recipients;
    let event = ReservedFeeRecipientsEvent {
        timestamp: Clock::get()?.unix_timestamp,
        reserved_fee_recipient: global.reserved_fee_recipient,
        reserved_fee_recipients: global.reserved_fee_recipients,
    };
    emit!(event);
    emit_cpi!(event);
    return Ok(());
}




























pub fn update_buyback_config(ctx: Context<AdminGlobal>, buyback_basis_points: Option<u64>) -> Result<()> {
    let global = &mut ctx.accounts.global;
    if let Some(value) = buyback_basis_points {
        global.set_buyback_basis_points(value)?;
    }
    let ra = ctx.remaining_accounts;
    match ra.len() {
        0 => {}
        8 => {
            let recipients = [ra[0].key(), ra[1].key(), ra[2].key(), ra[3].key(), ra[4].key(), ra[5].key(), ra[6].key(), ra[7].key()];
            global.set_buyback_fee_recipients(recipients)?;
        }
        _ => return err!(PumpError::WrongBuybackFeeRecipientsCount),
    }
    Ok(())
}
