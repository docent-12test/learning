
x = 4
y= 6
match x:
    case 1:
        print('x is 1')
    case 2:
        print('x is 2')
    case 3:
        print('x is 3')
    case y: 
        global y
        print(f'x is {y}')

exit(1)






flag = False
match (100, 200):
   case (100, 300):  # Mismatch: 200 != 300
       print('Case 1')
   case (100, 200) if flag:  # Successful match, but guard fails
       print('Case 2')
   case (100, y):  # Matches and binds y to 200
       print(f'Case 3, y: {y}')
   case _:  # Pattern not attempted
       print('Case 4, I match anything!')
