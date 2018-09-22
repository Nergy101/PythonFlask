from passlib.hash import sha256_crypt
password = sha256_crypt.hash("Etiam")
password2 = sha256_crypt.hash("Etiam")
# Etiam is het ww dat we hashen.
#Deze hash gebruik je in je Programma.
print(password)

#Om te kijken of een ingevoerd ww gelijk is of niet aan het Echte wachtwoord
#Wordt hieronder Etiam nogmaals gehashed en worden den 2 Hashes vergeleken.
#Het grappige is dat de hashes verschillend zijn, maar toch gelijk.

#Dit is een van de beste/meest gebruikte manieren om iets geheim te houden
print(sha256_crypt.verify("Etiam", password))
