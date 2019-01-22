# Zadanie 1

Za pomoc� modu�u pandas pobra� plik exams.csv. Agreguj�c po kilku kolumnach (np. gender oraz lunch  ) i wykonuj�c operacj� arytetyczne (przyk�adowo mean) otrzymujemy DataFrame z MultiIndexem. Nale�y utworzy� funkcj� reindex_df, kt�rej argumentem b�dzie taki DataFrame a wynikiem b�dzi� DataFrame, kt�ry b�dzi� mia� dodatkowe kolumny z odpowiednimi nazwami i index z kolejnymi liczbami od 0.

Przyk�ad:
```python
df = data.groupby(['gender','lunch']).mean()
print(df)

                     math score  reading score  writing score
gender lunch                                                 
female free/reduced   55.240964      67.234940      65.873494
       standard       67.956376      75.543624      75.929530
male   free/reduced   61.130890      60.214660      57.267016
       standard       73.539130      69.550725      67.695652


print(reindex_df(df))

   math score  reading score  writing score  gender         lunch
0   55.240964      67.234940      65.873494  female  free/reduced
1   67.956376      75.543624      75.929530  female      standard
2   61.130890      60.214660      57.267016    male  free/reduced
3   73.539130      69.550725      67.695652    male      standard

```

# Zadanie 2

(Zadania od Jakuba z model_classifier.py)

1. Napiszcie prosz� sami kod obliczaj�c� precision, recall oraz f1-score classification_report().

2. Napiszcie prosz� sami kod obliczaj�c� confusion matrix warto�ci powinny by� takie same jak te kt�re uzyskacie z funkcji confusion_matrix().
