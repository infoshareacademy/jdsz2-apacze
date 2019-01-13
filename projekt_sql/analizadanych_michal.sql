Co to jest wysoka roznica:


1. Top 10 najwiekszych roznic nominalnych
 / Jakub
2. 10-15% najwiekszych roznic procentowych / Mateusz
3. Liczba wnioskow powyzej mediany
 / Liliana
4. zbada� skrajne warto�ci - rozklad / Micha�


-- Ponizsze pokazuje wartosc zero dla wszystkich kwartylow mnniejszych niz 0.99 (pierwszy mniejszy kwartyl to 0.95). Podstawa liczenia to nominalna roznca miedzy
-- kwota rekompensaty oryginalna a wyplacona. Dla wartosci kwartyla 0.99 wartosc roznicy wynosi 150.

select unnest(
percentile_disc(array[0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
  within group (order by kwota_rekompensaty)
) as wartosc_kwwart_kwota_rekomp,
unnest(
percentile_disc(array[0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
  within group (order by kwota_rekompensaty_oryginalna)
) as wartosc_kwwart_kwota_rekomp_oryg,
unnest(
percentile_disc(array[0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
  within group (order by kwota_rekompensaty_oryginalna - kwota_rekompensaty)
) as wartosc_kwart_roznica_kwota_rekomp_oryg_a_wypl,
unnest(array[0.25, 0.5, 0.75, 0.9, 0.95, 0.99]) as rzad_kwantylu
from wnioski
where stan_wniosku like '%wypl%'

-- Ponizej wypisane wnioski z kwartylu 0.99
with wnioski_kwartyl_99 as (
  select *, kwota_rekompensaty_oryginalna - kwota_rekompensaty as roznica_kwot_oryg_reko
  from wnioski
  where kwota_rekompensaty_oryginalna - kwota_rekompensaty >= 125 and stan_wniosku like '%wypl%'
)

select * from wnioski_kwartyl_99;

--Analiza:

--1.rozklad czasu

--Badam roznice kwot wzgledem kolejnych miesiecy w latach. W kazdym miesiacu wzialem jedynie skrajne .99 wartosci i sprawdzilem mediane roznic.
--Widac generalny trend spadkowy w kolejnych miesiacach. Od maja 2017 widac stabilizacje

with wnioski_kwartyl_99 as (
  select *, kwota_rekompensaty_oryginalna - kwota_rekompensaty as roznica_kwot_oryg_reko
  from wnioski
  where kwota_rekompensaty_oryginalna - kwota_rekompensaty >= 125 and stan_wniosku like '%wypl%'
)

select to_char(data_utworzenia, 'YYYY-MM'),
  percentile_disc(array[0.5])
  within group (order by roznica_kwot_oryg_reko)
  from wnioski_kwartyl_99
group by 1

--2.wplyw kod kraju

--Usuwam dane wczesniejsze niz 2017-6 i patrze na wnioski

with wnioski_kwartyl_99 as (
select *, kwota_rekompensaty_oryginalna - kwota_rekompensaty as roznica_kwot_oryg_reko
  from wnioski
  where kwota_rekompensaty_oryginalna - kwota_rekompensaty >= 125 and stan_wniosku like '%wypl%'
)

select kod_kraju, count(1)
  from wnioski_kwartyl_99
where to_char(data_utworzenia, 'YYYY-MM') like '2017%' or to_char(data_utworzenia, 'YYYY-MM') like '2018%'
group by kod_kraju

-- Najwiecej takich skrajnych wnioskow pochodzi z ZZ oraz IE, na nich sie skupiam w dalszej analzie

--3.wplyw klient biznesowy a inny

with wnioski_kwartyl_99 as (
select *, kwota_rekompensaty_oryginalna - kwota_rekompensaty as roznica_kwot_oryg_reko
  from wnioski
  where kwota_rekompensaty_oryginalna - kwota_rekompensaty >= 125 and stan_wniosku like '%wypl%'
  and kod_kraju in ('ZZ', 'IE') and (to_char(data_utworzenia, 'YYYY-MM') like '2017%' or to_char(data_utworzenia, 'YYYY-MM') like '2018%')
)

select typ_podrozy, count(1)
  from wnioski_kwartyl_99
group by typ_podrozy

--Wszystkie wnioski w przedziale nie maja przydzielonego typu podrozy.

--4.wplyw liczba pasazerow


with wnioski_kwartyl_99 as (
select *, kwota_rekompensaty_oryginalna - kwota_rekompensaty as roznica_kwot_oryg_reko
  from wnioski
  where kwota_rekompensaty_oryginalna - kwota_rekompensaty >= 125 and stan_wniosku like '%wypl%'
  and kod_kraju in ('ZZ', 'IE') and (to_char(data_utworzenia, 'YYYY-MM') like '2017%' or to_char(data_utworzenia, 'YYYY-MM') like '2018%')
)

select liczba_pasazerow, count(1)
  from wnioski_kwartyl_99
group by liczba_pasazerow

--- Prawie caly zbior posiada 1 lub 2 pasazerow, wieksza ilosc jest juz nie warta uwagi (łącznie 4 wnioski)

/* Badane wnioski ze 0.99 percentyla. Od czerwca 2017 nastapila stabilazacja sredniomiesieczna w grupie. Najwiecej wnioskow pochodzi z ZZ oraz IE. Ograniczajac sie tylko
do tych dwoch krajow, zaden wniosek nie ma przypisanego typu klienta (ani biznesowy, ani prywatny). To moze oznaczac ze takie wnioski maja pewne braki w danych.
Patrzac na powyzsze dane z perspektywy ilosci pasazerow widac ze prawie wszystkie wnioski mialy 1 (liczba 641) lub 2 pasazerow (liczba 199), wyzsze ilosci sa skrajne (lacznie 2).
 */

