import bcrypt

pas = 'Scanme123@'.encode('utf-8')

x_pas = bcrypt.hashpw(pas, bcrypt.gensalt())

x = bcrypt.hashpw(pas, x_pas)

if x == x_pas:
   print("true")

print(x)
print(x_pas)
