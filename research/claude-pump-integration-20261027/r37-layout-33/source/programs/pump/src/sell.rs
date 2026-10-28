#[path = "fee_recipient.rs"]
pub(crate) mod fee_recipient;
use anchor_lang::prelude::*;
use anchor_spl::token_interface::{self,Mint,TokenAccount,TokenInterface,TransferChecked};
use crate::{Global,PumpError};
use crate::trade_types::{BondingCurve,TradeEvent};

#[derive(Clone)]pub struct LegacyCurve(pub BondingCurve,pub usize);
impl std::ops::Deref for LegacyCurve{type Target=BondingCurve;fn deref(&self)->&BondingCurve{&self.0}}
impl std::ops::DerefMut for LegacyCurve{fn deref_mut(&mut self)->&mut BondingCurve{&mut self.0}}
impl Owner for LegacyCurve{fn owner()->Pubkey{crate::ID}}
impl AccountDeserialize for LegacyCurve{fn try_deserialize(buf:&mut &[u8])->Result<Self>{let len=buf.len();Ok(Self(BondingCurve::try_deserialize(buf)?,len))}fn try_deserialize_unchecked(buf:&mut &[u8])->Result<Self>{Self::try_deserialize(buf)}}
impl AccountSerialize for LegacyCurve{fn try_serialize<W:std::io::Write>(&self,w:&mut W)->Result<()>{let mut b=Vec::new();self.0.try_serialize(&mut b)?;w.write_all(&b[..self.1.min(b.len())])?;Ok(())}}
pub use crate::pump_fees::{
    accounts::FeeConfig as LegacyFeeConfig,
    program::PumpFees as LegacyFeesProgram,
};

#[inline(never)]
pub fn process_cashback(remaining_ptr:*const u8,remaining_len:usize,user:*const u8,system_program:*const u8,curve:*const u8,amount:u64,mint:&Pubkey)->Result<()>{
    let remaining_accounts=unsafe{std::slice::from_raw_parts(remaining_ptr as *const AccountInfo,remaining_len)};let user=unsafe{&*(user as *const AccountInfo)};let system_program=unsafe{&*(system_program as *const AccountInfo)};let curve=unsafe{&*(curve as *const AccountInfo)};let user_key=user.key();let (pda,bump)=Pubkey::find_program_address(&[b"user_volume_accumulator",user_key.as_ref()],&crate::ID);
    let bump_arr=[bump];let seeds:&[&[u8]]=&[b"user_volume_accumulator",user_key.as_ref(),&bump_arr];
    let acc=remaining_accounts.first().ok_or_else(||error!(PumpError::MissingCashbackAccounts))?;









    require!(acc.key()==pda,PumpError::InvalidCashbackAccumulator);
    if acc.data_is_empty(){
        let rent=Rent::get()?;
        let space=82u64;
        let need=rent.minimum_balance(space as usize);
        if acc.lamports()<need{
            let pay=need-acc.lamports();
            anchor_lang::solana_program::program::invoke(&anchor_lang::solana_program::system_instruction::transfer(user.key,acc.key,pay),&[user.clone(),acc.clone(),system_program.clone()])?;
        }
        anchor_lang::solana_program::program::invoke_signed(&anchor_lang::solana_program::system_instruction::allocate(acc.key,space),&[acc.clone(),system_program.clone()],&[seeds])?;
        anchor_lang::solana_program::program::invoke_signed(&anchor_lang::solana_program::system_instruction::assign(acc.key,&crate::ID),&[acc.clone(),system_program.clone()],&[seeds])?;
    }




































    require!(acc.owner==&crate::ID,PumpError::InvalidCashbackAccumulator);



    require!(acc.data_len()>=82,PumpError::InvalidCashbackAccumulator);
    let earned={let data=acc.try_borrow_data()?;u64::from_le_bytes(data[74..82].try_into().unwrap())};















    let next=earned.checked_add(amount).ok_or_else(||error!(PumpError::Overflow))?;let curve_left=curve.lamports().checked_sub(amount).ok_or_else(||error!(PumpError::Overflow))?;
    let _=curve_left;
    curve.sub_lamports(amount)?;
    acc.add_lamports(amount)?;
    acc.try_borrow_mut_data()?[74..82].copy_from_slice(&next.to_le_bytes());
    require!(remaining_accounts.len()>1,PumpError::InvalidBondingCurveV2);
    let curve_v2=&remaining_accounts[1];
    let (curve_pda,_)=Pubkey::find_program_address(&[b"bonding-curve-v2",mint.as_ref()],&crate::ID);




    require!(curve_v2.key()==curve_pda,PumpError::InvalidBondingCurveV2);
    Ok(())
}








pub fn check_bonding_curve_v2<'info>(remaining_accounts:&[AccountInfo<'info>],mint:&Pubkey)->Result<()>{
    require!(!remaining_accounts.is_empty(),PumpError::InvalidBondingCurveV2);let bonding_curve_v2=&remaining_accounts[0];
    let (expected,_)=Pubkey::find_program_address(&[b"bonding-curve-v2",mint.as_ref()],&crate::ID);
// layout-pad(5): aligns the next Source site with the original line




    require!(bonding_curve_v2.key()==expected,PumpError::InvalidBondingCurveV2);
    Ok(())
}
// layout-pad(8): aligns the next Source site with the original line







pub fn buyback_fee_recipient<'a,'info>(remaining_accounts:&'a [AccountInfo<'info>],global:&Global,index:usize)->Result<&'a AccountInfo<'info>>{
    require!(index<remaining_accounts.len(),PumpError::BuybackFeeRecipientMissing);let account=&remaining_accounts[index];
    let result=global.validate_buyback_fee_recipient(&account.key());result.map(|_|account)

}

// Displaced from lines 19-45 so process_cashback can occupy the original sell.rs error lines.
#[derive(Accounts)]
pub struct LegacySell<'info>{
 #[account(seeds=[b"global"],bump)]pub global:Box<Account<'info,Global>>,
 /// CHECK: handler validates recipient.
 #[account(mut)]pub fee_recipient:UncheckedAccount<'info>,
 pub mint:InterfaceAccount<'info,Mint>,
 #[account(mut,seeds=[b"bonding-curve",mint.key().as_ref()],bump,constraint=bonding_curve.quote_mint==Pubkey::default() @ PumpError::UnsupportedQuoteMint)]pub bonding_curve:Account<'info,BondingCurve>,
 #[account(mut,associated_token::mint=mint,associated_token::authority=bonding_curve,associated_token::token_program=token_program)]pub associated_bonding_curve:InterfaceAccount<'info,TokenAccount>,
 #[account(mut,token::mint=mint)]pub associated_user:InterfaceAccount<'info,TokenAccount>,
 #[account(mut)]pub user:Signer<'info>,
 pub system_program:Program<'info,System>,
 /// CHECK: PDA checked.
 #[account(mut,seeds=[b"creator-vault",bonding_curve.creator.as_ref()],bump)]pub creator_vault:AccountInfo<'info>,
 pub token_program:Interface<'info,TokenInterface>,
 /// CHECK: event authority.
 #[account(seeds=[b"__event_authority"],bump)]pub event_authority:AccountInfo<'info>,
 /// CHECK: self CPI.
 pub program:Program<'info,crate::program::PumpRecovered>,
 /// CHECK: fee program validates config.
 #[account(seeds=[b"fee_config",crate::ID.as_ref()],bump,seeds::program=fee_program.key())]
 pub fee_config:Account<'info,LegacyFeeConfig>,
 /// CHECK: canonical dependency.
 pub fee_program:Program<'info,LegacyFeesProgram>,
}
pub(crate) fn add(a:u64,b:u64)->Result<u64>{a.checked_add(b).ok_or_else(||error!(PumpError::Overflow))}
pub(crate) fn sub(a:u64,b:u64)->Result<u64>{a.checked_sub(b).ok_or_else(||error!(PumpError::Overflow))}
pub(crate) fn narrow(a:u128)->Result<u64>{u64::try_from(a).map_err(|_|error!(PumpError::Truncation))}

#[path="fee_cpi.rs"]
pub(crate) mod fee_cpi;

#[path="util/fee.rs"]
pub mod fee_math;
