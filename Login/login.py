def validateUserAccount():
    global index_num,userName,passWord,balances,username,password
    username=input("Enter your username : ")
    password=input("Enter your password : ")
    fileRead=open('test.txt','r')
    flag=False
    while True:
        line=fileRead.readline()
        lineLength=len(line)
        if lineLength==0:
            break
        lineItem=line.split()
        if username.strip()==lineItem[0] and password.strip()==lineItem[1] :
            print("Hello !",username," you have logged in successfully.")
            flag=True
            break
    if flag==False:
        print("The user is not found.Please re-enter your username and password.")
        validateUserAccount()