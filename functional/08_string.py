i = 10000
print(id(i))
j = 20000
print(id(j))
i += j
print(id(i))

a = "arvid"
print(id(a))
b = "hej"
print(id(b))

a += b

print(id(a))

a = "arvid is een zero"
print(a)
a = a.replace("zero", "hero")
print(a)
print(a.split(" "))

print(a.capitalize())
print(a.upper())

print(a.count("r"))
print(a.find("is"))
print(a.title())

s = "Python 3.13"
len(s)              # 10
s.isalpha()         # False (spatie/punt/cijfer aanwezig)
"Hello".isalpha()   # True
"123".isdigit()     # True
"abc123".isalnum()  # True
" \t".isspace()     # True

# python
"42".zfill(5)            # "00042"
"hi".center(6, "-")      # "--hi--"
"hi".ljust(5, ".")       # "hi..."
"hi".rjust(5, ".")       # "...hi"


list = ["Homer", "Marge", "Bart", "Lisa", "Maggie"]
print(", ".join(list))

for ch in "arvid":
    print(ch)

# python
s = "Een regel\nVolgende regel\tmet tab"
s_quote = 'Hij zei: \'ok\''
path = "C:\\Users\\<naam>\\Documents"

raw_path = r"C:\Users\<naam>\Documents\project"

naam = "homer"
score = 3.5
s = f"Hallo {naam}, je score = {score:.2f}"  # 2 decimalen



