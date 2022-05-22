from wise.models import Account, ProfileTypes, ReserveAccount, CashAccount

test = Account.get_all_by_profile_type(ProfileTypes.PERSONAL)
pass
