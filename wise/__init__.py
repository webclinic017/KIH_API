from wise import constants
from wise.wise_models import UserProfiles, Account, ExchangeRate, Recipient, Quote, Transfer, Fund

profile_id: int
recipient_id: int
quote_id: str
for user_profile in UserProfiles.call():
    profile_id = user_profile.id
    recipient_id = Recipient.call(user_profile.id)[0].id
    break

quote_id = str(Quote.call(profile_id, "NZD", "NZD", 1000, recipient_id).id)
transfer_id = Transfer.call(recipient_id, quote_id, "API Test").id
test1 = Fund.call(profile_id, transfer_id)
pass