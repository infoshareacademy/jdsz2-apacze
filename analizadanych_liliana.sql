Co to jest wysoka roznica:


1. Top 10 najwiekszych roznic nominalnych
 / Jakub
2. 10-15% najwiekszych roznic procentowych / Mateusz
3. Liczba wnioskow powyzej mediany / Liliana

---3.1. Lista wnioskow powyzej mediany
with roznice_rekompensat
as
(
select id, kwota_rekompensaty, kwota_rekompensaty_oryginalna,
abs(kwota_rekompensaty-kwota_rekompensaty_oryginalna) as roznica
 from wnioski
 where abs(kwota_rekompensaty-kwota_rekompensaty_oryginalna) >0
),
mediana AS(
select
percentile_disc(0.5) within group (order by roznica) as mediana
from roznice_rekompensat
)
select * from roznice_rekompensat, mediana
where roznica >=mediana
order by roznica desc

----3.2. Liczba wnioskow powyzej mediany  #2131
with roznice_rekompensat
as
(
select id, kwota_rekompensaty, kwota_rekompensaty_oryginalna,
abs(kwota_rekompensaty-kwota_rekompensaty_oryginalna) as roznica
 from wnioski
 where abs(kwota_rekompensaty-kwota_rekompensaty_oryginalna) >0
),
mediana AS(
select
percentile_disc(0.5) within group (order by roznica) as mediana
from roznice_rekompensat
)

select count(1) from roznice_rekompensat,mediana
where roznica >=mediana


4. zbada� skrajne warto�ci 5% / Micha� 



Analiza:

1.rozklad czasu

2.wplyw partnera

3.wplyw kod kraju

4.wplyw klient biznesowy

5.wplyw liczba pasazerow