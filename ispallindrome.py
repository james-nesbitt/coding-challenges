
s = "isthissihtsi"

if len(s)<2:
    print("Cannot be a pallindrome")
else:
    l = len(s)
    for i in range(int(l/2)):
        if s[i] != s[l-i-1]:
            print("Not a pallindrome")
            break
    else:
        print("is a pallindrome")
