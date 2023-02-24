from interface.user_bill import *

# user_bill().get_bill({
#     "username": "12345"
# })

user_bill().create_bill_by_user({
    "username": "123456",
    "total_in": 10000,
    "total_out": 10000,
})
