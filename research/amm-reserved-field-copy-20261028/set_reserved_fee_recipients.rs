use crate::*;

/// One primary reserved fee recipient plus seven additional ones.
pub const RESERVED_FEE_RECIPIENTS_LEN: usize = 8;

#[event_cpi]
#[derive(Accounts)]
pub struct SetReservedFeeRecipients<'info> {
    #[account(
        mut,
        seeds = [b"global_config"],
        bump,
        has_one = admin @ PumpAmmError::InvalidAdmin,
    )]
    pub global_config: Account<'info, GlobalConfig>,

    pub admin: Signer<'info>,
}

/// Sets the reserved fee recipients and the whitelist PDA.
///
/// The reserved fee recipients are passed as the first
/// `RESERVED_FEE_RECIPIENTS_LEN` remaining accounts. The first one becomes
/// `GlobalConfig::reserved_fee_recipient`, the other seven become
/// `GlobalConfig::reserved_fee_recipients`.
///
/// Every recipient must be a non-default, non-executable, rent exempt
/// account so that fee transfers to it can never fail.
pub fn handler(ctx: Context<SetReservedFeeRecipients>, whitelist_pda: Pubkey) -> Result<()> {
    let remaining_accounts = ctx.remaining_accounts;

    // remaining_accounts:
    //   [0]    reserved_fee_recipient
    //   [1..8] reserved_fee_recipients
    //
    // Any further remaining accounts are ignored. The admin is trusted to
    // pass distinct accounts; duplicates are not rejected, they only reduce
    // the number of distinct reserved fee recipients the trade instructions
    // can pick from.
    require_gte!(
        remaining_accounts.len(),
        RESERVED_FEE_RECIPIENTS_LEN,
        PumpAmmError::NotEnoughRemainingAccounts
    );
    let global_config = &mut ctx.accounts.global_config;
    let recipients: [Pubkey; RESERVED_FEE_RECIPIENTS_LEN] = remaining_accounts[..RESERVED_FEE_RECIPIENTS_LEN]
        .iter()
        .map(|account| account.key())
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
    let reserved_fee_recipients: [Pubkey; 7] = recipients[1..].try_into().unwrap();

    let rent = Rent::get()?;

    for (i, account) in remaining_accounts[..RESERVED_FEE_RECIPIENTS_LEN]
        .iter()
        .enumerate()
    {
        require_keys_neq!(
            account.key(),
            Pubkey::default(),
            PumpAmmError::AllProtocolFeeRecipientsShouldBeNonZero
        );
        if account.executable {
            return Err(Error::from(ErrorCode::ConstraintExecutable)
                .with_account_name(format!("reserved_fee_recipients[{}]", i)));
        }
        if unlikely(!rent.is_exempt(account.lamports(), account.try_data_len()?)) {
            return Err(Error::from(ErrorCode::ConstraintRentExempt)
                .with_account_name(format!("reserved_fee_recipients[{}]", i)));
        }
    }

    global_config.whitelist_pda = whitelist_pda;
    copy_parts(&mut global_config.reserved_fee_recipient, &recipients[0]);
    global_config.reserved_fee_recipients = reserved_fee_recipients;

    let event = ReservedFeeRecipientsEvent {
        timestamp: Clock::get()?.unix_timestamp,
        reserved_fee_recipient: global_config.reserved_fee_recipient,
        reserved_fee_recipients: global_config.reserved_fee_recipients,
    };
    emit!(event);
    emit_cpi!(event);

    Ok(())
}


#[inline]
#[cold]
fn cold() {}

#[inline]
fn unlikely(b: bool) -> bool {
    if b {
        cold();
    }
    b
}

#[inline(always)]
fn copy_parts(dst: &mut Pubkey, src: &Pubkey) {
    unsafe {
        let s = src as *const Pubkey as *const u8;
        let d = dst as *mut Pubkey as *mut u8;
        core::ptr::write_unaligned(d as *mut u16, core::ptr::read_unaligned(s as *const u16));
        core::ptr::write_unaligned(d.add(2), s.add(2).read());
        core::ptr::write_unaligned(d.add(3) as *mut u32, core::ptr::read_unaligned(s.add(3) as *const u32));
        core::ptr::write_unaligned(d.add(7) as *mut u64, core::ptr::read_unaligned(s.add(7) as *const u64));
        core::ptr::write_unaligned(d.add(15) as *mut u64, core::ptr::read_unaligned(s.add(15) as *const u64));
        core::ptr::write_unaligned(d.add(23) as *mut u64, core::ptr::read_unaligned(s.add(23) as *const u64));
        core::ptr::write_unaligned(d.add(31), s.add(31).read());
    }
}
