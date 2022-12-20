from goat_grade import GOAT_GRADE

for year in range(1950, 2024):
    print(year)    
    GOAT_GRADE(year, folder="goat_grade/", file_name=f"gg_{str(year)}")

