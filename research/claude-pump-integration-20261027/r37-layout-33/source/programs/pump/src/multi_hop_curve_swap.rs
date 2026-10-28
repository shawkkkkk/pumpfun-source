//! Reconstructed multi-hop curve trading.
//! Signed original-runtime probes cover ordinary trades, completion, and quote adapters.
use anchor_lang::prelude::*;
use anchor_lang::solana_program::{instruction::{Instruction,AccountMeta},program::{invoke,invoke_signed},program_error::ProgramError};
use anchor_spl::{token::Token,token_2022::Token2022,token_interface::{Mint,TokenAccount}};
use crate::{Global,PumpError};
use crate::trade_types::{BondingCurve,FeeConfig,FeeTier,Fees,TradeEvent};
const FEES:Pubkey=anchor_lang::solana_program::pubkey!("pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ");
const AMM:Pubkey=anchor_lang::solana_program::pubkey!("pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA");
const WSOL:Pubkey=anchor_spl::token::spl_token::native_mint::ID;
#[derive(Accounts)]
pub struct MultiHopCurve<'info>{
 #[account(seeds=[b"global"],bump)]pub global:Box<Account<'info,Global>>,
 #[account(seeds=[b"fee_config",crate::ID.as_ref()],bump=fee_config.0.bump,seeds::program=FEES)]pub fee_config:Box<Account<'info,RouteFeeConfig>>,
 #[account(seeds=[b"global_config"],bump,seeds::program=AMM)]pub pump_amm_global_config:Signer<'info>,
 #[account(mut)]pub user:Signer<'info>,
 pub source_authority:Signer<'info>,
 #[account(mut)]pub source:Box<InterfaceAccount<'info,TokenAccount>>,
 #[account(mut)]pub destination:Box<InterfaceAccount<'info,TokenAccount>>,
 /// CHECK: Slot 7 is writable raw AccountInfo; no local owner/mint/membership constraint.
 #[account(mut)]pub buyback_fee_recipient:UncheckedAccount<'info>,
 pub token_program:Program<'info,Token>,
 pub token_2022_program:Program<'info,Token2022>,
 pub system_program:Program<'info,System>,
 /// CHECK: event-signing PDA.
 #[account(seeds=[b"__event_authority"],bump)]
 pub event_authority:AccountInfo<'info>,
 pub program:Program<'info,crate::program::PumpRecovered>,
}
#[derive(Accounts)]
pub struct CurveHop<'info>{
 pub base_mint:Box<InterfaceAccount<'info,Mint>>,
 pub quote_mint:Box<InterfaceAccount<'info,Mint>>,
 #[account(mut,seeds=[b"bonding-curve",base_mint.key().as_ref()],bump,
 constraint=quote_mint.key()==bonding_curve.quote_mint || (bonding_curve.quote_mint==Pubkey::default() && quote_mint.key()==WSOL) @ PumpError::MintDoesNotMatchBondingCurve)]
 pub bonding_curve:Box<Account<'info,BondingCurve>>,
 #[account(mut)]pub associated_base_bonding_curve:Box<InterfaceAccount<'info,TokenAccount>>,
 /// CHECK: Address and native quote branch checked before transfer.
 #[account(mut)]pub associated_quote_bonding_curve:UncheckedAccount<'info>,
}
#[derive(AnchorSerialize,AnchorDeserialize,Clone)]
pub struct CurveRunResult{pub amount_out:u64,pub buyback_fee:u64}

// D01: Decode every field before context PDA constraints and handler shape checks.
// Keep the decoded vectors; account length controls selection, never decoding.
#[derive(Clone)]
pub struct RouteFeeConfig(pub FeeConfig);
impl Owner for RouteFeeConfig { fn owner() -> Pubkey { FEES } }
impl AccountSerialize for RouteFeeConfig {}
impl AccountDeserialize for RouteFeeConfig {
    fn try_deserialize(buf: &mut &[u8]) -> Result<Self> {
        if buf.len() < 8 { return err!(anchor_lang::error::ErrorCode::AccountDiscriminatorNotFound); }
        if buf[..8] != [143,52,146,187,219,123,76,155] {
            return err!(anchor_lang::error::ErrorCode::AccountDiscriminatorMismatch);
        }
        Self::try_deserialize_unchecked(buf)
    }
    fn try_deserialize_unchecked(buf: &mut &[u8]) -> Result<Self> {
        let mut cursor = buf.get(8..).ok_or_else(|| error!(anchor_lang::error::ErrorCode::AccountDidNotDeserialize))?;
        FeeConfig::deserialize(&mut cursor).map(Self)
            .map_err(|_| error!(anchor_lang::error::ErrorCode::AccountDidNotDeserialize))
    }
}
fn add(a: u64, b: u64) -> Result<u64> { a.checked_add(b).ok_or(error!(PumpError::Overflow)) }
fn sub(a: u64, b: u64) -> Result<u64> { a.checked_sub(b).ok_or(error!(PumpError::Overflow)) }
fn n(a: u128) -> Result<u64> { u64::try_from(a).map_err(|_| error!(PumpError::Truncation)) }
fn div(a: u128, b: u128) -> Result<u128> {
    a.checked_div(b).ok_or(error!(PumpError::DivisionByZero))
}
fn fee(a: u64, b: u64) -> Result<u64> { n((a as u128 * b as u128 + 9999) / 10000) }

// D02: First-threshold gate before reverse search matters for unsorted tables.
fn tier(tiers: &[FeeTier], cap: u128) -> Result<Fees> {
    let first = tiers.first().ok_or(error!(PumpError::FeeTiersEmpty))?;
    if cap < first.market_cap_lamports_threshold { return Ok(first.fees.clone()); }
    Ok(tiers.iter().rev().find(|t| t.market_cap_lamports_threshold <= cap)
        .unwrap_or(first).fees.clone())
}
struct SelectedFees { protocol: u64, creator: u64, rates: Fees }
fn select_fees(a: &MultiHopCurve, c: &BondingCurve, cap: u128, amount: u64) -> Result<SelectedFees> {
    let len = a.fee_config.to_account_info().data_len();
    require!(len >= 2512, PumpError::FeeConfigTooShort);
    let config = &a.fee_config.0;
    // Exact selector constants, descriptive labels only; emitted from sealed bytes.
    let quote = c.quote_mint;
    let mut rates = if quote == Pubkey::default() || quote == QUOTE_1 || quote == QUOTE_2 {
        tier(&config.fee_tiers, cap)?
    } else if quote == QUOTE_STABLE {
        tier(if len > 4072 { &config.stable_fee_tiers } else { &[] }, cap)?
    } else if len > 4096 && (config.exotic_flat_fees.lp_fee_bps != 0
        || config.exotic_flat_fees.protocol_fee_bps != 0 || config.exotic_flat_fees.creator_fee_bps != 0) {
        config.exotic_flat_fees.clone()
    } else { config.flat_fees.clone() };
    if a.global.creator_fee_configurable && c.creator_fee_bps != 0 {
        rates.creator_fee_bps = c.creator_fee_bps;
    }
    // Both selector amounts are evaluated BEFORE the route's masks, also on buys.
    let protocol = fee(amount, rates.protocol_fee_bps)?;
    let creator = if c.creator == Pubkey::default() { 0 } else { fee(amount, rates.creator_fee_bps)? };
    Ok(SelectedFees { protocol, creator, rates })
}

// A01: The corrected estimate is checked but not used as the route's net quote.
fn buy_budget(budget: u64, p: u64, requested_c: u64, creator: Pubkey) -> Result<(u64,u64)> {
    let c = if creator == Pubkey::default() { 0 } else { requested_c };
    let sum = p.checked_add(c).ok_or(PumpError::Overflow)?;
    let mut estimate = if sum == 0 { budget } else { n(budget as u128 * 10000 / (10000 + sum as u128))? };
    require_gt!(estimate,0,PumpError::BuyNotEnoughSolToCoverFees);
    let pf = fee(estimate, p)?;
    let cf = fee(estimate, c)?;
    let total = estimate.saturating_add(pf).saturating_add(cf);
    if total > budget {
        estimate = sub(estimate, total - budget)?;
        require_gt!(estimate,0,PumpError::BuySlippageBelowMinTokensOut);
    }
    Ok((pf,cf))
}

// T01: Exact four AccountInfos; program identity is in the instruction.
#[inline(always)] fn transfer_tokens<'info>(program: &AccountInfo<'info>, from: &impl ToAccountInfo<'info>, to: &AccountInfo<'info>, authority: &impl ToAccountInfo<'info>,
    mint: &AccountInfo<'info>, amount: u64, decimals: u8, seeds: &[&[&[u8]]]) -> Result<()> {
    if amount == 0 { return Ok(()); }
    anchor_spl::token_2022::transfer_checked(CpiContext::new_with_signer(program.clone(), anchor_spl::token_2022::TransferChecked { from: from.to_account_info(), to: to.clone(), authority: authority.to_account_info(), mint: mint.clone() }, seeds), amount, decimals)
}



pub struct PreviousHop<'info> {
    base_mint: Pubkey,
    output_vault: AccountInfo<'info>,
    authority: AccountInfo<'info>,
    bump: u8,
}
pub fn transfer_input<'info>(a: &MultiHopCurve<'info>, previous: Option<&PreviousHop<'info>>, token_program: &AccountInfo<'info>, to: &AccountInfo<'info>, decimals: u8, mint: &AccountInfo<'info>, amount: u64) -> Result<()> {
    match previous {
        None => {
            transfer_tokens(token_program, &*a.source, to, &a.source_authority, mint, amount, decimals, &[])
        }
        Some(p) => {
            if p.output_vault.key() == to.key() { return Ok(()); }
            transfer_tokens(token_program, &p.output_vault, to, &p.authority, mint, amount, decimals, &[&[b"bonding-curve", p.base_mint.as_ref(), &[p.bump]]])
        }
    }
}



// V01: Address before owner/data checks; zero stored quote skips quote data admission.
fn admit_vaults(h: &CurveHop, require_ata: fn(&Pubkey,&Pubkey,&Pubkey,&Pubkey)->Result<()>) -> Result<()> {
    for (vault,mint,token_program) in [(h.associated_base_bonding_curve.key(),h.base_mint.key(),*h.base_mint.to_account_info().owner),(h.associated_quote_bonding_curve.key(),h.quote_mint.key(),*h.quote_mint.to_account_info().owner)] {
        require_ata(&vault,&h.bonding_curve.key(),&mint,&token_program)?;


    }
    if h.bonding_curve.quote_mint != Pubkey::default() {
        let info = h.associated_quote_bonding_curve.to_account_info();
        if info.owner == &anchor_lang::system_program::ID {
            return err!(anchor_lang::error::ErrorCode::AccountNotInitialized);
        }
        require_keys_eq!(*info.owner,*h.quote_mint.to_account_info().owner,PumpError::AccountTypeNotSupported);
        let data = info.try_borrow_data()?;
        let token = TokenAccount::try_deserialize(&mut &data[..])?;
        require_keys_eq!(token.mint,h.quote_mint.key(),PumpError::MintDoesNotMatchBondingCurve);
        // No token.authority == curve test: canonical address alone is the local relation.
    }
    Ok(())
}
























// N01: Native interface hypotheses use pinned SDK APIs, not newly recovered processors.
fn prepare_curve<'info>(a: &MultiHopCurve<'info>, h: &CurveHop<'info>) -> Result<()> {
    crate::trade_types::prepare_bonding_curve(&h.bonding_curve, &a.system_program, &a.user)
}
fn move_lamports(from: &AccountInfo, to: &AccountInfo, amount: u64) -> Result<()> {
    if amount == 0 { return Ok(()); }
    let source = from.lamports();
    // Original raw ...0017 is ArithmeticOverflow; outer formatted error data is unproved.
    let debit = source.checked_sub(amount).ok_or(ProgramError::ArithmeticOverflow)?;
    **from.try_borrow_mut_lamports()? = debit;
    // Source borrow is dropped before this read, including when handles alias.
    let credit = to.lamports().checked_add(amount).ok_or(ProgramError::ArithmeticOverflow)?;
    **to.try_borrow_mut_lamports()? = credit;
    Ok(())
}
pub fn native_buyback<'info>(a: &MultiHopCurve<'info>, event_bump: u8, curve: &Account<'info, BondingCurve>, amount: u64) -> Result<()> {
    if amount == 0 { return Ok(()); }
    let to = a.buyback_fee_recipient.to_account_info();
    let curve_info = curve.to_account_info();
    crate::trade::quote_payments::transfer_native(curve, to.clone(), amount)?;
    invoke_signed(&Instruction { program_id: crate::ID, accounts: vec![AccountMeta::new_readonly(a.event_authority.key(), true), AccountMeta::new(curve_info.key(), false), AccountMeta::new(to.key(), false)], data: anchor_lang::event::EVENT_IX_TAG_LE.to_vec() },
        &[a.event_authority.to_account_info(), curve_info, to.clone()], &[&[b"__event_authority", &[event_bump]]])?;
    invoke(&anchor_spl::token::spl_token::instruction::sync_native(&anchor_spl::token::spl_token::id(), to.key)?, &[to])?;
    Ok(())
}






fn route_event<E: anchor_lang::Event>(a: &MultiHopCurve, event: &E, event_bump: u8) -> Result<()> {
    let data = anchor_lang::Event::data(event);
    anchor_lang::solana_program::log::sol_log_data(&[&data]);
    let authority = a.event_authority.to_account_info();
    let mut payload = vec![228,69,165,46,81,203,154,29];
    payload.extend_from_slice(&anchor_lang::Event::data(event));
    let bump = [event_bump];
    invoke_signed(&Instruction { program_id: crate::ID,
        accounts: vec![AccountMeta::new_readonly(authority.key(),true)], data: payload },
        &[authority],&[&[b"__event_authority",&bump]])?;
    Ok(())
}

struct PostCompleteFill {
    base: u64,
    quote: u64,
    protocol: u64,
    creator: u64,
    pool_base: u64,
    pool_quote: u64,
}

// S01: General iteration; fee flags and last-hop transfer are independent.
pub fn execute<'info>(ctx: Context<'_,'_,'info,'info,MultiHopCurve<'info>>,
    amount_in: u64, hop_fees: Vec<u8>) -> Result<CurveRunResult> {
    require!(amount_in > 0,PumpError::BuyZeroAmount);
    require!(ctx.remaining_accounts.len() >= 5 && ctx.remaining_accounts.len() % 5 == 0,
        PumpError::NotEnoughRemainingAccounts);
    let count = ctx.remaining_accounts.len()/5;
    require!(hop_fees.len() == count && hop_fees.iter().all(|f| *f < 4),PumpError::MultiHopHopFeesMismatch);
    let a = &ctx.accounts;
    let mut remaining = ctx.remaining_accounts;
    let mut current_mint = a.source.mint;
    let mut amount = amount_in;
    let mut total_buyback = 0u64;
    let mut previous = None;
    for (index,flag) in hop_fees.iter().copied().enumerate() { let overflow=||error!(PumpError::Overflow);
        let mut bumps = CurveHopBumps::default();
        let mut h = CurveHop::try_accounts(&crate::ID,&mut remaining,&[],&mut bumps,
            &mut std::collections::BTreeSet::new())?;
        prepare_curve(a,&h)?;
        crate::trade::validate_trade(h.bonding_curve.complete as u8,h.bonding_curve.is_cashback_coin as u64,(flag & 2 == 0) as u64)?;
// layout-pad(219): aligns the next Source site with the original line























        fn pool_before(global: &Global, curve: &BondingCurve, curve_base: u64, is_sol: bool, amount: u64, quote: u64) -> Result<(u64, u64)> { crate::trade::v3_pool_before(curve.real_quote_reserves, global.pool_migration_fee, curve_base, is_sol, amount, quote) }
        #[inline(never)]
        fn complete_fill(global: &Global, fee_config: &FeeConfig, fee_config_len: usize, market_cap: u128,
            bonding_curve: &Account<BondingCurve>, associated_base_bonding_curve: &Box<InterfaceAccount<TokenAccount>>, flag: u8,
            protocol_fee_bps: u64, creator_fee_bps: u64, budget: u64) -> Result<Option<(crate::trade::TradeFees, u64, crate::trade::PostComplete)>> {
            let quote = u64::try_from(crate::buy_quote(bonding_curve, bonding_curve.real_token_reserves)?)
                .map_err(|_| error!(PumpError::Truncation))?;
            let fees = crate::legacy_sell::fee_math::get_fees(global, bonding_curve, fee_config, fee_config_len, market_cap, quote)?;
            let fees = crate::trade::TradeFees {
                protocol_fee: if flag & 1 != 0 { fees.protocol_fee } else { 0 },
                creator_fee: if flag & 2 != 0 { fees.creator_fee } else { 0 },
                protocol_fee_bps: if flag & 1 != 0 { fees.protocol_fee_bps } else { 0 },
                creator_fee_bps: if flag & 2 != 0 { fees.creator_fee_bps } else { 0 } };
            let total = crate::trade::add3(quote, fees.protocol_fee, fees.creator_fee)?;
            let remaining = match budget.checked_sub(total) { Some(r) if r > 0 => r, _ => return Ok(None) };

            let (pool_base, pool_quote) = pool_before(global, bonding_curve,
                associated_base_bonding_curve.amount, bonding_curve.quote_mint == Pubkey::default(), bonding_curve.real_token_reserves, quote)?;
            Ok(crate::trade::estimate_post_complete(&bonding_curve.creator, pool_base, pool_quote, protocol_fee_bps, creator_fee_bps,
                remaining, true)?.map(|post| (fees, quote, post)))
        }











































        #[inline(never)]
        fn token_program_for<'info>(token_program: &AccountInfo<'info>, token_2022_program: &AccountInfo<'info>,
            mint: &AccountInfo<'info>) -> Result<AccountInfo<'info>> {
            let owner = mint.to_account_info().owner;
            if owner == &anchor_spl::token_2022::ID { return Ok(token_2022_program.to_account_info()); }
            if owner == &anchor_spl::token::ID { return Ok(token_program.to_account_info()); }
            err!(PumpError::AccountTypeNotSupported)
        }






        #[inline(never)]
        fn require_ata(key:&Pubkey,owner:&Pubkey,mint:&Pubkey,program:&Pubkey)->Result<()>{
            require_keys_eq!(*key,anchor_spl::associated_token::get_associated_token_address_with_program_id(owner,mint,program),anchor_lang::error::ErrorCode::ConstraintSeeds);
            Ok(())
        }












































































































        let stepped=run_curve(a,&mut h,flag,index,count,current_mint,amount,previous,total_buyback,bumps,ctx.bumps.event_authority,overflow)?;
        current_mint=stepped.0;amount=stepped.1;previous=stepped.2;total_buyback=stepped.3;
        #[inline(never)]
        fn run_curve<'info>(a:&MultiHopCurve<'info>,h:&mut CurveHop<'info>,flag:u8,index:usize,count:usize,mut current_mint:Pubkey,mut amount:u64,mut previous:Option<PreviousHop<'info>>,mut total_buyback:u64,bumps:CurveHopBumps,event_bump:u8,overflow:fn()->anchor_lang::error::Error)->Result<(Pubkey,u64,Option<PreviousHop<'info>>,u64)>{
        require!(!h.bonding_curve.is_mayhem_mode,PumpError::MultiHopMayhemCurveNotSupported);
        let base_token_program = token_program_for(&a.token_program, &a.token_2022_program, h.base_mint.as_ref().as_ref())?; let quote_token_program = token_program_for(&a.token_program, &a.token_2022_program, h.quote_mint.as_ref().as_ref())?; require_ata(&h.associated_base_bonding_curve.key(),&h.bonding_curve.key(),&h.base_mint.key(),h.base_mint.to_account_info().owner)?; require_ata(&h.associated_quote_bonding_curve.key(),&h.bonding_curve.key(),&h.quote_mint.key(),h.quote_mint.to_account_info().owner)?; crate::buy_v2::admit_associated_token_account(h.associated_quote_bonding_curve.as_ref(),&h.bonding_curve.to_account_info(),h.quote_mint.key(),*h.quote_mint.to_account_info().owner,h.quote_mint.as_ref().as_ref(),&quote_token_program,false,a.user.as_ref(),a.system_program.as_ref())?;
        if flag & 1 != 0 {
            crate::trade::validate_buyback_fee_recipient_account(&a.global,&a.buyback_fee_recipient.to_account_info(),false,
                &h.quote_mint.key(),h.quote_mint.to_account_info().owner)?;
        }
        let buy = current_mint == h.quote_mint.key();
// layout-pad(55): aligns the next Source site with the original line






















































        require!(buy || current_mint == h.base_mint.key(),PumpError::MultiHopDiscontinuousPath);
        let last = index == count - 1;
        let native = h.bonding_curve.quote_mint == Pubkey::default();
        let c = &h.bonding_curve;
        let trade_amount = if buy && !native {
            sub(amount,crate::trade::quote_transfer_fee(&h.quote_mint.to_account_info(),amount,false)?)?
        }else{amount};
// layout-pad(18): aligns the next Source site with the original line

















        let buy_transfer_fee = amount.checked_sub(trade_amount).ok_or_else(|| error!(PumpError::Overflow))?;
        let cap = div(h.base_mint.supply as u128 * c.virtual_quote_reserves as u128,
            c.virtual_token_reserves as u128)?;
        let mut post_fill = None;
        let (p_rate,c_rate,base_amount,quote_amount,pf,cf,raw_output) = if buy {
            let fees = crate::legacy_sell::fee_math::get_fees(&a.global,c,&a.fee_config.0,a.fee_config.to_account_info().data_len(),cap,trade_amount)?;
            let p_rate = if flag & 1 != 0 { fees.protocol_fee_bps } else { 0 };
            let c_rate = if flag & 2 != 0 { fees.creator_fee_bps } else { 0 };
            let (pf,cf) = buy_budget(trade_amount,p_rate,c_rate,c.creator)?;
            let q = sub(sub(trade_amount,pf)?,cf)?;
            require!(q != 0,PumpError::Overflow);
            let effective = q - 1;
// layout-pad(6): aligns the next Source site with the original line





            let base = u64::try_from(div(effective as u128 * c.virtual_token_reserves as u128, c.virtual_quote_reserves as u128 + effective as u128)?).map_err(|_| error!(PumpError::Truncation))?;
            require_gt!(base,0,PumpError::BuyZeroAmount);
            let capped = base.min(c.real_token_reserves);
            if base > c.real_token_reserves {
                if let Some((fees, quote, post)) = complete_fill(&a.global,&a.fee_config.0,a.fee_config.to_account_info().data_len(),cap,c,
                    &h.associated_base_bonding_curve,flag,p_rate,c_rate,trade_amount)? {
                    
                    post_fill=Some(PostCompleteFill { base:post.base_out,quote:post.quote_in,
                        protocol:post.fees.protocol_fee,creator:post.fees.creator_fee,pool_base:post.pool_base_before,pool_quote:post.pool_quote_before });


























                    (p_rate,c_rate,capped,quote,fees.protocol_fee,fees.creator_fee,capped.checked_add(post.base_out).ok_or_else(|| error!(PumpError::Overflow))?)
                }else{(p_rate,c_rate,capped,q,pf,cf,capped)}
            }else{(p_rate,c_rate,base,q,pf,cf,base)}
// layout-pad(45): aligns the next Source site with the original line












































        } else {
            let gross_sell = u64::try_from(c.sell_quote(amount)?).map_err(|_| error!(PumpError::Truncation))?;
            let fees = crate::legacy_sell::fee_math::get_fees(&a.global,c,&a.fee_config.0,a.fee_config.to_account_info().data_len(),cap,gross_sell)?;
            let p_rate = if flag & 1 != 0 { fees.protocol_fee_bps } else { 0 };
            let c_rate = if flag & 2 != 0 { fees.creator_fee_bps } else { 0 };
            let pf = if flag & 1 != 0 { fees.protocol_fee } else { 0 };
            let cf = if flag & 2 != 0 { fees.creator_fee } else { 0 };
            let net = sub(sub(gross_sell,pf)?,cf)?;
// layout-pad(6): aligns the next Source site with the original line





            require_gt!(net,0,PumpError::SellZeroAmount);
            (p_rate,c_rate,amount,gross_sell,pf,cf,net)
        };
        let output = if !buy && !native {
            sub(raw_output,crate::trade::quote_transfer_fee(&h.quote_mint.to_account_info(),raw_output,false)?)?
        }else{raw_output};
        let sell_transfer_fee = raw_output.checked_sub(output).ok_or_else(|| error!(PumpError::Overflow))?;
        if buy && native {
            crate::user_quote_payments::transfer_native(a.system_program.as_ref(),&a.user,h.bonding_curve.as_ref(),amount)?;
        } else if buy {
            transfer_input(a,previous.as_ref(),&quote_token_program,&h.associated_quote_bonding_curve,h.quote_mint.decimals,AsRef::<AccountInfo>::as_ref(&*h.quote_mint),amount)?;
        } else {
            transfer_input(a,previous.as_ref(),&base_token_program,&h.associated_base_bonding_curve.to_account_info(),h.base_mint.decimals,AsRef::<AccountInfo>::as_ref(&*h.base_mint),amount)?;
        }
        // A02: Input succeeded; each checked operation immediately precedes its store.
        let c = &mut h.bonding_curve;
        if buy {
            c.virtual_token_reserves = sub(c.virtual_token_reserves,base_amount)?;
            c.real_token_reserves = sub(c.real_token_reserves,base_amount)?;
            c.virtual_quote_reserves = add(c.virtual_quote_reserves,quote_amount)?;
            c.real_quote_reserves = add(c.real_quote_reserves,quote_amount)?;
        } else {
            c.virtual_token_reserves = add(c.virtual_token_reserves,base_amount)?;
            c.real_token_reserves = add(c.real_token_reserves,base_amount)?;
            c.virtual_quote_reserves = sub(c.virtual_quote_reserves,quote_amount)?;
            c.real_quote_reserves = sub(c.real_quote_reserves,quote_amount)?;
        }
        let mint_key = h.base_mint.key();
        let bump = [bumps.bonding_curve];
        let seeds: &[&[u8]] = &[b"bonding-curve",mint_key.as_ref(),&bump];
        if last && (buy || !native) && (if buy{output}else{raw_output}) != 0 {



            if buy{transfer_base_out(&base_token_program,&h.associated_base_bonding_curve,&a.destination,&h.bonding_curve,h.base_mint.decimals,AsRef::<AccountInfo>::as_ref(&*h.base_mint),output,&[seeds])?;}else{transfer_quote_out(&quote_token_program,&h.associated_quote_bonding_curve,&a.destination,&h.bonding_curve,h.quote_mint.decimals,AsRef::<AccountInfo>::as_ref(&*h.quote_mint),raw_output,&[seeds])?;}
        }
        let adapter_difference = if buy { buy_transfer_fee } else { sell_transfer_fee };
        // S02: Both assertions reflect terminal original edges, not new recoverable guards.
        let product = pf as u128 * a.global.buyback_basis_points as u128;
        assert!(product >> 64 <= 9999,"buyback fee is at most protocol_fee");
        let buyback_raw = (product / 10000) as u64;
        assert!(pf >= buyback_raw,"buyback_fee never exceeds protocol_fee");
        let post_buyback_raw = if let Some(post)=post_fill.as_ref() {
            let product=post.protocol as u128*a.global.buyback_basis_points as u128;
            assert!(product >> 64 <= 9999,"buyback fee is at most protocol_fee");
            let value=(product/10000) as u64;
            assert!(post.protocol >= value,"buyback_fee never exceeds protocol_fee");
            value
        }else{0};
        let paid_buyback=buyback_raw.checked_add(post_buyback_raw).ok_or_else(
            ||error!(PumpError::Overflow))?;let received_buyback=if native{paid_buyback}else{sub(paid_buyback,crate::trade::quote_transfer_fee(&h.quote_mint.to_account_info(),paid_buyback,false)?)?};
        let post_buyback=if native{post_buyback_raw}else{sub(post_buyback_raw,crate::trade::quote_transfer_fee(&h.quote_mint.to_account_info(),post_buyback_raw,false)?)?};

        h.bonding_curve.protocol_fees = add(h.bonding_curve.protocol_fees,pf - buyback_raw)?;
        h.bonding_curve.creator_fee = add(h.bonding_curve.creator_fee,cf)?;
        let completed=buy && h.bonding_curve.real_token_reserves==0;
        if completed {
            h.bonding_curve.complete=true;
        } let buyback=received_buyback.checked_sub(post_buyback).ok_or_else(||error!(PumpError::Overflow))?;
        if let Some(post)=post_fill.as_ref() {
            h.bonding_curve.protocol_fees=add(h.bonding_curve.protocol_fees,sub(post.protocol,post_buyback_raw)?)?;
            h.bonding_curve.creator_fee=add(h.bonding_curve.creator_fee,post.creator)?;
            h.bonding_curve.post_complete_base_out=post.base;
            h.bonding_curve.post_complete_quote_in=post.quote;
        }
        // One quote transfer pays both buybacks; the receipt is assigned to the first fill before the post fill.
        if flag & 1 != 0 {
            if native {
                native_buyback(a,event_bump,&h.bonding_curve,paid_buyback)?;
            } else if paid_buyback != 0 {
                transfer_buyback_out(&quote_token_program,&h.associated_quote_bonding_curve,&a.buyback_fee_recipient,
                    &h.bonding_curve,h.quote_mint.decimals,AsRef::<AccountInfo>::as_ref(&*h.quote_mint),
                    paid_buyback,&[seeds])?;
            }
        }
        if native && !buy && last {
            move_lamports(&h.bonding_curve.to_account_info(),&a.user.to_account_info(),output)?;
        }
        let c = &h.bonding_curve;
        let event = trade_event(c,&a.global,&crate::UserVolumeAccumulator::default(),&a.user.key(),&mint_key,buy,base_amount,quote_amount,&(pf,cf,p_rate,c_rate),buyback,adapter_difference,"multi_hop_swap",Clock::get()?.unix_timestamp);














        route_event(a,&event,event_bump)?;
        if completed {
            let completion=crate::trade_types::CompleteEvent { user:a.user.key(),mint:mint_key,
                bonding_curve:h.bonding_curve.key(),timestamp:Clock::get()?.unix_timestamp,quote_mint:c.quote_mint };
            route_event(a,&completion,event_bump)?;
        }
        if let Some(post)=post_fill.as_ref() {
            let post_event=crate::trade::PostCompleteBuyEvent { user:a.user.key(),mint:mint_key,
                bonding_curve:h.bonding_curve.key(),quote_mint:c.quote_mint,timestamp:Clock::get()?.unix_timestamp,
                base_out:post.base,quote_in:post.quote,fee_basis_points:p_rate,fee:post.protocol,
                creator_fee_basis_points:c_rate,creator_fee:post.creator,buyback_fee:post_buyback,
                pool_base_reserves_before:post.pool_base,pool_quote_reserves_before:post.pool_quote,
                pool_base_reserves_after:sub(post.pool_base,post.base)?,pool_quote_reserves_after:add(post.pool_quote,post.quote)? };
            route_event(a,&post_event,event_bump)?;
        }
        h.exit(&crate::ID)?;
        current_mint = if buy { h.base_mint.key() } else { h.quote_mint.key() };
        previous = Some(PreviousHop { base_mint: mint_key,
            output_vault: if buy { h.associated_base_bonding_curve.to_account_info() } else { h.associated_quote_bonding_curve.to_account_info() },
            authority: h.bonding_curve.to_account_info(),bump: bumps.bonding_curve });
        amount = output;
        total_buyback = total_buyback.checked_add(add(buyback,post_buyback)?).ok_or_else(overflow)?;
        Ok((current_mint,amount,previous,total_buyback))
        }
    }
    require_keys_eq!(current_mint,a.destination.mint,PumpError::MultiHopDiscontinuousPath);
    Ok(CurveRunResult { amount_out: amount,buyback_fee: total_buyback })
}

const QUOTE_1: Pubkey = Pubkey::new_from_array([6, 155, 136, 87, 254, 171, 129, 132, 251, 104, 127, 99, 70, 24, 192, 53, 218, 196, 57, 220, 26, 235, 59, 85, 152, 160, 240, 0, 0, 0, 0, 1]);

const QUOTE_2: Pubkey = Pubkey::new_from_array([131, 13, 252, 159, 222, 95, 230, 184, 170, 124, 4, 164, 118, 233, 30, 138, 198, 187, 38, 74, 173, 144, 250, 25, 201, 223, 73, 216, 92, 62, 91, 94]);

const QUOTE_STABLE: Pubkey = Pubkey::new_from_array([198, 250, 122, 243, 190, 219, 173, 58, 61, 101, 243, 106, 171, 201, 116, 49, 177, 187, 228, 194, 210, 246, 224, 228, 124, 166, 2, 3, 69, 47, 93, 97]);

#[inline(never)]
pub fn transfer_quote_out<'info>(token_program:&AccountInfo<'info>,from:&UncheckedAccount<'info>,to:&InterfaceAccount<'info,TokenAccount>,authority:&Account<'info,BondingCurve>,decimals:u8,mint:&AccountInfo<'info>,amount:u64,signer_seeds:&[&[&[u8]];1])->Result<()>{
    anchor_spl::token_2022::transfer_checked(CpiContext::new_with_signer(token_program.clone(),anchor_spl::token_2022::TransferChecked{from:from.to_account_info(),to:to.to_account_info(),authority:authority.to_account_info(),mint:mint.clone()},signer_seeds),amount,decimals)
}






pub fn trade_event(curve:&BondingCurve,global:&Global,volume:&crate::UserVolumeAccumulator,user:&Pubkey,mint:&Pubkey,is_buy:bool,token_amount:u64,quote_amount:u64,fees:&(u64,u64,u64,u64),buyback_fee:u64,unparsed_trailing_field:u64,ix_name:&str,timestamp:i64)->TradeEvent{
    let virtual_quote_reserves=curve.virtual_quote_reserves;let real_quote_reserves=curve.real_quote_reserves;
    let quote_mint=curve.quote_mint;let is_sol=quote_mint==Pubkey::default();
    TradeEvent{
        quote_mint:curve.quote_mint,
        mint:*mint,
        sol_amount:if is_sol{quote_amount}else{0},
        is_buy,
        token_amount,
        user:*user,
        timestamp,
        virtual_sol_reserves:if is_sol{virtual_quote_reserves}else{0},
        virtual_token_reserves:curve.virtual_token_reserves,
        real_token_reserves:curve.real_token_reserves,
        fee_recipient:Pubkey::default(),
        fee_basis_points:fees.2,
        fee:fees.0,
        creator:curve.creator,
        creator_fee_basis_points:fees.3,
        creator_fee:fees.1,
        track_volume:false,
        total_unclaimed_tokens:volume.total_unclaimed_tokens,
        total_claimed_tokens:volume.total_claimed_tokens,
        current_sol_volume:volume.current_sol_volume,
        last_update_timestamp:volume.last_update_timestamp,
        ix_name:ix_name.to_string(),
        mayhem_mode:curve.is_mayhem_mode,
        cashback_fee_basis_points:0,
        cashback:0,
        real_sol_reserves:if is_sol{real_quote_reserves}else{0},
        buyback_fee_basis_points:if curve.is_mayhem_mode{0}else{global.buyback_basis_points},
        buyback_fee,
        shareholders:vec![],
        quote_amount,
        virtual_quote_reserves,
        real_quote_reserves,
        holder_rewards_bps:if curve.is_holder_reward{fees.3}else{0},
        holder_rewards:if curve.is_holder_reward{fees.1}else{0},
        creator_fee_unclaimed:curve.creator_fee,
        unparsed_trailing_field,
    }
}
#[inline(never)]
pub fn transfer_base_out<'info>(token_program:&AccountInfo<'info>,from:&InterfaceAccount<'info,TokenAccount>,to:&InterfaceAccount<'info,TokenAccount>,authority:&Account<'info,BondingCurve>,decimals:u8,mint:&AccountInfo<'info>,amount:u64,signer_seeds:&[&[&[u8]];1])->Result<()>{
    if amount==0{return Ok(());}
    anchor_spl::token_2022::transfer_checked(CpiContext::new_with_signer(token_program.clone(),anchor_spl::token_2022::TransferChecked{from:from.to_account_info(),to:to.to_account_info(),authority:authority.to_account_info(),mint:mint.clone()},signer_seeds),amount,decimals)
}
#[inline(never)]
pub fn transfer_buyback_out<'info>(token_program:&AccountInfo<'info>,from:&UncheckedAccount<'info>,to:&UncheckedAccount<'info>,authority:&Account<'info,BondingCurve>,decimals:u8,mint:&AccountInfo<'info>,amount:u64,signer_seeds:&[&[&[u8]];1])->Result<()>{
    if amount==0{return Ok(());}
    anchor_spl::token_2022::transfer_checked(CpiContext::new_with_signer(token_program.clone(),anchor_spl::token_2022::TransferChecked{from:from.to_account_info(),to:to.to_account_info(),authority:authority.to_account_info(),mint:mint.clone()},signer_seeds),amount,decimals)
}
